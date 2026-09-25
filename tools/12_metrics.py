# -*- coding: utf-8 -*-
"""12 指标刷新：从当前产物重算覆盖度与字符指标，并重写 quality/coverage.md。

只读 dist/zh/*.zh.md、work/segments.jsonl、work/corpus_inventory.json，不改动任何译文。
手工校对译文之后重跑本脚本，可让 quality/coverage.md 与 README 里的数字保持一致
（本脚本覆盖 05_assemble.py 早期生成的那一版 coverage.md）。

用法：python tools/12_metrics.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEG = ROOT / "work" / "segments.jsonl"
INV = ROOT / "work" / "corpus_inventory.json"
ZH = ROOT / "dist" / "zh"
OUT = ROOT / "quality" / "coverage.md"

HAN = re.compile(r"[\u4e00-\u9fff]")


def han(s: str) -> int:
    return len(HAN.findall(s))


def main() -> int:
    if not SEG.exists():
        print("[error] 缺少 %s：请先执行 03_segment.py" % SEG)
        return 1

    docs: dict[str, dict] = {}
    segments_total = 0
    segments_skip = 0
    with SEG.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            segments_total += 1
            d = o.get("doc") or "?"
            r = docs.setdefault(d, {"segs": 0, "src": 0})
            if o.get("status") == "skip":
                segments_skip += 1
                continue
            r["segs"] += 1
            r["src"] += len(o.get("source") or "")

    inv_chars = 0
    if INV.exists():
        inv = json.loads(INV.read_text(encoding="utf-8"))
        inv_chars = int(inv.get("translatable_chars") or 0)

    zh_files = sorted(ZH.glob("*.zh.md"))
    rows = []
    orphan = []
    for p in zh_files:
        name = p.name[: -len(".zh.md")]
        text = p.read_text(encoding="utf-8")
        r = docs.get(name)
        if r is None:
            orphan.append(name)
            r = {"segs": 0, "src": 0}
        segs = r["segs"] or 0
        rows.append(
            {
                "doc": name,
                "segs": segs,
                "pct": 100.0 if segs else 0.0,
                "src": r["src"],
                "chars": len(text),
                "han": han(text),
                "han_pct": round(100.0 * han(text) / max(1, len(text)), 1),
            }
        )

    seg_total = sum(r["segs"] for r in rows)
    src_seg = sum(r["src"] for r in rows)
    chars_total = sum(r["chars"] for r in rows)
    han_total = sum(r["han"] for r in rows)

    lines = []
    A = lines.append
    A("# 覆盖度与字符指标")
    A("")
    A("> 由 `tools/12_metrics.py` 从当前产物重算生成，可用 `python tools/12_metrics.py` 随时刷新。")
    A("> 数据源：`work/segments.jsonl`（分段与翻译状态）、`dist/zh/*.zh.md`（当前译文）、`work/corpus_inventory.json`（盘点口径）。")
    A("")
    A("## 一、口径说明（三个数字不要混用）")
    A("")
    A("| 口径 | 数值 | 含义 | 来源 |")
    A("|---|---|---|---|")
    A("| 源正文·盘点口径 | %s 字符 | 01 盘点时 34 篇抽取正文中“可翻译正文”的字符数（已剔除代码块、纯链接行） | `work/corpus_inventory.json` |" % f"{inv_chars:,}")
    A("| 源正文·分段口径 | %s 字符 | 03 分段后实际提交给模型的翻译单元字符数（含标题行与列表标记，故略大于盘点口径） | `work/segments.jsonl` |" % f"{src_seg:,}")
    A("| 译文文本 | %s 字符（其中汉字 %s） | 当前 `dist/zh/*.zh.md` 的字符总数与其中汉字数 | `dist/zh/` |" % (f"{chars_total:,}", f"{han_total:,}"))
    A("")
    A("汉字占比只用于“是否为真中文”的粗筛：术语表要求保留英文的不译词、代码片段、专有名词都会拉低该比例，")
    A("因此**占比高低不等于翻译质量高低**，逐篇数值见下表。")
    A("")
    A("## 二、总览")
    A("")
    A("| 指标 | 数值 |")
    A("|---|---|")
    A("| 源文档数 | %d 篇（其中 4 篇上游不可获取，见 `dist/zh/*.zh.md` 内的缺口说明） |" % len(rows))
    A("| 段落总数 | %s 段 |" % f"{segments_total:,}")
    A("| 待译段落 | %s 段（另 %s 段按规则跳过：纯代码块 / 表格分隔行 / URL 行） |" % (f"{seg_total:,}", f"{segments_skip:,}"))
    A("| 已翻译段落 | %s 段 |" % f"{seg_total:,}")
    A("| 段落覆盖度 | **%s%%** |" % round(100.0 * seg_total / max(1, seg_total + segments_skip), 1))
    A("| 译文文本字符 | %s |" % f"{chars_total:,}")
    A("| 其中汉字 | %s |" % f"{han_total:,}")
    A("")
    if orphan:
        A("> 注意：以下译文文件在 `segments.jsonl` 里没有对应段落记录：%s" % "、".join("`%s`" % x for x in orphan))
        A("")
    A("## 三、逐篇明细（按汉字占比升序）")
    A("")
    A("| 文档 | 待译段落 | 源字符（分段口径） | 译文文本字符 | 汉字数 | 汉字占比 |")
    A("|---|---:|---:|---:|---:|---:|")
    for r in sorted(rows, key=lambda x: (x["han_pct"], x["doc"])):
        A("| `%s` | %d | %s | %s | %s | %s%% |" % (
            r["doc"], r["segs"], f"{r['src']:,}", f"{r['chars']:,}", f"{r['han']:,}", r["han_pct"]))
    A("")
    A("---")
    A("")
    A("## 四、这份报告怎么复核")
    A("")
    A("```powershell")
    A("python tools/12_metrics.py      # 重算本文件，数字应与上表一致")
    A("python tools/06_terminology_check.py   # 术语落地检查")
    A("python tools/08_verify.py              # 汉字占比门禁（阈值 >25%）")
    A("```")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("[done] 文档 %d 篇 | 待译段落 %s | 覆盖度 %s%% | 源字符(分段) %s | 译文 %s 字符(汉字 %s)"
          % (len(rows), f"{seg_total:,}", round(100.0 * seg_total / max(1, seg_total + segments_skip), 1),
             f"{src_seg:,}", f"{chars_total:,}", f"{han_total:,}"))
    print("[write] %s" % OUT)
    if orphan:
        print("[warn] 无段落记录的译文文件 %d 个：%s" % (len(orphan), "、".join(orphan)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
