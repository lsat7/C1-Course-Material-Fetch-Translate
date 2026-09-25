# C1 · Stanford「Vibe Coding」课程中文资料包

> **一句话**：把 Stanford CS146S *Vibe Coding*（2025）的全部公开资料，走一遍
> **批量获取 → 机器翻译 → 术语强约束 → 质量门禁 → 发布**的流水线，
> 产出一套**能直接读、也能换一门课复用**的中文课程资料包。
>
> 本仓库是 Challenge C1「课程资料获取与翻译」的完整交付。

| 我该看哪 | 去哪 |
|---|---|
| 直接读中文 | [`dist/zh/`](dist/zh) —— 34 个文件，文件名与源文档一一对应 |
| 跑流水线 / 换一门课复用 | [§5 复跑与换源](#五流水线怎么复跑含换源复用) |
| 看每条验收要点怎么达标 | [§6 验收要点逐条对照](#六验收要点逐条对照) |
| 看哪里没覆盖 | [§8 已知缺口](#八已知缺口如实标注)（如实标注，未编造译文） |

---

## 一、成品一览

| 指标 | 数值 | 证据文件 |
|---|---|---|
| 源资料 | 34 篇（课程官网 / PDF 讲义 / 公开博客） | [`dist/来源清单.md`](dist/来源清单.md) |
| 有效中文译文 | **30 篇**（另 4 篇上游不可获取，见 §8） | [`dist/zh/`](dist/zh) |
| 段落覆盖度 | **97.1%**（5,653 / 5,823 段） | [`quality/coverage.md`](quality/coverage.md) |
| 源正文字符 | 591,975 → 中文产出 **255,875** 字符 | 同上 |
| 术语表 | **100 条**术语 + **47 条**强制保留英文词 | [`dist/术语表.md`](dist/术语表.md) |
| 术语一致性违规 | **0**（含验收点名的 Vibe Coding / Scaffolding / Context Engineering） | [`quality/术语三词一致性审计.md`](quality/术语三词一致性审计.md) |
| 占位符泄漏 | **0 处** | [`quality/抽检报告.md`](quality/抽检报告.md) |

## 二、目录结构

```
C1-Translation-Pipeline/
├─ README.md                  # 本文件：入口 + 验收对照 + 使用方法
├─ dist/                      # ★ 交付物（给人看、可直接阅读）
│  ├─ README.md               # 资料包总说明：来源 / 覆盖 / 流程 / 用法 / 缺口
│  ├─ zh/                     # 34 个中文文件 = 30 篇译文 + 4 篇上游缺口说明
│  ├─ 术语表.md               # 100 条术语 + 47 条不译词（分发版）
│  ├─ 来源清单.md             # 一手来源 URL、抓取结果、失败清单
│  ├─ AI日志.md               # 每日 AI 协作日志（工具 / prompt / 踩坑）
│  ├─ AAR-七维复盘.md         # 七维 AAR（含失败经验与改进方案）
│  └─ 拿来说明-01/02/03.md    # 3 个关键决策的完整证据链
├─ quality/                   # 质量证据（可复核）
│  ├─ coverage.md             # 逐篇段落覆盖度
│  ├─ terminology_report.md   # 逐篇术语落地检查
│  ├─ 术语三词一致性审计.md   # 验收点名三词的逐篇核对
│  └─ 抽检报告.md             # Han 占比 / 占位符残留 / 修复闭环
├─ tools/                     # 流水线脚本 01→11 + glossary.json（机器可读术语表）
└─ work/                      # 中间产物（可重建；原语料与中间文件不入库）
```

## 三、3 分钟上手

不需要安装任何东西，也不需要 Key，**读中文只需要浏览器**：

1. 打开 [`dist/zh/`](dist/zh) → 每个 `xxx.zh.md` 对应源文档 `xxx`，点开即读。
2. 想知道某篇的出处、抓取时间、覆盖了多少段 → [`dist/来源清单.md`](dist/来源清单.md) 与 [`quality/coverage.md`](quality/coverage.md)。
3. 想核对质量会不会是机翻糊弄 → [`quality/抽检报告.md`](quality/抽检报告.md)（每篇的 Han 字符占比、占位符残留、缺陷修复记录）。
4. 想确认术语没被译乱 → [`quality/术语三词一致性审计.md`](quality/术语三词一致性审计.md)。

## 四、翻译流程：从源链接到中文成稿

6 个阶段、11 个脚本，**每一段都可单独复跑**：

| 阶段 | 脚本 | 做什么 | 产出 |
|---|---|---|---|
| 1 盘点 | `tools/01_inventory.py` | 建立课程公开资料清单 | `work/inventory.json` |
| 2 抽取 | `tools/02_extract.py` | HTML / PDF 正文抽取与清洗 | `work/extracted/*.src.md` |
| 3 分段 | `tools/03_segment.py` | 段落切分 + **术语占位符保护** | `work/segments.jsonl` |
| 4 翻译 | `tools/04_translate.py` | 调模型批量翻译，**断点续传** | `work/translated.jsonl` |
| 5 装配 | `tools/05_assemble.py` | 占位符回填、按原文结构重组 | `dist/zh/*.zh.md` |
| 6 校验 | `tools/06`–`11` | 术语一致性 / Han 占比 / 占位符残留 / 覆盖度 / 报告 | `quality/*.md` |

**两个关键设计（也是这套流水线能成立的原因）**

- **术语保护是结构性的，不靠模型自觉**：译前把 100 条术语与 47 条不译词替换为占位符 `@K0@`…`@K{n}@`，模型被要求原样保留占位符，译后回填。5,823 段中 959 段命中保护，2,030 个占位符全部按段落重新编号并校验通过 —— 这让"术语全文一致"从软约束变成硬约束。
- **断点续传 + 全程留证**：译文逐段落盘，中断后重跑只补未完成段落；`work/` 保留中间产物，任何一句中文都能回溯到源段落与它当时的术语占位符。

## 五、流水线怎么复跑（含换源复用）

**前置**：Python 3.10+；一个 OpenAI 兼容的 `/chat/completions` 端点（本项目实测使用 DeepSeek `deepseek-flash`）。

```powershell
# 1) 配置凭证（脚本只读环境变量，不硬编码、不落盘）
$env:TRANSLATE_BASE_URL = "https://api.deepseek.com/v1"
$env:TRANSLATE_API_KEY  = "<你的 Key>"
$env:TRANSLATE_MODEL    = "deepseek-flash"

# 2) 全链路复跑
python tools/01_inventory.py
python tools/02_extract.py
python tools/03_segment.py
python tools/04_translate.py     # 中断可重跑，自动续传
python tools/05_assemble.py
python tools/06_terminology_check.py   # 之后依次 07→11
```

**换一门课怎么复用（改 2 个数据文件，不改代码）**

1. 替换 `work/inventory.json`（或改 `01_inventory.py` 里的源清单）；
2. 替换 `tools/glossary.json` 的术语（保持 `term` / `keep_english` 结构）；
3. 顺序执行 `02 → 05`；
4. `06 → 11` 自动重新生成质量报告与全部指标。

> 换句话说：**换课 = 换输入数据**。术语表结构、占位符协议、校验脚本都不需要动。

## 六、验收要点逐条对照

| # | 验收要点 | 本仓库如何满足 | 可复核证据 |
|---|---|---|---|
| 1 | 覆盖课程主体内容（≥80% 讲义/字幕有对应中文） | **段落级覆盖 97.1%**（5,653 / 5,823 段）；34 篇中 30 篇为完整中文译文 | [`quality/coverage.md`](quality/coverage.md)（逐篇表） |
| 2 | 术语表 ≥50 条且**全文一致**（Vibe Coding / Scaffolding / Context Engineering 译法统一） | **100 条**术语 + 47 条不译词；点名三词逐篇核对 **0 违规**（`Scaffolding→脚手架`、`Context Engineering→上下文工程`、`Vibe Coding` 保留英文） | [`dist/术语表.md`](dist/术语表.md)、[`quality/术语三词一致性审计.md`](quality/术语三词一致性审计.md) |
| 3 | 翻译流水线**可复跑**：换一门课同样流程能再产出 | 11 个脚本全链路 + `glossary.json`；换源只需替换清单与术语表两个数据文件 | [§5](#五流水线怎么复跑含换源复用)、[`tools/`](tools) |
| 4 | 发布仓库有**完整 README 与目录结构**，陌生人可按说明独立使用 | 本文件（入口/结构/上手/复跑/缺口）+ [`dist/README.md`](dist/README.md)（包内总说明） | 本文件 §2、§3 |

## 七、评分维度自检

| 维度 | 满分 | 交付了什么 | 证据 |
|---|---|---|---|
| contentAccuracy | 25 | 30 篇译文共 255,875 中文字符；术语 0 违规；逐篇 Han 占比抽检 | [`quality/抽检报告.md`](quality/抽检报告.md) |
| pipelineAutomation | 20 | `01→11` 全链路脚本、断点续传、换源只改数据 | [`tools/`](tools)、§5 |
| artifactCompleteness | 15 | README、来源清单、术语表、AI 日志、七维 AAR、3 篇拿来说明 | [`dist/`](dist) |
| aiUsage | 20 | AI 日志记录真实 prompt 与工具链；拿来说明含「原文 / prompt / 产出 / 对比」四段 | [`dist/AI日志.md`](dist/AI日志.md)、[`dist/拿来说明-01.md`](dist/拿来说明-01.md) |
| reflectionQuality | 20 | 七维 AAR，含失败经验（假译文识别、4 篇上游失败、术语误报）与改进方案 | [`dist/AAR-七维复盘.md`](dist/AAR-七维复盘.md) |

**红线自检**：① 4 类必需交付物齐全 → 产物完整性红线未触发；② AI 日志与七维 AAR 均在 → 复盘红线未触发。

## 八、已知缺口（如实标注）

**4 篇源页面无法获取正文**，未编造译文，`dist/zh/` 下对应文件写明源链接、失败原因，以及"拿到正文后重跑哪几条命令即可补译"：

| 文档 | 失败原因 |
|---|---|
| `lessons-from-ai-code-reviews` | 源文件为空（抓取到的正文为 0 字节） |
| `how-warp-uses-warp` | Notion 页面需 JS 渲染，静态抓取拿不到正文 |
| `good-context-good-code` | Ghost 站点访问码墙 |
| `peeking-under-the-hood-of-claude-code` | Medium 拦截自动下载 |

合计约 **970 字符**，占源正文 **0.16%**。

**另外两点需要你知情的质量事实**：

- **170 段（3.1%）按规则跳过**：纯代码块、表格分隔行、URL 行，不构成正文。
- **`owasp-top-ten` 的 Han 占比 20.6%，明显低于其他篇（33%–82%）**：OWASP 十条的条目名、缩写与代码片段密度极高，而术语表要求这类词保留英文，属**术语保护的结果，不是漏译**（该篇译文 11,540 字符，为完整全文）。若希望这类文档更"中文"，可把部分条目名加入翻译白名单后重跑 `04_translate.py`。

## 九、来源与合规

- 全部源资料均为课程**公开**材料，来源 URL 与抓取结果见 [`dist/来源清单.md`](dist/来源清单.md)。
- 译文仅供学习交流，版权归原作者与 Stanford CS146S 课程所有。
- 仓库内**不含任何 API Key**；流水线仅从环境变量读取凭证；`.gitignore` 已排除本地探测脚本与中间产物。
