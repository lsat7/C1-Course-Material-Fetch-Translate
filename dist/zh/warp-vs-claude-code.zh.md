<!-- source: pages/warp-vs-claude-code.html -->

# Warp 与 Oz 入门 | Warp

circle-info

隆重推出 Oz：面向云端智能体的编排平台。

了解更多。 arrow-up-right

close

bars

Warp

search

circle-xmark

⌘ Ctrl k

Warp

入门

Warp 与 Oz 入门

快速开始 chevron-right

迁移到 Warp

支持的 shell

键盘快捷键

终端

经典输入

块 chevron-right

现代文本编辑 chevron-right

命令输入 chevron-right

命令补全 chevron-right

会话管理 chevron-right

窗口管理 chevron-right

终端外观 chevron-right

Warpify 概览 chevron-right

更多功能 chevron-right

命令面板

终端对比 chevron-right

终端功能

终端集成

代码

代码概览

内置代码编辑器 chevron-right

代码评审面板

Git Worktrees

通过 SSH 使用的功能支持

知识与协作

Warp Drive 概览 chevron-right

团队管理

团队管理面板

会话共享

chevron-up chevron-down

gitbook 由 GitBook 提供支持

xmark

block-quote 本页内容 chevron-down

copy 复制 chevron-down

# Warp 与 Oz 入门

从 Warp——智能体化开发环境（Agentic Development Environment）——以及 Oz，即面向云智能体的编排平台开始。

Warp 是一个智能体化开发环境，它将现代终端与强大的智能体结合在一起，帮助你构建、测试、部署和调试代码。Warp 的 AI 由 Oz 驱动，这是面向云智能体的编排平台。

Warp 将现代终端与 Oz——面向云智能体的编排平台——融为一体

## hashtagWarp

Warp 就是你的工作场所——一个为与智能体协作编码而打造的快速、现代终端。

核心能力：

智能体模式 arrow-up-right：在用于执行命令的简洁终端与面向多轮智能体工作流的专属对话视图之间切换。

现代终端体验：Cursor 移动、基于块的导航、多行编辑、语法高亮和丰富的自动补全。使用 Rust 构建，性能出色。

代码编辑器：文件树、支持 LSP 的代码编辑器，以及交互式代码评审体验。

编码智能体集成 arrow-up-right：具备语音输入、用于处理基于终端的图像的 @-selection 等功能。兼容 Oz 或 Claude Code、Codex 等智能体。

深入了解 Warp 的核心功能

## hashtagOz：面向云智能体的编排平台

Oz 是面向云智能体的编排平台，为 Warp 的全部智能功能提供支持。Oz 旨在规模化地协调智能体——理解你的代码库、自主执行任务，并适应你的工作流。Oz 在设计上就支持多模型，让你可以灵活地为每项任务选择最合适的 LLM。

Oz 有两种运行模式：

### 本地智能体

直接在 Warp 应用中运行，获得实时、交互式的编码辅助。

在整个代码库中编写和重构代码

调试问题并修复错误

运行命令并解读结果

规划并执行多步骤任务

本地智能体让你始终掌控全局。你可以查看变更、在任务进行中引导智能体，并在操作执行前进行批准。

→ 开始使用本地智能体 arrow-up-right

### 云端智能体

Oz 云端智能体在 Warp 的基础设施（或你自己的基础设施）上后台运行，以实现规模化自动化。

触发器：React 来自 Slack、Linear、GitHub 或自定义 webhook 的事件

计划任务：运行依赖项更新或死代码清理等周期性任务

并行化：跨仓库或任务并发运行多个智能体

可观测性：每次运行都可追踪、可审计，并可与团队共享

云智能体适合那些不需要你即时关注的工作，比如 PR 评审、问题分诊、例行维护，以及由集成驱动的工作流。

→ 了解云智能体 arrow-up-right

## hashtag它们如何协同工作

Warp 和 Oz 在本地与云端开发中提供统一的体验：

同一个智能体，随处可用：无论你是在 Warp 中交互式地工作，还是在云端运行智能体，使用的都是同一套底层智能体能力。

无缝交接：在云端启动任务，当你想要亲自掌控时，可在 Warp 中于本地接手，而不会丢失进度或上下文。

共享上下文：Warp Drive、Rules arrow-up-right 以及 MCP 服务器 arrow-up-right 在本地和云端智能体上均可使用，因此团队的知识与工具始终可用。

团队协作：共享智能体会话、评审智能体的操作、引导正在运行的任务，无论任务由谁发起。

## hashtag多模型支持

Oz 在设计上支持多模型。你可以从一组精选的顶级模型中，选择自己偏好的 LLM arrow-up-right。

## hashtag隐私与安全

Warp 符合 SOC 2 合规要求，并与所有签约的 LLM 供应商实行零数据保留（Zero Data Retention）政策。不会保留、存储客户 AI 数据，也不会将其用于训练。

Warp 的 AI 功能可在「设置 > AI」中全局禁用。

→ 详细了解数据隐私 arrow-up-right

## hashtag后续步骤

快速开始指南：安装 Warp 并开始编码

本地智能体概览 arrow-up-right：探索 Warp 中提供的全部 AI 功能

云端智能体概览 arrow-up-right：配置后台自动化

Oz 平台 arrow-up-right：了解 CLI、API、SDK 以及基础设施

下一页 快速开始 chevron-right

最后更新于 3 天前

这有帮助吗？

Warp

Oz：面向云端智能体的编排平台

本地智能体

云端智能体

它们如何协同工作

多模型支持

隐私与安全

后续步骤

这篇内容对你有帮助吗？

阳光般明亮的桌面月亮

阳光般明亮的桌面月亮