<!-- source: pages/claude-code-best-practices.html -->

# Claude Code 概览 - Claude Code 文档

跳至主要内容

Claude Code 文档主页

英语

搜索...

⌘ K

询问 AI

搜索...

导航

快速开始

Claude Code 概述

快速开始

使用 Claude Code 构建

部署

管理

配置

参考

资源

##### 快速开始

概述

快速开始

更新日志

##### 核心概念

Claude Code 的工作原理

扩展 Claude Code

探索 .claude 目录

探索上下文窗口

##### 使用 Claude Code

存储指令与记忆

权限模式

常见工作流

最佳实践

##### 平台与集成

概览

远程控制

网页端 Claude Code

桌面端 Claude Code

Chrome 扩展（测试版）

计算机使用（预览版）

Visual Studio Code

JetBrains 系列 IDE

代码评审与 CI/CD

Slack 中的 Claude Code

本页内容

开始使用

你可以做什么

在各处使用 Claude Code

后续步骤

快速上手

# Claude Code 概览

复制页面

Claude Code 是一款智能体化编码工具，能够读取你的代码库、编辑文件、运行命令，并与你的开发工具集成。可在终端、IDE、桌面应用和浏览器中使用。

复制页面

Claude Code 是一款由 AI 驱动的编码助手，帮助你构建功能、修复缺陷并自动化开发任务。它能理解你的整个代码库，并可跨多个文件和工具协同工作，把事情办成。

## ​开始使用

选择你的环境即可开始。大多数使用界面需要 Claude 订阅或 Anthropic Console 账户。终端 CLI 与 VS Code 还支持第三方提供商。

终端

VS Code

桌面应用

Web

JetBrains

功能完备的 CLI，可直接在终端中使用 Claude Code。编辑文件、运行命令，从命令行管理整个项目。要安装 Claude Code，请使用以下方法之一：

原生安装（推荐）

Homebrew

WinGet

macOS、Linux、WSL：

curl -fsSL https://claude.ai/install.sh | bash

Windows PowerShell：

irm https: // claude.ai / install.ps1 | iex

Windows CMD：

curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd

如果你看到 token“&&”不是有效的语句分隔符，说明你当前在 PowerShell 中，而不是 CMD。请改用上面的 PowerShell 命令。在 PowerShell 中，你的 prompt 会显示为 PS C:\。Windows 需要 Git for Windows。如果尚未安装，请先安装。

原生安装会在后台自动更新，让你始终使用最新版本。

brew install --cask claude-code

Homebrew 安装不会自动更新。请定期运行 brew upgrade claude-code，以获取最新功能和安全修复。

winget install Anthropic.ClaudeCode

WinGet 安装不会自动更新。请定期运行 winget upgrade Anthropic.ClaudeCode，以获取最新功能和安全修复。

然后在任意项目中启动 Claude Code：

cd your-project
claude

首次使用时系统会提示你登录。就这么简单！继续阅读快速入门 →

有关安装选项、手动更新或卸载说明，请参阅高级设置。如果遇到问题，请访问故障排除。

VS Code 扩展可直接在编辑器中提供内联差异、@ 提及、计划评审和对话历史。

为 VS Code 安装

为 Cursor 安装

或者在扩展视图中搜索“Claude Code”（Mac 上为 Cmd+Shift+X，Windows/Linux 上为 Ctrl+Shift+X）。安装后，打开命令面板（Cmd+Shift+P / Ctrl+Shift+P），输入“Claude Code”，然后选择“在新标签页中打开”。开始使用 VS Code →

一款独立应用，用于运行 Claude Code，可在你的 IDE 或终端之外使用。以可视方式审查差异，并排运行多个会话，安排周期性任务，并启动云端会话。下载并安装：

macOS（Intel 和 Apple Silicon）

Windows（x64）

Windows ARM64（仅限远程会话）

安装后，启动 Claude，登录，然后点击 Code 标签页开始编码。需要付费订阅。详细了解桌面应用 →

无需本地设置，即可在浏览器中运行 Claude Code。启动长时间运行的任务，完成后再回来查看；处理本地没有的仓库，或并行运行多个任务。可在桌面浏览器和 Claude iOS 应用中使用。前往 claude.ai/code 开始编码。在网页端开始使用 →

适用于 IntelliJ IDEA、PyCharm、WebStorm 及其他 JetBrains IDE 的插件，支持交互式 diff 查看和选区上下文共享。从 JetBrains Marketplace 安装 Claude Code 插件，然后重启你的 IDE。开始使用 JetBrains →

## 你可以做什么

以下是使用 Claude Code 的一些方式：

自动化那些你一直拖延的工作

Claude Code 能处理那些耗掉你一整天时间的繁琐任务：为没有测试的代码编写测试、修复整个项目的 lint 错误、解决合并冲突、更新依赖项，以及撰写发布说明。

claude "write tests for the auth module, run them, and fix any failures"

构建功能并修复缺陷

用平实的语言描述你的需求。Claude Code 会规划实现方案、跨多个文件编写代码并验证其可用性。对于缺陷，粘贴错误信息或描述现象即可。Claude Code 会在你的代码库中追踪问题、定位根因并实施修复。更多示例参见常见工作流。

创建提交与拉取请求

Claude Code 直接与 git 协作。它会暂存变更、撰写 commit 信息、创建分支并开启拉取请求。

claude "commit my changes with a descriptive message"

在 CI 中，你可以借助 GitHub Actions 或 GitLab CI/CD 自动完成代码评审与议题分诊。

用 MCP 连接你的工具

模型上下文协议（Model Context Protocol，MCP）是一个开放标准，用于把 AI 工具连接到外部数据源。借助 MCP，Claude Code 可以读取你放在 Google Drive 里的设计文档、更新 Jira 中的工单、从 Slack 拉取数据，或者使用你自己定制的工具。

通过指令、技能与钩子进行定制

CLAUDE.md 是一个放在项目根目录的 markdown 文件，Claude Code 会在每次会话开始时读取它。你可以用它来设定编码规范、架构决策、偏好的库以及评审清单。Claude 在工作的同时还会自动构建记忆，跨会话保存构建命令、调试经验等所得，而你什么都不用写。创建自定义命令，可以把团队可共享的重复性工作流打包起来，例如 /review-pr 或 /deploy-staging。钩子（hooks）让你能在 Claude Code 执行动作之前或之后运行 shell 命令，比如每次编辑文件后自动格式化，或者在 commit 之前运行 lint。

运行智能体团队并构建自定义智能体

同时启动多个 Claude Code 智能体，让它们并行处理同一任务的不同部分。由一个主控智能体协调工作、分配子任务并合并结果。对于完全自定义的工作流，Agent SDK 让你能够构建由 Claude Code 的工具与能力驱动的自有智能体，并完全掌控编排、工具访问与权限。

用 CLI 实现管道、脚本与自动化

Claude Code 可组合，并遵循 Unix 哲学。把日志通过管道传给它，在 CI 中运行它，或者把它与其他工具串联起来：

# Analyze recent log output
tail -200 app.log | claude -p "Slack me if you see any anomalies"

# Automate translations in CI
claude -p "translate new strings into French and raise a PR for review"

# Bulk operations across files
git diff main --name-only | claude -p "review these changed files for security issues"

完整的命令与参数列表见 CLI 参考文档。

安排周期性任务

按计划运行 Claude，自动完成重复性工作：早晨的 PR 评审、夜间 CI 失败分析、每周依赖审计，或在 PR 合并后同步文档。

云端定时任务运行在由 Anthropic 管理的基础设施上，因此即使你的电脑关机也能持续运行。可从网页端、桌面应用创建，也可在 CLI 中运行 /schedule 来创建。

桌面端定时任务在你的机器上运行，可直接访问本地文件和工具

/loop 会在 CLI 会话中重复 prompt，以实现快速轮询

随时随地工作

会话不再绑定到单一界面。随着上下文变化，可在不同环境之间迁移工作：

离开办公桌，也能通过 Remote Control 从手机或任意浏览器继续工作

用 Message Dispatch 从手机发送任务，并打开它创建的桌面端会话

在网页端或 iOS 应用上启动长时间运行的任务，然后用 claude --teleport 将其拉入终端

用 /desktop 将终端会话交接给桌面应用，以便进行可视化的 diff 评审

从团队聊天中分派任务：在 Slack 里提及 @Claude 并附上缺陷报告，就能拿回一个拉取请求

## ​随处使用 Claude Code

每个界面都连接到同一个底层 Claude Code 引擎，因此你的 CLAUDE.md 文件、设置和 MCP 服务器在所有界面上都通用。除了上面的 Terminal、VS Code、JetBrains、Desktop 和 Web 环境之外，Claude Code 还与 CI/CD、聊天和浏览器工作流集成：

我想…… 最佳选择

从我的手机或其他设备继续本地会话 Remote Control

将来自 Telegram、Discord、iMessage 或我自己的 webhook 的事件推送到会话中 Channels

在本地启动任务，在移动端继续 Web 或 Claude iOS 应用

按周期性计划运行 Claude 云端计划任务或 Desktop 计划任务

自动化 PR 评审和问题分类 GitHub Actions 或 GitLab CI/CD

对每个 PR 获取自动代码评审 GitHub Code Review

将来自 Slack 的缺陷报告转成拉取请求 Slack

调试实时 Web 应用 Chrome

为你自己的工作流构建自定义智能体 Agent SDK

## ​后续步骤

安装 Claude Code 之后，这些指南可以帮你更进一步。

快速入门：走完你的第一个真实任务，从探索代码库到 commit 一个修复

存储指令与记忆：通过 CLAUDE.md 文件和自动记忆，为 Claude 提供持久化指令

常见工作流与最佳实践：充分发挥 Claude Code 价值的模式

设置：按你的工作流定制 Claude Code

故障排查：常见问题的解决方案

code.claude.com：演示、定价与产品详情

本页面对你有帮助吗？

是

快速入门

⌘ I

助手

回复由 AI 生成，可能包含错误。