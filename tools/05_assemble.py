# -*- coding: utf-8 -*-
"""
05_assemble.py — 译文回填与重组器

把 work/translations.jsonl 的逐段译文回填到保护占位符，还原为完整 Markdown 文档，
输出到 dist/zh/<doc>.md，并生成覆盖度报告 quality/coverage.md。

可复跑：任何时候重跑都会基于最新 translations.jsonl 重新生成全部分发文件。
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"
DIST = ROOT / "dist"
ZH = DIST / "zh"
QUALITY = ROOT / "quality"
GLOSSARY = ROOT / "tools" / "glossary.json"


def src_join(rows):
    return "".join(r.get("source", "") for r in rows)


def load_jsonl(p):
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def restore_placeholders(zh, pmap):
    """把 @K{n}@ 还原为原始受保护文本。

    修复记录（v1.1）：原实现 pmap.get(m.group(1)) 取到的是 "0"，
    而 protected_map 的键是 "@K0@"，键格式不匹配 → 2030 个占位符全部未还原。
    现做键归一化，并容忍 @k0@ / @ K0 @ 等模型变体。
    """
    if not pmap:
        return zh
    norm = {}
    for k, v in pmap.items():
        mm = re.fullmatch(r"@?\s*[Kk]?\s*(\d+)\s*@?", str(k).strip())
        if mm:
            norm[mm.group(1)] = v
        else:
            norm[str(k).strip()] = v

    def sub(m):
        return norm.get(m.group(1), m.group(0))

    return re.sub(r"@\s*[Kk]\s*(\d+)\s*@", sub, zh)


def main():
    segs = load_jsonl(WORK / "segments.jsonl")
    trans = {r["id"]: r for r in load_jsonl(WORK / "translations.jsonl")}

    ZH.mkdir(parents=True, exist_ok=True)
    QUALITY.mkdir(parents=True, exist_ok=True)

    by_doc = defaultdict(list)
    for s in segs:
        by_doc[s["doc"]].append(s)

    report = []
    total_seg = total_done = total_chars_src = total_chars_zh = 0
    bad_ph = []

    for doc, rows in sorted(by_doc.items()):
        rows.sort(key=lambda r: r["idx"])
        out_lines = []
        done = 0
        chars_src = chars_zh = 0
        for r in rows:
            t = trans.get(r["id"])
            src = r.get("source", "")
            if t and t.get("zh"):
                zh = restore_placeholders(t["zh"], r.get("protected_map", {}))
                out_lines.append(zh)
                done += 1
                chars_src += len(src)
                chars_zh += len(zh)
                if not t.get("placeholders_ok", True):
                    bad_ph.append(r["id"])
            else:
                out_lines.append(src)
        text = "\n\n".join(x for x in out_lines if x is not None)
        (ZH / f"{doc}.zh.md").write_text(text, encoding="utf-8")
        total_seg += len(rows)
        total_done += done
        total_chars_src += chars_src
        total_chars_zh += chars_zh
        report.append({
            "doc": doc, "segments": len(rows), "translated": done,
            "coverage_pct": round(100.0 * done / len(rows), 1) if rows else 0.0,
            "src_chars": len(src_join(rows)), "zh_chars": chars_zh,
        })

    cov = round(100.0 * total_done / total_seg, 1) if total_seg else 0.0
    lines = [
        "# 翻译覆盖度报告",
        "",
        f"- 文档数：{len(by_doc)}",
        f"- 段落总数：{total_seg}",
        f"- 已翻译段落：{total_done}",
        f"- **整体覆盖度：{cov}%**",
        f"- 已翻译源字符：{total_chars_src:,}",
        f"- 产出中文字符：{total_chars_zh:,}",
        f"- 占位符校验失败段：{len(bad_ph)}",
        "",
        "| 文档 | 段落 | 已译 | 覆盖度 | 源字符 | 中文字符 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in sorted(report, key=lambda x: x["coverage_pct"]):
        lines.append(
            f"| {r['doc']} | {r['segments']} | {r['translated']} | "
            f"{r['coverage_pct']}% | {r['src_chars']:,} | {r['zh_chars']:,} |"
        )
    if bad_ph:
        lines += ["", "## 占位符异常段落", ""] + [f"- {x}" for x in bad_ph]
    (QUALITY / "coverage.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"[done] 整体覆盖度 {cov}% | 中文产出 {total_chars_zh:,} 字符 | 见 quality/coverage.md")


def src_join(rows):
    return "".join(r.get("source", "") for r in rows)


if __name__ == "__main__":
    main()
