# -*- coding: utf-8 -*-
"""
09_retranslate.py — 定向补译与修复器（质量闭环的「回归修复」环节）

用途
----
全量翻译后，用低 Han 占比扫描会暴露两类段：
  (a) 本就该保留英文的：代码块、CLI 命令、JSON、文献引用、OWASP 译者署名、对抗性乱码样本；
  (b) 真·漏译的英文正文（批量解析失败时按 `04_translate.py` 的保守策略回填了原文）。

本脚本只处理 (b)：按显式 id 清单重译，写回 work/translations.jsonl（原地更新，先备份），
不改变分段与术语保护逻辑，因此 05_assemble.py 可直接复跑。

修复溯源
--------
每次修复都追加到 work/fix_log.jsonl（id / 原因 / 修复前后 Han 占比 / 引擎 / 时间戳），
用于在质量报告里证明「问题被发现→被定位→被修复→被复检」的闭环，而不是宣称无缺陷。

用法
----
    python tools/09_retranslate.py --scan                 # 只打印候选，不调用模型
    python tools/09_retranslate.py --ids-file work/retranslate_ids.json --workers 4
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"
SEGMENTS = WORK / "segments.jsonl"
OUT = WORK / "translations.jsonl"
BACKUP = WORK / "translations.bak.jsonl"
FIXLOG = WORK / "fix_log.jsonl"
GLOSSARY = ROOT / "tools" / "glossary.json"

DEFAULT_BASE = os.environ.get("TRANSLATE_BASE_URL", "")
DEFAULT_KEY = os.environ.get("TRANSLATE_API_KEY", "")
DEFAULT_MODEL = os.environ.get("TRANSLATE_MODEL", "")

# 明确「不该翻译」的形态：命中即从候选里剔除，避免把代码/引用/署名译坏
NO_TRANSLATE_PATTERNS = [
    re.compile(r"^<!--\s*(source|来源)"),          # 抽取溯源注释
    re.compile(r"^```"),                            # 代码围栏
    re.compile(r"^\s*[\{\[\"]"),                    # JSON / 配置片段
    re.compile(r"^\s*(npm|npx|yarn|pnpm|git|cd|curl|brew|winget|irm|docker|kubectl|helm|codex|claude)\s"),
    re.compile(r"^\s*(const|let|var|import|export|function|async|await|return|#include|enum|class)\s"),
    re.compile(r"^\s*#\s*(Analyze|Automate|Bulk)"),  # shell 注释示例
    re.compile(r"@techreport|@article|@inproceedings|@misc"),   # BibTeX
    re.compile(r"\[\d+\]\s*[A-Z][a-z]+,", ),         # 参考文献条目
    re.compile(r"\[email protected\]|gmail\.com|\(at\)"),        # 署名/邮箱
    re.compile(r"^\s*[A-Za-z][A-Za-z\-\.]*\s*:\s*[\"']"),        # key: "value"
    re.compile(r"^\s*[\w\.\-]+\s*\([^)]*\)\s*$"),     # 纯标识符
]


def looks_non_translatable(src: str) -> bool:
    s = src.strip()
    if any(p.search(s) for p in NO_TRANSLATE_PATTERNS):
        return True
    # 无空格的长 token 串（URL/路径/标识符）
    if " " not in s and len(s) > 12 and re.fullmatch(r"[\w\.\-/:@#\[\]<>]+", s):
        return True
    return False


def han_ratio(s: str) -> float:
    if not s:
        return 0.0
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff") / len(s)


def load_glossary():
    g = json.loads(GLOSSARY.read_text(encoding="utf-8"))
    terms = g.get("terms", {})
    lines = []
    for en, meta in terms.items():
        zh = meta.get("zh") if isinstance(meta, dict) else meta
        if zh:
            lines.append(f"{en} => {zh}")
    return lines, g.get("do_not_translate", [])


def build_system_prompt():
    terms, dnt = load_glossary()
    dnt_txt = "、".join(dnt) if dnt else "（无）"
    return (
        "你是专业的技术文档译者，负责把 Stanford CS146S「Vibe Coding / AI 辅助软件工程」"
        "课程资料从英文翻译成简体中文。\n\n"
        "【硬性规则】\n"
        "1. 术语必须严格使用下表译法，不得同义替换；术语首次出现时用「中文（English）」标注，其后只用中文。\n"
        "2. 下列词汇永不翻译，保留英文原形：" + dnt_txt + "\n"
        "3. 形如 @K12@ 的占位符是受保护的代码/术语/链接，必须原样保留在译文对应位置，"
        "不得增删、改写编号或改变数量。\n"
        "4. 保持 Markdown 结构：标题层级、列表符号、表格行列、代码块围栏一律不动。\n"
        "5. 只输出译文，不要解释、不要前言后语、不要重复原文。\n"
        "6. 段落内的英文代码/命令/文件名保留英文，其余正文一律译为中文。\n"
        "7. 语言自然流畅，避免翻译腔；长句可拆分，但不得丢失信息。\n\n"
        "【术语表】\n" + "\n".join(terms) + "\n"
    )


def call_chat(base_url, api_key, model, system, user, timeout=240):
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
        "stream": False,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + api_key},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def placeholder_ok(src, zh):
    want = re.findall(r"@K\d+@", src)
    got = re.findall(r"@K\d+@", zh or "")
    return sorted(want) == sorted(got)


def scan(min_len=40, max_ratio=0.10):
    segs = {}
    for line in SEGMENTS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            s = json.loads(line)
            segs[s["id"]] = s
    cands = []
    for line in OUT.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        t = json.loads(line)
        zh = t.get("zh") or ""
        seg = segs.get(t["id"], {})
        if len(zh) < min_len:
            continue
        if han_ratio(zh) >= max_ratio:
            continue
        if seg.get("kind") in ("code", "code-block"):
            continue
        if looks_non_translatable(seg.get("source", "")):
            continue
        cands.append({"id": t["id"], "doc": t["doc"], "len": len(zh),
                      "ratio": round(han_ratio(zh), 3),
                      "head": seg.get("source", "")[:90].replace("\n", " ")})
    return cands


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--ids-file", default=None)
    ap.add_argument("--ids", default=None, help="逗号分隔的 id 列表")
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--base-url", default=DEFAULT_BASE)
    ap.add_argument("--api-key", default=DEFAULT_KEY)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    if args.scan:
        cands = scan()
        print(f"[scan] 候选 {len(cands)} 段（已剔除代码/引用/署名等不该翻译的形态）")
        for c in sorted(cands, key=lambda x: (x["doc"], x["id"])):
            print(f"{c['doc']}#{c['id'].split('#')[-1]} | len={c['len']} | han={c['ratio']} | {c['head']}")
        return

    ids = []
    if args.ids_file:
        ids = json.loads(Path(args.ids_file).read_text(encoding="utf-8"))
        if isinstance(ids, dict):
            ids = ids.get("ids", [])
    if args.ids:
        ids = [x.strip() for x in args.ids.split(",") if x.strip()]
    if not ids:
        ids = [c["id"] for c in scan()]
    ids = list(dict.fromkeys(ids))

    if not (args.base_url and args.api_key and args.model):
        print("缺少 --base-url / --api-key / --model（或同名环境变量）。")
        sys.exit(2)

    segs = {}
    for line in SEGMENTS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            s = json.loads(line)
            segs[s["id"]] = s

    entries = {}
    order = []
    for line in OUT.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        t = json.loads(line)
        entries[t["id"]] = t
        order.append(t["id"])

    if not BACKUP.exists():
        BACKUP.write_text(OUT.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"[info] 已备份 -> {BACKUP}")

    system = build_system_prompt()
    todo = [i for i in ids if i in entries and i in segs]
    print(f"[info] 待补译 {len(todo)} 段 | 并发 {args.workers}")

    def do_one(sid):
        seg = segs[sid]
        src = seg.get("protected") or seg.get("source", "")
        user = ("请把下面这段技术文档正文完整翻译成简体中文，保持 Markdown 结构：\n\n" + src)
        zh = call_chat(args.base_url, args.api_key, args.model, system, user)
        zh = zh.strip()
        ok = placeholder_ok(src, zh)
        if not ok:
            zh = call_chat(args.base_url, args.api_key, args.model, system,
                           user + "\n\n注意：必须原样保留所有 @K{n}@ 占位符，一个都不能少。")
            zh = zh.strip()
            ok = placeholder_ok(src, zh)
        return sid, zh, ok

    fixed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(do_one, i): i for i in todo}
        for k, fut in enumerate(as_completed(futs), 1):
            sid = futs[fut]
            old = entries[sid].get("zh") or ""
            try:
                sid, zh, ok = fut.result()
            except Exception as e:
                print(f"[warn] {sid} 补译失败：{type(e).__name__} {e}")
                continue
            if not zh or not ok:
                print(f"[warn] {sid} 占位符校验未通过，保留原译文")
                continue
            entries[sid]["zh"] = zh
            entries[sid]["engine"] = args.model
            entries[sid]["ts"] = int(time.time())
            entries[sid]["repaired"] = True
            entries[sid]["han_before"] = round(han_ratio(old), 3)
            entries[sid]["han_after"] = round(han_ratio(zh), 3)
            with FIXLOG.open("a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "id": sid, "doc": entries[sid]["doc"],
                    "han_before": entries[sid]["han_before"],
                    "han_after": entries[sid]["han_after"],
                    "engine": args.model, "ts": int(time.time()),
                    "reason": "低 Han 占比疑似漏译，定向补译",
                }, ensure_ascii=False) + "\n")
            fixed += 1
            if k % 5 == 0 or k == len(futs):
                print(f"[progress] {k}/{len(futs)} | 修复 {fixed} 段")

    with OUT.open("w", encoding="utf-8") as f:
        for sid in order:
            f.write(json.dumps(entries[sid], ensure_ascii=False) + "\n")
    print(f"[done] 补译写回 {fixed} 段 -> {OUT}")


if __name__ == "__main__":
    main()
