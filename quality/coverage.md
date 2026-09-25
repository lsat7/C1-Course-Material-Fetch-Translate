# 覆盖度与字符指标

> 由 `tools/12_metrics.py` 从当前产物重算生成，可用 `python tools/12_metrics.py` 随时刷新。
> 数据源：`work/segments.jsonl`（分段与翻译状态）、`dist/zh/*.zh.md`（当前译文）、`work/corpus_inventory.json`（盘点口径）。

## 一、口径说明（三个数字不要混用）

| 口径 | 数值 | 含义 | 来源 |
|---|---|---|---|
| 源正文·盘点口径 | 591,975 字符 | 01 盘点时 34 篇抽取正文中“可翻译正文”的字符数（已剔除代码块、纯链接行） | `work/corpus_inventory.json` |
| 源正文·分段口径 | 633,993 字符 | 03 分段后实际提交给模型的翻译单元字符数（含标题行与列表标记，故略大于盘点口径） | `work/segments.jsonl` |
| 译文文本 | 270,210 字符（其中汉字 151,643） | 当前 `dist/zh/*.zh.md` 的字符总数与其中汉字数 | `dist/zh/` |

汉字占比只用于“是否为真中文”的粗筛：术语表要求保留英文的不译词、代码片段、专有名词都会拉低该比例，
因此**占比高低不等于翻译质量高低**，逐篇数值见下表。

## 二、总览

| 指标 | 数值 |
|---|---|
| 源文档数 | 34 篇（其中 4 篇上游不可获取，见 `dist/zh/*.zh.md` 内的缺口说明） |
| 段落总数 | 5,823 段 |
| 待译段落 | 5,653 段（另 170 段按规则跳过：纯代码块 / 表格分隔行 / URL 行） |
| 已翻译段落 | 5,653 段 |
| 段落覆盖度 | **97.1%** |
| 译文文本字符 | 270,210 |
| 其中汉字 | 151,643 |

## 三、逐篇明细（按汉字占比升序）

| 文档 | 待译段落 | 源字符（分段口径） | 译文文本字符 | 汉字数 | 汉字占比 |
|---|---:|---:|---:|---:|---:|
| `owasp-top-ten` | 185 | 16,454 | 11,540 | 2,374 | 20.6% |
| `peeking-under-the-hood-of-claude-code` | 6 | 397 | 746 | 189 | 25.3% |
| `lessons-from-ai-code-reviews` | 1 | 56 | 634 | 181 | 28.5% |
| `mcp-server-authentication` | 171 | 13,640 | 8,373 | 2,503 | 29.9% |
| `how-warp-uses-warp` | 4 | 141 | 720 | 219 | 30.4% |
| `good-context-good-code` | 8 | 175 | 937 | 297 | 31.7% |
| `prompt-engineering-guide` | 144 | 2,797 | 1,586 | 607 | 38.3% |
| `claude-code-best-practices` | 154 | 9,922 | 5,337 | 2,168 | 40.6% |
| `warp-vs-claude-code` | 111 | 5,360 | 2,694 | 1,270 | 47.1% |
| `mcp-food-for-thought` | 77 | 5,346 | 2,716 | 1,307 | 48.1% |
| `ai-assisted-code-review-assessment` | 53 | 53,172 | 23,013 | 11,128 | 48.4% |
| `prompt-engineering-overview` | 1383 | 55,188 | 25,996 | 12,678 | 48.8% |
| `observability-basics` | 178 | 12,516 | 5,962 | 3,010 | 50.5% |
| `context-rot` | 408 | 50,450 | 21,833 | 11,735 | 53.7% |
| `finding-vulnerabilities-claude-codex` | 258 | 25,145 | 11,098 | 6,134 | 55.3% |
| `mcp-registry-preview` | 32 | 5,724 | 2,471 | 1,383 | 56.0% |
| `agentic-ai-threats` | 593 | 50,833 | 20,770 | 11,759 | 56.6% |
| `kubernetes-troubleshooting-ai` | 85 | 9,671 | 4,200 | 2,415 | 57.5% |
| `copilot-prompt-injection-rce` | 81 | 7,593 | 3,366 | 1,943 | 57.7% |
| `mcp-introduction` | 177 | 31,019 | 12,538 | 7,503 | 59.8% |
| `ai-code-review-best-practices` | 240 | 14,273 | 5,570 | 3,586 | 64.4% |
| `code-reviews-just-do-it` | 45 | 5,683 | 2,167 | 1,397 | 64.5% |
| `how-anthropic-uses-claude-code` | 77 | 74,528 | 27,665 | 17,939 | 64.8% |
| `multi-agent-systems-ai-native` | 91 | 14,384 | 5,680 | 3,693 | 65.0% |
| `how-openai-uses-codex` | 20 | 12,818 | 5,078 | 3,311 | 65.2% |
| `specs-are-the-new-source-code` | 125 | 13,094 | 5,537 | 3,638 | 65.7% |
| `writing-effective-tools-for-agents` | 122 | 22,172 | 8,650 | 5,741 | 66.4% |
| `sast-vs-dast` | 198 | 20,875 | 7,474 | 4,974 | 66.6% |
| `benefits-agentic-ai-oncall` | 65 | 7,180 | 2,696 | 1,846 | 68.5% |
| `how-long-contexts-fail` | 60 | 10,109 | 3,988 | 2,762 | 69.3% |
| `how-to-review-code-effectively` | 156 | 23,062 | 8,598 | 6,238 | 72.6% |
| `devin-coding-agents-101` | 147 | 21,668 | 7,819 | 5,839 | 74.7% |
| `sre-introduction` | 134 | 26,611 | 8,786 | 6,612 | 75.3% |
| `code-review-essentials` | 64 | 11,937 | 3,972 | 3,264 | 82.2% |

---

## 四、这份报告怎么复核

```powershell
python tools/12_metrics.py      # 重算本文件，数字应与上表一致
python tools/06_terminology_check.py   # 术语落地检查
python tools/08_verify.py              # 汉字占比门禁（阈值 >25%）
```
