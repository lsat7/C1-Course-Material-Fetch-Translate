# -*- coding: utf-8 -*-
"""13 校对修正：对 dist/zh/*.zh.md 应用一轮可复核的人工校对修正（幂等，重复执行不会重复改动）。

修正规则（每一处改动都写入 quality/校对修正记录.md，可逐条回查）：
  R1 代码围栏：示例命令行被抽取成标题的，包进 ```bash 围栏（claude-code-best-practices）
  R2 标题残留符号：去掉标题尾部由原文锚点残留的孤立 '#'；原为 H1 的降为 H2（一篇文档只保留一个 H1）
  R3 重复标题：删除与同文件内前一个 H1 完全相同的 H1 行（网页 <title> 与正文标题重复造成的）
  R4 署名/站点名：作者名、博客名被抽取成 H1 的，降为普通段落
  R5 PDF 文件名标题：以文件名 slug 充当 H1 的，换成中文标题并合并紧随其后的重复标题行
  R6 围栏去重：合并相邻的重复围栏行，避免某条围栏规则被重复执行时把文档套成双层围栏

规则只作用于标题与围栏结构，不改动任何正文句子；若判断有误可用 git checkout 回滚单个文件。

用法：python tools/13_proofread_fixes.py                     # 应用并写记录
      python tools/13_proofread_fixes.py --dry-run           # 只打印会改什么，不落盘
      python tools/13_proofread_fixes.py --baseline 35bd874  # 从修正前的版本重放全部规则，
                                                             # 重建完整修正记录（不写 dist/zh）
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZH = ROOT / "dist" / "zh"
LOG = ROOT / "quality" / "校对修正记录.md"

MAX_BYLINE_LINE = 40

BYLINE = {
    "code-review-essentials.zh.md": ["# Blake Smith"],
    "copilot-prompt-injection-rce.zh.md": ["# Embrace The Red"],
    "mcp-food-for-thought.zh.md": ["# Reilly Wood"],
    "specs-are-the-new-source-code.zh.md": ["# Ravi on Product"],
}

SLUG_H1 = {
    "how-anthropic-uses-claude-code.zh.md": (
        "# how-anthropic-uses-claude-code",
        "# Anthropic 团队如何使用 Claude Code",
    ),
    "how-openai-uses-codex.zh.md": (
        "# how-openai-uses-codex",
        "# OpenAI 如何使用 Codex",
    ),
}

TRAILING_H = re.compile(r"^(#{1,6})\s+(.+?)#\s*$")
H1 = re.compile(r"^#\s+\S")
SHELL = re.compile(r"^(#|tail |claude |git )")


def fence_mask(lines):
    """逐行标记该行是否处于 ``` 围栏内部（围栏行本身也算受保护）。"""
    mask = []
    on = False
    for l in lines:
        if l.strip().startswith("```"):
            on = not on
            mask.append(True)
        else:
            mask.append(on)
    return mask


def r1_fence(lines, fname, notes):
    if fname != "claude-code-best-practices.zh.md":
        return lines
    mask = fence_mask(lines)
    for i, l in enumerate(lines):
        if mask[i]:
            continue  # 已在围栏内说明本处已修，跳过以保证幂等
        if l.strip() == "# Analyze recent log output":
            j = i
            while j < len(lines) and (lines[j].strip() == "" or SHELL.match(lines[j])):
                j += 1
            while j - 1 > i and lines[j - 1].strip() == "":
                j -= 1
            block = lines[i:j]
            notes.append(("R1 代码围栏", i + 1, "示例命令行 %d 行被抽取为标题" % len(block),
                          "整段包进 ```bash 围栏"))
            return lines[:i] + ["```bash"] + block + ["```"] + lines[j:]
    return lines


def r6_fence_dedup(lines, fname, notes):
    """合并相邻的重复围栏行（同型：开启型带语言 / 闭合型裸围栏）。

    防止某条围栏规则被重复执行时把文档套成双层围栏——那会让后半篇被渲染成代码块。
    """
    out = []
    for i, l in enumerate(lines):
        s = l.strip()
        if out and s.startswith("```") and out[-1].strip().startswith("```"):
            p = out[-1].strip()
            both_open = len(p) > 3 and len(s) > 3
            both_close = len(p) == 3 and len(s) == 3
            if both_open or both_close:
                notes.append(("R6 围栏去重", i + 1, l, "删除：与前一行重复的同型围栏（重复套壳产生）"))
                continue
        out.append(l)
    return out


def r2_trailing(lines, fname, notes):
    mask = fence_mask(lines)
    out = []
    for i, l in enumerate(lines):
        m = None if mask[i] else TRAILING_H.match(l)
        if m and m.group(2).strip():
            lv = len(m.group(1))
            newlv = 2 if lv == 1 else lv
            new = "#" * newlv + " " + m.group(2).strip()
            notes.append(("R2 标题残留符号", i + 1, l, new))
            out.append(new)
        else:
            out.append(l)
    return out


def r3_dups(lines, fname, notes):
    mask = fence_mask(lines)
    seen = set()
    drop = set()
    for i, l in enumerate(lines):
        if mask[i] or not H1.match(l):
            continue
        t = l.strip()
        if t in seen:
            drop.add(i)
            if i > 0 and i + 1 < len(lines) and lines[i - 1].strip() == "" and lines[i + 1].strip() == "":
                drop.add(i + 1)
        seen.add(t)
    if not drop:
        return lines
    out = []
    for i, l in enumerate(lines):
        if i in drop:
            notes.append(("R3 重复标题", i + 1,
                          l if l.strip() else "（空行）",
                          "删除：与同文件前一个 H1 完全重复"))
            continue
        out.append(l)
    return out


def r4_byline(lines, fname, notes):
    targets = set(BYLINE.get(fname, []))
    mask = fence_mask(lines)
    out = []
    for i, l in enumerate(lines):
        if i < MAX_BYLINE_LINE and not mask[i] and l.strip() in targets:
            new = l.strip()[2:].strip()
            notes.append(("R4 署名降级", i + 1, l, new + "（署名/站点名，降为普通段落）"))
            out.append(new)
        else:
            out.append(l)
    return out


def r5_slug(lines, fname, notes):
    if fname not in SLUG_H1:
        return lines
    old, new = SLUG_H1[fname]
    title = new[2:].strip()
    mask = fence_mask(lines)
    out = []
    for i, l in enumerate(lines):
        if not mask[i] and l.strip() == old:
            notes.append(("R5 PDF slug 标题", i + 1, l, new))
            out.append(new)
            continue
        if not mask[i] and l.strip() == title and out and out[-1].strip() == new:
            notes.append(("R5 PDF slug 标题", i + 1, l, "删除：与上方标题重复"))
            continue
        out.append(l)
    return out


def read_baseline(p, rev):
    """从某 git 版本读取该文件的原始文本，用于重放规则、重建完整记录。"""
    r = subprocess.run(["git", "show", "%s:dist/zh/%s" % (rev, p.name)],
                       cwd=str(ROOT), capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--baseline", default=None,
                    help="从该 git 版本（如 35bd874 / HEAD）重放规则并重建完整记录；不写 dist/zh")
    args = ap.parse_args()

    files = sorted(ZH.glob("*.zh.md"))
    all_notes = []
    changed_files = []
    mismatched = []
    for p in files:
        if args.baseline:
            original = read_baseline(p, args.baseline)
            if original is None:
                print("[skip] %s 在该版本中不存在" % p.name)
                continue
        else:
            original = p.read_text(encoding="utf-8")
        lines = original.split("\n")
        notes = []
        lines = r1_fence(lines, p.name, notes)
        lines = r6_fence_dedup(lines, p.name, notes)
        lines = r2_trailing(lines, p.name, notes)
        lines = r3_dups(lines, p.name, notes)
        lines = r4_byline(lines, p.name, notes)
        lines = r5_slug(lines, p.name, notes)
        new = "\n".join(lines)
        if notes:
            changed_files.append(p.name)
            for rule, ln, before, after in notes:
                all_notes.append((p.name, rule, ln, before, after))
        if args.baseline:
            if new != p.read_text(encoding="utf-8"):
                mismatched.append(p.name)
        elif new != original and not args.dry_run:
            p.write_text(new, encoding="utf-8")

    by_rule = {}
    for n in all_notes:
        by_rule[n[1]] = by_rule.get(n[1], 0) + 1

    print("[%s] 涉及 %d 个文件，共 %d 处修改" % ("dry-run" if args.dry_run else "applied",
                                                len(changed_files), len(all_notes)))
    for k in sorted(by_rule):
        print("  %-16s %d 处" % (k, by_rule[k]))
    for n in all_notes:
        print("  %s L%s  %s  ->  %s" % (n[0], n[2], n[3].replace("|", "\\|"), n[4].replace("|", "\\|")))

    if args.baseline:
        print("[baseline %s] 重放完成；与磁盘内容不一致的文件：%d 个" % (args.baseline, len(mismatched)))
        for m in mismatched:
            print("  !! %s" % m)

    if args.dry_run:
        return 0

    lines = []
    A = lines.append
    A("# 校对修正记录")
    A("")
    A("> 本文件由 `python tools/13_proofread_fixes.py` 生成，记录机器翻译落盘之后人工校对做过的每一处结构性修改。")
    A("> 规则只作用于标题与围栏结构，不改动任何正文句子；脚本幂等，重复执行不会重复改动。")
    A("> 记录可从修正前的版本重放重建（见文末复核方式），因此不依赖某一次运行的现场状态。")
    A("")
    A("| 规则 | 说明 | 处数 |")
    A("|---|---|---:|")
    A("| R1 代码围栏 | 示例命令行被抽取成标题，整段包进 ```bash 围栏 | %d |" % by_rule.get("R1 代码围栏", 0))
    A("| R2 标题残留符号 | 去掉标题尾部原文锚点残留的 `#`，H1 降为 H2 | %d |" % by_rule.get("R2 标题残留符号", 0))
    A("| R3 重复标题 | 删除与同文件前一个 H1 完全相同的标题行 | %d |" % by_rule.get("R3 重复标题", 0))
    A("| R4 署名降级 | 作者名/博客名被抽取成 H1，降为普通段落 | %d |" % by_rule.get("R4 署名降级", 0))
    A("| R5 PDF slug 标题 | 文件名 slug 充当 H1，换成中文标题 | %d |" % by_rule.get("R5 PDF slug 标题", 0))
    A("| R6 围栏去重 | 合并相邻同型重复围栏行（防止重复套壳） | %d |" % by_rule.get("R6 围栏去重", 0))
    A("")
    A("涉及 %d 个文件，合计 %d 处。" % (len(changed_files), len(all_notes)))
    A("")
    A("| 文件 | 规则 | 行号 | 修改前 | 修改后 |")
    A("|---|---|---:|---|---|")
    esc = lambda s: (s or "").replace("|", "\\|").replace("\n", " ")
    for f, rule, ln, before, after in all_notes:
        A("| `%s` | %s | %s | %s | %s |" % (f, rule, ln, esc(before), esc(after)))
    A("")
    A("---")
    A("")
    A("## 复核方式")
    A("")
    A("```powershell")
    A("python tools/13_proofread_fixes.py --dry-run   # 重新执行应输出 0 处修改（幂等）")
    A("python tools/13_proofread_fixes.py --baseline 35bd874   # 从修正前的版本重放规则，重建本记录")
    A("git diff --stat    # 查看本轮修正的实际改动量")
    A("```")

    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("[write] %s" % LOG)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
