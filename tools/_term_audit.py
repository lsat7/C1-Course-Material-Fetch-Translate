# -*- coding: utf-8 -*-
"""术语一致性审计：对验收要点点名的三词（Vibe Coding / Scaffolding / Context Engineering，
另加 context rot 作对照组）在 dist/zh/*.zh.md 全量译文中做逐篇落地核对。"""
import re, pathlib, collections

root = pathlib.Path(__file__).resolve().parent.parent
zh_dir = root / "dist" / "zh"
src_dir = root / "work" / "extracted"

def n(text, pat):
    return len(re.findall(pat, text, re.I))

SRC_PAT = {
    "vibe": r"Vibe\s*Coding",
    "scf":  r"scaffold",
    "ce":   r"context\s+engineering",
    "cr":   r"context\s+rot",
}
ZH_PAT = {
    "vibe":     r"Vibe\s*Coding",           # 术语表 #87：保留英文原形
    "vibe_bad": r"氛围编程|感觉编程|凭感觉编程|随意编程|随性编程|氛围式编程",
    "scf":      r"脚手架",                   # 术语表 #4
    "scf_bad":  r"代码支架|代码骨架",
    "ce":       r"上下文工程",                # 术语表 #5
    "ce_bad":   r"语境工程|情境工程|上下文工程学",
    "cr":       r"上下文腐化",                # 术语表 #7
    "cr_bad":   r"上下文腐烂|上下文退化|语境腐化",
}

rows = []
violations = []
agg_s = collections.Counter()
agg_z = collections.Counter()

for src in sorted(src_dir.glob("*.src.md")):
    name = src.name.replace(".src.md", "")
    zf = zh_dir / (name + ".zh.md")
    if not zf.exists():
        continue
    ts = src.read_text(encoding="utf-8", errors="replace")
    tz = zf.read_text(encoding="utf-8", errors="replace")
    s = {k: n(ts, p) for k, p in SRC_PAT.items()}
    z = {k: n(tz, p) for k, p in ZH_PAT.items()}
    agg_s.update(s); agg_z.update(z)
    rows.append((name, s, z))

    if s["scf"] and not z["scf"]:
        violations.append((name, "Scaffolding 源文出现 %d 次、译文无「脚手架」" % s["scf"]))
    if s["ce"] and not z["ce"]:
        violations.append((name, "Context Engineering 源文出现 %d 次、译文无「上下文工程」" % s["ce"]))
    if s["vibe"] and not z["vibe"]:
        violations.append((name, "Vibe Coding 源文出现 %d 次、译文未保留英文原形" % s["vibe"]))
    for key, label in (("vibe_bad", "Vibe Coding"), ("ce_bad", "Context Engineering"),
                       ("scf_bad", "Scaffolding"), ("cr_bad", "Context rot")):
        if z[key]:
            violations.append((name, "%s 出现术语表外变体 %d 处" % (label, z[key])))

print("===== 全局计数（译文篇数 %d） =====" % len(rows))
print("  源文 Vibe Coding            =", agg_s["vibe"], " 译文保留英文原形 =", agg_z["vibe"])
print("  源文 scaffold*              =", agg_s["scf"],  " 译文「脚手架」   =", agg_z["scf"])
print("  源文 context engineering    =", agg_s["ce"],   " 译文「上下文工程」=", agg_z["ce"])
print("  源文 context rot            =", agg_s["cr"],   " 译文「上下文腐化」=", agg_z["cr"])
print("  术语表外变体（应为 0）：vibe=%d  scf=%d  ce=%d  cr=%d"
      % (agg_z["vibe_bad"], agg_z["scf_bad"], agg_z["ce_bad"], agg_z["cr_bad"]))

print()
print("===== 逐篇对照（源 vs 译文） =====")
print("%-48s %5s %5s %6s %6s %5s %8s %5s %6s" %
      ("doc", "VC源", "VC译", "scf源", "脚手架", "CE源", "上下文工程", "CR源", "腐化"))
for name, s, z in rows:
    print("%-48s %5d %5d %6d %6d %5d %8d %5d %6d" %
          (name, s["vibe"], z["vibe"], s["scf"], z["scf"], s["ce"], z["ce"], s["cr"], z["cr"]))

print()
print("===== 一致性违规清单 =====")
if violations:
    for v in violations:
        print("  x", v[0], "->", v[1])
else:
    print("  0 违规：三词在全部译文中与术语表唯一对应，无变体、无误译、无漏译")

covtxt = (root / "quality" / "coverage.md").read_text(encoding="utf-8", errors="replace")
m = re.search(r"整体覆盖度：([\d.]+)%", covtxt)
tot = len(list(zh_dir.glob("*.zh.md")))
print()
print("===== 覆盖度 =====")
print("  段落级覆盖度 =", (m.group(1) + "%") if m else "?")
print("  dist/zh 文档数 =", tot, "；其中含源文可对照的译文 =", len(rows))
