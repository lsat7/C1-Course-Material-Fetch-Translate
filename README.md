# C1 — Stanford Vibe Coding 课程资料获取与翻译

> Challenge C1 交付仓库：把 Stanford CS146S「Vibe Coding」(2025) 的公开课程资料
> 全量获取、机器翻译、术语强约束、质量门禁，产出一套可复用的**中文课程资料包**。

## 📦 交付物在哪

面向读者的完整说明与成品都在 **`dist/`**：

| 文件 | 内容 |
|---|---|
| [`dist/README.md`](dist/README.md) | **总说明**：来源、覆盖范围、翻译流程、使用方法、已知缺口 |
| [`dist/zh/`](dist/zh) | 34 篇中文译文（对应 30 篇有效源文档 + 4 篇上游不可获取占位） |
| [`dist/术语表.md`](dist/术语表.md) | 100 条术语 + 47 条强制保留英文词 |
| [`dist/来源清单.md`](dist/来源清单.md) | 一手来源、语料盘点、上游抓取失败清单 |
| [`dist/AI日志.md`](dist/AI日志.md) | 每日 AI 协作日志（工具 / prompt / 踩坑） |
| [`dist/AAR-七维复盘.md`](dist/AAR-七维复盘.md) | 七维 AAR 复盘 |
| [`dist/拿来说明-01…03.md`](dist) | 3 个关键决策的完整证据链（原文 / prompt / 产出 / 对比） |

## 🔧 流水线与质量证据

- `tools/01→11`：盘点 → 抽取 → 分段（术语占位符保护）→ 机翻 → 回填 → 术语校验 → Han 门禁 → 补译 → 交付物生成 → 抽检报告。**换一门课只需改资料路径与 `glossary.json`。**
- `quality/`：`coverage.md`（逐篇段落覆盖度）、`terminology_report.md`（逐篇术语落地）、`抽检报告.md`（Han 占比 / 占位符残留 / 缺陷修复闭环）。

## 📊 关键指标

| 覆盖度 | 中文产出 | 术语表 | 占位符泄漏 |
|---|---|---|---|
| **97.1%**（5653/5823 段） | 255,875 字符 | 100 条 | 0 处 |

## ⚠️ 已知缺口（如实标注）

`how-warp-uses-warp`（Notion 需 JS）、`good-context-good-code`（Ghost 访问码墙）、
`peeking-under-the-hood-of-claude-code`（Medium 拦截）、`lessons-from-ai-code-reviews`（源文件为空）
—— 4 篇正文在镜像中无法获取，合计约占源正文 0.16%，**未编造译文**。详见 `dist/来源清单.md`。

## 快速上手

```powershell
# 只想看中文 → 直接读 dist/zh/
# 想复跑流水线 → 见 dist/README.md 第三节（模型密钥仅经环境变量注入，仓库不含任何凭据）
```
