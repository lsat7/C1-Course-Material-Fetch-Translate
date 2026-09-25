#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
01_inventory.py — C1 课程资料获取管线：语料盘点

功能：扫描课程离线镜像目录，统计每个来源文件可提取正文的字符量，
输出 corpus_inventory.json / corpus_inventory.md，作为覆盖率分母的基线。

用法：
    python tools/01_inventory.py --src "<课程离线镜像根目录>" --out "<输出目录>"
"""
import argparse
import json
import os
import re
import sys

TEXT_EXT_OK = {".html", ".htm", ".md", ".txt", ".json"}


def strip_html(raw: str) -> str:
    """剥离 script/style/标签，返回可读正文。"""
    body = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.S | re.I)
    body = re.sub(r"<style\b.*?</style>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    body = re.sub(r"<(br|/p|/div|/li|/h[1-6])\s*/?>", "\n", body, flags=re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"&nbsp;", " ", body)
    body = re.sub(r"&amp;", "&", body)
    body = re.sub(r"&lt;", "<", body)
    body = re.sub(r"&gt;", ">", body)
    body = re.sub(r"&quot;", '"', body)
    body = re.sub(r"[ \t\u00a0]+", " ", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="课程离线镜像根目录")
    ap.add_argument("--out", required=True, help="输出目录")
    args = ap.parse_args()

    src = os.path.abspath(args.src)
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)

    items = []
    for root, _dirs, files in os.walk(src):
        for fn in sorted(files):
            path = os.path.join(root, fn)
            ext = os.path.splitext(fn)[1].lower()
            rel = os.path.relpath(path, src).replace("\\", "/")
            size = os.path.getsize(path)
            rec = {
                "path": rel,
                "ext": ext,
                "bytes": size,
                "text_chars": 0,
                "status": "skipped",
                "note": "",
            }
            if ext in TEXT_EXT_OK:
                try:
                    raw = open(path, encoding="utf-8", errors="ignore").read()
                except OSError as exc:
                    rec["status"] = "error"
                    rec["note"] = f"read failed: {exc}"
                    items.append(rec)
                    continue
                text = strip_html(raw) if ext in {".html", ".htm"} else raw
                rec["text_chars"] = len(text)
                if rec["text_chars"] >= 200:
                    rec["status"] = "translatable"
                elif rec["text_chars"] > 0:
                    rec["status"] = "tiny"
                    rec["note"] = "正文过短（可能为 JS 渲染壳页），需人工确认"
                else:
                    rec["status"] = "empty"
                    rec["note"] = "无可提取正文"
            elif ext == ".pdf":
                rec["status"] = "pdf-deferred"
                rec["note"] = "PDF 正文由 02_extract.py 单独处理"
            items.append(rec)

    translatable = [i for i in items if i["status"] == "translatable"]
    total_chars = sum(i["text_chars"] for i in translatable)

    summary = {
        "source_root": src,
        "files_total": len(items),
        "translatable_files": len(translatable),
        "translatable_chars": total_chars,
        "empty_or_tiny": [
            {"path": i["path"], "status": i["status"], "note": i["note"]}
            for i in items
            if i["status"] in {"empty", "tiny"}
        ],
        "pdfs": [i["path"] for i in items if i["status"] == "pdf-deferred"],
        "items": items,
    }

    with open(os.path.join(out, "corpus_inventory.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)

    lines = [
        "# 语料盘点（corpus_inventory）",
        "",
        f"- 来源根目录：`{src}`",
        f"- 文件总数：{len(items)}",
        f"- 可翻译文件数：{len(translatable)}",
        f"- 可翻译正文字符总量：{total_chars:,}",
        "",
        "| 文件 | 大小(KB) | 正文字符 | 状态 | 备注 |",
        "|---|---:|---:|---|---|",
    ]
    for i in items:
        lines.append(
            f"| `{i['path']}` | {i['bytes'] // 1024} | {i['text_chars']:,} | {i['status']} | {i['note']} |"
        )
    with open(os.path.join(out, "corpus_inventory.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"files={len(items)} translatable={len(translatable)} chars={total_chars}")
    print(f"-> {os.path.join(out, 'corpus_inventory.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
