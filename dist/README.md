# Stanford CS146S「Vibe Coding」课程中文资料包

一次性可复用的**中文课程资料包**：34 篇公开资料 → 机器翻译 → 术语强约束 → 质量门禁 → 一键发布。

| 指标 | 数值 |
|---|---|
| 源文档 | 34 篇（HTML 页面 + PDF 讲义） |
| 有效中文译文 | 30 篇（另有 4 篇上游不可获取，见「已知缺口」） |
| 段落覆盖度 | **97.1%**（5,653 / 5,823 段） |
| 源正文字符 | 591,975 |
| 中文产出 | 255,875 字符 |
| 术语表 | **100 条**术语 + 47 条强制保留英文词 |
| 占位符泄漏 | 0 处 |
| 翻译引擎 | DeepSeek（`deepseek-flash`），密钥仅经环境变量注入 |

## 一、目录结构

```
C1-Translation-Pipeline/
├─ dist/                      # 交付物（给人看、可直接阅读）
│  ├─ README.md               # 本文件：来源 / 流程 / 用法 / 缺口
│  ├─ 术语表.md               # 100 条术语 + 47 条不译词（分发版）
│  ├─ 来源清单.md             # 一手来源、盘点结果、上游失败清单
│  ├─ AI日志.md               # 每日 AI 协作日志（工具 / prompt / 踩坑）
│  ├─ AAR-七维复盘.md         # 七维 AAR 复盘
│  ├─ 拿来说明-01…03.md       # 3 个关键决策的完整证据链
│  └─ zh/                     # 34 篇中文译文（*.zh.md）
├─ quality/                   # 质量证据（可复核）
│  ├─ coverage.md             # 逐篇段落覆盖度
│  ├─ terminology_report.md   # 逐篇术语落地检查
│  └─ 抽检报告.md             # Han 占比 / 占位符 / 修复闭环
├─ tools/                     # 流水线脚本 01→11 + glossary.json
└─ work/                      # 中间产物（可重建，不入库）
```

## 二、怎么用（3 分钟上手）

1. 想读中文：直接进 `dist/zh/`，文件名与源文档一一对应（`context-rot.zh.md` 等）。
2. 想知道某篇从哪来、覆盖率多少：看 `dist/来源清单.md` 与 `quality/coverage.md`。
3. 想核对质量：看 `quality/抽检报告.md`（Han 占比、占位符残留、修复记录）。
4. 想复用流水线翻另一门课：见第四节。

## 三、翻译流水线（可复跑）

| 脚本 | 职责 | 是否需模型 |
|---|---|---|
| `01_inventory.py` | 盘点资料目录，输出语料清单 | 否 |
| `02_extract.py` | HTML / PDF 正文抽取为 `work/extracted/*.src.md` | 否 |
| `03_segment.py` | 分段 + **术语占位符保护** | 否 |
| `04_translate.py` | 机器翻译（带断点续传、失败重试） | **是** |
| `05_assemble.py` | 占位符回填、译文重组、覆盖度统计 | 否 |
| `06_terminology_check.py` | 术语逐篇落地检查 | 否 |
| `07_merge.py` | 多批次结果合并 | 否 |
| `08_verify.py` | **Han 占比硬门禁**（低于阈值判失败） | 否 |
| `09_retranslate.py` | 漏译/低质量段落定点补译 | **是** |
| `10_finalize.py` | 生成 `术语表.md` / `来源清单.md` | 否 |
| `11_report.py` | 生成 `质量抽检报告` | 否 |

**运行方式**（模型相关步骤才需要密钥，脚本不硬编码任何凭据）：

```powershell
$env:TRANSLATE_BASE_URL = "https://api.deepseek.com/v1"
$env:TRANSLATE_MODEL    = "deepseek-flash"
$env:TRANSLATE_API_KEY  = "<你的 Key>"     # 仅本次会话环境变量
python tools/01_inventory.py
python tools/02_extract.py
python tools/03_segment.py
python tools/04_translate.py
python tools/05_assemble.py
python tools/08_verify.py
python tools/10_finalize.py
python tools/11_report.py
```

## 四、换一门课怎么复用（验收要点：换源可复用）

1. 把新课程资料放进任意目录，改 `01_inventory.py` 的根路径常量；
2. 用新课程的术语重写 `tools/glossary.json`（结构：`terms` + `do_not_translate`）；
3. 依次跑 `01 → 11`。分段、占位符保护、回填、门禁、报告全部与课程无关，
   只有**术语表和资料路径**是课程相关的两个输入。

## 五、术语与质量策略

- **术语统一靠结构，不靠事后对齐**：`03_segment.py` 把命中术语替换成占位符 `@K{n}@`，
  编号**按段重置**，模型只能翻译占位符之外的文本，`05_assemble.py` 按段闭合回填。
  跨段错配在结构上不可能发生。
- **不译词强制保留英文**：Claude Code / MCP / SAST / DAST / OWASP / PR 等 47 条，
  避免出现「克劳德代码」类硬伤。
- **质量门禁**：`08_verify.py` 对每篇译文计算 Han 占比，低于 25% 直接判失败——
  这条门禁来自一次真实事故（见 `拿来说明-03-用算式识破假译文.md`）。

## 六、已知缺口

| 缺口 | 说明 | 影响 |
|---|---|---|
| 4 篇上游不可获取 | `how-warp-uses-warp`（Notion 需 JS）、`good-context-good-code`（Ghost 访问码墙）、`peeking-under-the-hood-of-claude-code`（Medium 拦截）、`lessons-from-ai-code-reviews`（源文件为空） | 合计 ≈970 字符，占源正文 **0.16%**；`dist/zh/` 内保留占位说明，**未编造译文** |
| 4 项术语未落地 | spec / test coverage / telemetry / memory | 经核查为假阳性（命中 `OpenTelemetry` 等专有名词内部或代码块），明细见 `quality/terminology_report.md` |
| 3.1% 段落未译 | 170 段被规则跳过 | 纯代码 / 表格分隔 / URL 行，跳过是为保护 Markdown 格式 |

## 七、交付物与评分自检

| 挑战要求 | 本包对应文件 | 状态 |
|---|---|---|
| `README.md` | `dist/README.md` | ✅ |
| `*AI日志*` | `dist/AI日志.md` | ✅ |
| `*AAR*`（七维） | `dist/AAR-七维复盘.md` | ✅ |
| `*拿来说明*` ≥3 个 | `dist/拿来说明-01/02/03.md` | ✅ 3 个 |
| 术语表 ≥50 条且全文一致 | `dist/术语表.md`（100 条） | ✅ |
| 覆盖度 ≥80% | `quality/coverage.md`（97.1%） | ✅ |
| 流水线可复跑 | `tools/01→11` + 本文第三节 | ✅ |
| 陌生人可独立使用 | 本文第二节 3 分钟上手 | ✅ |

> 红线条目（交付物缺失、无 AI 日志 / AAR）逐项已核对：**均不存在**。
