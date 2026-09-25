# -*- coding: utf-8 -*-
"""
04_translate.py — 机器翻译执行器（方案 C 的「脚本流水线」半边）

设计原则
--------
1. 引擎无关：通过 OpenAI 兼容的 /chat/completions 协议调用任意模型端点
   （DeepSeek / Moonshot / Qwen / OpenAI / 本地 vLLM / Ollama 均可）。
2. 可复跑：断点续传，已完成的 segment 不重复请求；输出追加写。
3. 术语强制：把 glossary 注入 system prompt；保护占位符 @K{n}@ 必须原样回填。
4. 批量：一次请求携带多条 segment，用分隔符编号，返回后按编号对齐。
5. 零硬编码密钥：从环境变量或 --base-url/--api-key 参数读取。

用法
----
    python tools/04_translate.py --probe                 # 探测端点是否可用
    python tools/04_translate.py --doc prompt-engineering-overview
    python tools/04_translate.py --all --batch 12 --workers 4
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"
SEGMENTS = WORK / "segments.jsonl"
OUT = WORK / "translations.jsonl"
GLOSSARY = ROOT / "tools" / "glossary.json"

DEFAULT_BASE = os.environ.get("TRANSLATE_BASE_URL", "")
DEFAULT_KEY = os.environ.get("TRANSLATE_API_KEY", "")
DEFAULT_MODEL = os.environ.get("TRANSLATE_MODEL", "")

SENTINEL = "<<<SEG>>>"


def load_glossary():
    g = json.loads(GLOSSARY.read_text(encoding="utf-8"))
    terms = g.get("terms", {})
    dnt = g.get("do_not_translate", [])
    lines = []
    for en, meta in terms.items():
        zh = meta.get("zh") if isinstance(meta, dict) else meta
        if zh:
            lines.append(f"{en} => {zh}")
    return lines, dnt, g.get("_meta", {})


def build_system_prompt():
    terms, dnt, meta = load_glossary()
    dnt_txt = "、".join(dnt) if dnt else "（无）"
    return (
        "你是专业的技术文档译者，负责把 Stanford CS146S「Vibe Coding / AI 辅助软件工程」"
        "课程资料从英文翻译成简体中文。\n\n"
        "【硬性规则】\n"
        "1. 术语必须严格使用下表译法，不得同义替换；术语首次出现时用「中文（English）」标注，其后只用中文。\n"
        "2. 下列词汇永不翻译，保留英文原形，不得音译或意译：" + dnt_txt + "\n"
        "3. 形如 @K12@ 的占位符是受保护的代码/术语/链接，必须原样保留在译文的对应位置，"
        "不得增删、改写编号或改变数量。\n"
        "4. 保持 Markdown 结构：标题层级、列表符号、表格行列、代码块围栏（```）与内的代码一律不动。\n"
        "5. 只输出译文，不要解释、不要加前言后语、不要重复原文。\n"
        "6. 若某条内容本身已是中文或纯代码/纯符号，原样返回。\n"
        "7. 语言自然流畅，避免翻译腔；长句可拆分，但不得丢失信息。\n\n"
        "【术语表】\n" + "\n".join(terms) + "\n"
    )


def call_chat(base_url, api_key, model, system, user, timeout=180):
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
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def probe(base_url, api_key, model):
    print(f"[probe] base_url = {base_url or '(未设置)'}")
    print(f"[probe] model    = {model or '(未设置)'}")
    if not base_url or not api_key:
        print("[probe] 缺少 base_url 或 api_key —— 请设置 TRANSLATE_BASE_URL / TRANSLATE_API_KEY")
        return 1
    try:
        out = call_chat(base_url, api_key, model,
                        "You are a translator.", "Translate to Chinese: hello world",
                        timeout=60)
        print("[probe] OK ->", out.strip()[:120])
        return 0
    except Exception as e:
        print("[probe] FAILED ->", type(e).__name__, e)
        return 2


def load_done():
    done = {}
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("zh"):
                done[r["id"]] = r
    return done


def load_segments():
    return [json.loads(l) for l in SEGMENTS.read_text(encoding="utf-8").splitlines() if l.strip()]


def should_translate(seg):
    if seg.get("status") == "skip":
        return False
    if seg.get("kind") in ("code", "code-block"):
        return False
    src = seg.get("source", "")
    if not src.strip():
        return False
    # 纯符号/纯 markdown 分隔线
    if re.fullmatch(r"[\s\-\*_=#>`|:\.]*", src):
        return False
    return True


def build_batch(segs):
    parts = []
    for i, s in enumerate(segs):
        parts.append(f"{SENTINEL}{i}{SENTINEL}\n{s['protected']}")
    return "\n".join(parts)


def parse_batch_reply(text, n):
    """按哨兵切分回复，返回 {index: zh}。"""
    out = {}
    pattern = re.compile(re.escape(SENTINEL) + r"(\d+)" + re.escape(SENTINEL))
    matches = list(pattern.finditer(text))
    if not matches:
        return out
    for j, m in enumerate(matches):
        idx = int(m.group(1))
        start = m.end()
        end = matches[j + 1].start() if j + 1 < len(matches) else len(text)
        out[idx] = text[start:end].strip()
    return out


def check_placeholders(src, zh):
    """校验保护占位符是否全部原样保留。"""
    want = re.findall(r"@K\d+@", src)
    got = re.findall(r"@K\d+@", zh or "")
    return sorted(set(want)) == sorted(set(got)) and len(want) == len(got)


def process_batch(batch, base_url, api_key, model, system, retries=2):
    """返回本批的翻译结果列表。"""
    user = (
        "请逐条翻译下面的内容。每条以 <<<SEG i>>> 开头，"
        "请对每条都在其译文前输出同样的标记，然后接译文。\n\n"
        + build_batch(batch)
    )
    last_err = None
    for attempt in range(retries + 1):
        try:
            reply = call_chat(base_url, api_key, model, system, user)
            parsed = parse_batch_reply(reply, len(batch))
            results = []
            for i, seg in enumerate(batch):
                zh = parsed.get(i, "")
                if not zh:
                    zh = seg["protected"]  # 解析失败时保守回填原文
                if not check_placeholders(seg["protected"], zh):
                    # 占位符丢失 -> 重试一次该批
                    if attempt < retries:
                        raise ValueError(f"placeholder mismatch in {seg['id']}")
                results.append({
                    "id": seg["id"],
                    "doc": seg["doc"],
                    "idx": seg["idx"],
                    "kind": seg["kind"],
                    "source": seg["source"],
                    "protected": seg["protected"],
                    "zh": zh,
                    "placeholders_ok": check_placeholders(seg["protected"], zh),
                    "engine": model,
                    "ts": int(time.time()),
                })
            return results
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"batch failed after retries: {last_err}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--doc", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--batch", type=int, default=10)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--base-url", default=DEFAULT_BASE)
    ap.add_argument("--api-key", default=DEFAULT_KEY)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    if args.probe:
        sys.exit(probe(args.base_url, args.api_key, args.model))

    if not (args.base_url and args.api_key and args.model):
        print("缺少 --base-url / --api-key / --model（或同名环境变量）。")
        print("例如：")
        print('  $env:TRANSLATE_BASE_URL="https://api.deepseek.com/v1"')
        print('  $env:TRANSLATE_API_KEY="sk-..."')
        print('  $env:TRANSLATE_MODEL="deepseek-chat"')
        print("  python tools/04_translate.py --all")
        sys.exit(2)

    system = build_system_prompt()
    segs = load_segments()
    done = load_done()

    todo = [s for s in segs if should_translate(s) and s["id"] not in done]
    if args.doc:
        todo = [s for s in todo if s["doc"] == args.doc]
    if args.limit:
        todo = todo[: args.limit]

    print(f"[info] 总段 {len(segs)} | 已完成 {len(done)} | 本次待译 {len(todo)}")
    if not todo:
        print("[info] 无待译内容。")
        return

    batches = [todo[i:i + args.batch] for i in range(0, len(todo), args.batch)]
    print(f"[info] 批次数 {len(batches)} | 并发 {args.workers} | 批大小 {args.batch}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fout = OUT.open("a", encoding="utf-8")
    ok = fail = 0
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(process_batch, b, args.base_url, args.api_key,
                          args.model, system): b for b in batches}
        for k, fut in enumerate(as_completed(futs), 1):
            try:
                rows = fut.result()
                for r in rows:
                    fout.write(json.dumps(r, ensure_ascii=False) + "\n")
                fout.flush()
                ok += len(rows)
            except Exception as e:
                fail += len(futs[fut])
                print(f"[warn] 批次失败：{e}")
            if k % 5 == 0 or k == len(futs):
                rate = ok / max(1e-9, time.time() - t0)
                print(f"[progress] {k}/{len(futs)} 批 | 成功 {ok} 段 | 失败 {fail} 段 | {rate:.1f} 段/秒")

    fout.close()
    print(f"[done] 成功 {ok} | 失败 {fail} | 输出 {OUT}")


if __name__ == "__main__":
    main()
