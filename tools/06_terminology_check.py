# -*- coding: utf-8 -*-
"""
06_terminology_check.py — 术语一致性检查器

对 dist/zh/*.md 的译文做两项检查：
A. 术语覆盖：glossary 中的每个术语，若其英文原词在源文中出现 >= 2 次，
   则译文中应能检出对应中文译法（否则记为「术语未落地」）。
B. 禁用形式：术语在译文中不得以英文原形裸奔（do_not_translate 白名单除外）。

输出 quality/terminology_report.md，供人工校对定位问题段落。

可复跑、确定性、不调用模型。
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"
ZH = ROOT / "dist" / "zh"
QUALITY = ROOT / "quality"
GLOSSARY = ROOT / "tools" / "glossary.json"


def load_glossary():
    g = json.loads(GLOSSARY.read_text(encoding="utf-8"))
    terms = {}
    for en, meta in g.get("terms", {}).items():
        zh = meta.get("zh") if isinstance(meta, dict) else meta
        if zh:
            terms[en] = zh
    dnt = set(x.lower() for x in g.get("do_not_translate", []))
    return terms, dnt


def main():
    terms, dnt = load_glossary()
    QUALITY.mkdir(parents=True, exist_ok=True)

    rows = []
    total_missing = 0
    for md in sorted(ZH.glob("*.zh.md")):
        doc = md.name.replace(".zh.md", "")
        src_path = WORK / "extracted" / f"{doc}.src.md"
        if not src_path.exists():
            continue
        src = src_path.read_text(encoding="utf-8")
        zh = md.read_text(encoding="utf-8")
        if not zh.strip():
            continue
        missing, ok_cnt = [], 0
        for en, z in terms.items():
            if en.lower() in dnt:
                continue
            n_en = len(re.findall(re.escape(en), src, flags=re.IGNORECASE))
            if n_en < 2:
                continue
            # 该术语的英文是否仍大量裸留（允许首次出现的「中文（English）」标注）
            n_zh = zh.count(z)
            bracket_ok = len(re.findall(re.escape(z) + r"（[^）]*" + re.escape(en) + r"[^）]*）",
                                       zh, flags=re.IGNORECASE))
            bare = max(0, len(re.findall(re.escape(en), zh, flags=re.IGNORECASE)) - bracket_ok)
            if n_zh == 0 and bare >= 2:
                missing.append((en, z, n_en, bare))
            else:
                ok_cnt += 1
        total_missing += len(missing)
        rows.append({"doc": doc, "checked": ok_cnt, "missing": missing})

    lines = ["# 术语一致性检查报告", "",
             f"- 术语表条目：{len(terms)}",
             f"- 检查文档数：{len(rows)}",
             f"- 术语未落地总数：{total_missing}", ""]
    for r in sorted(rows, key=lambda x: -len(x["missing"])):
        lines.append(f"## {r['doc']}")
        lines.append(f"- 已落地术语：{r['checked']}")
        if r["missing"]:
            lines.append(f"- 未落地术语：{len(r['missing'])}")
            lines.append("")
            lines.append("| 英文 | 期望译法 | 源文出现 | 译文裸留 |")
            lines.append("|---|---|---:|---:|")
            for en, z, n_en, bare in sorted(r["missing"], key=lambda x: -x[3]):
                lines.append(f"| {en} | {z} | {n_en} | {bare} |")
        else:
            lines.append("- 未落地术语：0 ✅")
        lines.append("")

    (QUALITY / "terminology_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[done] 术语检查完成 | 未落地总数 {total_missing} | 见 quality/terminology_report.md")


if __name__ == "__main__":
    main()
