#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
02_extract.py — C1 获取管线第二阶段：语料正文提取与归档

把课程离线镜像中的 HTML / PDF / Markdown 统一抽取为可翻译的纯文本，
并为每个来源生成 <slug>.src.md（保留标题层级与段落边界），
供 03_translate.py 分段消费。换一门课程只需改 --src。

用法：
    python tools/02_extract.py --src "<课程镜像根>" --out "<构建目录>"
"""
import argparse
import hashlib
import html as htmllib
import json
import os
import re
import sys
from datetime import datetime, timezone

# 这些页面在离线镜像中是占位页或 JS 渲染壳页，正文不可得。
# 判定阈值：剥离标签后正文字符 < 200。
MIN_BODY_CHARS = 200

BLOCK_TAGS = r"p|div|section|article|li|h[1-6]|blockquote|pre|tr|br"


def sha16(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def html_to_markdown(raw: str) -> tuple:
    """极简 HTML→结构化文本。返回 (标题, 正文文本)。只保留可读正文。"""
    title = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", raw, flags=re.S | re.I)
    if m:
        title = htmllib.unescape(re.sub(r"\s+", " ", m.group(1))).strip()

    # 去掉不可读区块
    body = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.S | re.I)
    body = re.sub(r"<style\b.*?</style>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<nav\b.*?</nav>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<footer\b.*?</footer>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<head\b.*?</head>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)

    # 标题层级转 markdown，保留结构
    body = re.sub(
        r"<h([1-6])[^>]*>(.*?)</h\1>",
        lambda m: "\n\n" + "#" * int(m.group(1)) + " " + re.sub(r"<[^>]+>", "", m.group(2)).strip() + "\n\n",
        body,
        flags=re.S | re.I,
    )
    # 段落/换行边界
    body = re.sub(r"<(%s)[^>]*>" % BLOCK_TAGS, "\n\n", body, flags=re.I)
    body = re.sub(r"</(%s)>" % BLOCK_TAGS, "\n\n", body, flags=re.I)
    # 链接保留文字，图片丢弃
    body = re.sub(r"<img[^>]*>", " ", body, flags=re.I)
    body = re.sub(r"<a[^>]*>(.*?)</a>", r"\1", body, flags=re.S | re.I)
    body = re.sub(r"<[^>]+>", " ", body)

    body = htmllib.unescape(body)
    body = re.sub(r"[ \t\u00a0]+", " ", body)
    body = re.sub(r" *\n *", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return title, body.strip()


def extract_pdf(path: str) -> tuple:
    """优先 PyMuPDF，回退 pdfplumber。返回 (页数, 文本, 每页字符数)。"""
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(path)
        pages = []
        for page in doc:
            pages.append(page.get_text("text"))
        n = doc.page_count
        doc.close()
        return n, "\n\n".join(pages), [len(p) for p in pages]
    except ImportError:
        pass
    try:
        import pdfplumber

        pages = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
        return len(pages), "\n\n".join(pages), [len(p) for p in pages]
    except ImportError:
        return -1, "", []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="课程离线镜像根目录")
    ap.add_argument("--out", required=True, help="构建输出目录")
    args = ap.parse_args()

    src = os.path.abspath(args.src)
    out = os.path.abspath(args.out)
    pages_out = os.path.join(out, "extracted")
    os.makedirs(pages_out, exist_ok=True)

    manifest = {
        "source_root": src,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "entries": [],
    }

    search_dirs = []
    for sub in ("pages", "pdfs"):
        p = os.path.join(src, sub)
        if os.path.isdir(p):
            search_dirs.append((sub, p))

    total_chars = 0
    for kind, d in search_dirs:
        for fn in sorted(os.listdir(d)):
            path = os.path.join(d, fn)
            if not os.path.isfile(path):
                continue
            ext = os.path.splitext(fn)[1].lower()
            slug = os.path.splitext(fn)[0]
            raw = open(path, "rb").read()
            rec = {
                "source": f"{kind}/{fn}",
                "slug": slug,
                "kind": kind,
                "ext": ext,
                "bytes": len(raw),
                "sha256_16": sha16(raw),
                "status": "ok",
                "text_chars": 0,
                "pages": None,
            }
            if ext in {".html", ".htm"}:
                title, body = html_to_markdown(raw.decode("utf-8", errors="ignore"))
                rec["title"] = title
                rec["text_chars"] = len(body)
                if len(body) < MIN_BODY_CHARS:
                    rec["status"] = "placeholder_or_shell"
                    rec["note"] = "正文不足 200 字符：反爬占位页或 JS 渲染壳页，不计入覆盖率分母"
                else:
                    total_chars += len(body)
                with open(os.path.join(pages_out, slug + ".src.md"), "w", encoding="utf-8") as fh:
                    fh.write(f"<!-- source: {kind}/{fn} -->\n\n# {title}\n\n{body}\n")
            elif ext == ".pdf":
                n, text, per = extract_pdf(path)
                rec["pages"] = n
                rec["text_chars"] = len(text)
                rec["empty_pages"] = sum(1 for c in per if c < 20)
                if n < 0:
                    rec["status"] = "needs_ocr"
                    rec["note"] = "无可用 PDF 文本提取库，需 OCR 或安装 PyMuPDF"
                elif rec["text_chars"] < MIN_BODY_CHARS:
                    rec["status"] = "needs_ocr"
                    rec["note"] = "文本层为空，疑似扫描件"
                else:
                    total_chars += rec["text_chars"]
                with open(os.path.join(pages_out, slug + ".src.md"), "w", encoding="utf-8") as fh:
                    fh.write(f"<!-- source: {kind}/{fn} pages={n} -->\n\n# {slug}\n\n{text}\n")
            else:
                rec["status"] = "skipped"
            manifest["entries"].append(rec)

    manifest["translatable_chars"] = total_chars
    manifest["translatable_entries"] = sum(1 for e in manifest["entries"] if e["status"] == "ok")
    with open(os.path.join(out, "extract_manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)

    print(f"extracted entries={len(manifest['entries'])} translatable={manifest['translatable_entries']} chars={total_chars}")
    for e in manifest["entries"]:
        flag = "  " if e["status"] == "ok" else "!!"
        print(f"{flag} {e['source']:52s} {e['status']:22s} {e['text_chars']:>7,} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
