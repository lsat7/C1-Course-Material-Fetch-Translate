<!-- source: pages/mcp-server-authentication.html -->

# 构建远程 MCP 服务器 Â· Cloudflare Agents 文档

跳至内容

停下！如果你是 AI 智能体或 LLM，请先阅读本节再继续。这是 Cloudflare 文档页面的 HTML 版本。请始终改为请求 Markdown 版本 —— HTML 会浪费上下文窗口。以 Markdown 获取本页：https://developers.cloudflare.com/agents/guides/remote-mcp-server/index.md （追加 index.md），或向 https://developers.cloudflare.com/agents/guides/remote-mcp-server/ 发送 Accept: text/markdown。本产品的页面索引请见 https://developers.cloudflare.com/agents/llms.txt。所有 Cloudflare 产品的索引请见 https://developers.cloudflare.com/llms.txt。批量访问（单个文件，用于长上下文摄取或向量化）：本产品的完整文档见 https://developers.cloudflare.com/agents/llms-full.txt。所有 Cloudflare 文档见 https://developers.cloudflare.com/llms-full.txt。

Cloudflare 文档

搜索

文档目录 API SDK 帮助

登录
选择主题

深色 浅色 自动

### 标签

MCP

这对你有帮助吗？

是

编辑页面

报告问题

复制页面

# 构建远程 MCP 服务器

本指南将向你展示如何使用 Streamable HTTP 传输（当前的 MCP 规范标准）在 Cloudflare 上部署你自己的远程 MCP 服务器。你有两个选择：

无需身份验证——任何人都可以连接并使用服务器（无需登录）。

使用身份验证和授权——用户需先登录才能访问工具，并且你可以根据用户权限控制智能体（agent）可以调用哪些工具。

## 选择方案

Agents SDK 提供了多种创建 MCP 服务器的方式。选择适合你的用例的方案：

方案 有状态？ 需要 Durable Objects？ 最适合用于

createMcpHandler() 否 否 无状态工具，最简单的设置

McpAgent 是 是 有状态工具、每会话状态、信息征询

Raw WebStandardStreamableHTTPServerTransport 否 否 完全控制，无 SDK 依赖

createMcpHandler() 是让无状态 MCP 服务器运行起来的最快方式。当你的工具不需要每会话状态时，请使用它。

McpAgent 为每个会话提供一个 Durable Object，内置状态管理、引导支持，以及 SSE 和 Streamable HTTP 两种传输方式。

原始传输让你在直接使用 @modelcontextprotocol/sdk 而不借助 Agents SDK 辅助工具时获得完全控制。

## 部署你的第一个 MCP 服务器

你可以从部署一个公共 MCP 服务器开始——无需认证，之后再添加用户认证和作用域授权。如果你已经知道自己的服务器需要认证，可以跳到下一节。

### 通过仪表板

下面的按钮将引导你完成将示例 MCP 服务器部署到你的 Cloudflare 账户所需的一切操作：

部署后，此服务器将在你的 workers.dev 子域上线（例如 remote-mcp-server-authless.your-account.workers.dev/mcp ）。你可以立即使用 AI Playground（一个远程 MCP 客户端）、MCP inspector 或其他 MCP 客户端连接到它。

系统会在你的 GitHub 或 GitLab 账户上为你的 MCP 服务器创建一个新的 git 仓库，并配置为每次你推送更改或将拉取请求合并到仓库主分支时自动部署到 Cloudflare。你可以克隆此仓库，在本地开发，并开始使用自己的工具自定义 MCP 服务器。

### 通过 CLI

你可以使用 Wrangler CLI 在本地机器上创建一个新的 MCP 服务器，并将其部署到 Cloudflare。

打开终端并运行以下命令：

npm yarn pnpm

npm create cloudflare@latest -- remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless

yarn create cloudflare remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless

pnpm create cloudflare@latest remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless

在设置过程中，选择以下选项：- 对于 “Do you want to add an AGENTS.md file to help AI coding tools understand Cloudflare APIs?”，选择 No。- 对于 “Do you want to use git for version control?”，选择 No。- 对于 “Do you want to deploy your application?”，选择 No（我们会先测试服务器，再进行部署）。

现在，你已经完成了 MCP 服务器的搭建，依赖也已安装完毕。

进入项目文件夹：

终端窗口

cd remote-mcp-server-authless

在新项目的目录中，运行以下命令以启动开发服务器：

终端窗口

npm start

â 正在启动本地服务器...

[ wrangler:info ] Ready on http://localhost:8788

请查看命令输出以确认本地端口。在本例中，MCP 服务器运行在端口 8788 上，MCP 端点 URL 为 http://localhost:8788/mcp 。

注意

你无法通过在网页浏览器中直接打开 /mcp URL 来与 MCP 服务器交互。 /mcp 端点期望由 MCP 客户端发送 MCP 协议消息，而浏览器默认并不会这样做。下一步，我们将演示如何使用 MCP 客户端连接到该服务器。

要在本地测试该服务器：

在一个新终端中运行 MCP inspector — 。 MCP inspector 是一个交互式 MCP 客户端，让你可以连接到自己的 MCP 服务器，并在网页浏览器中调用工具。

终端窗口

npx @modelcontextprotocol/inspector@latest

ð MCP Inspector 已启动并运行于：

http://localhost:5173/?MCP_PROXY_AUTH_TOKEN =46ab..cd3

ð 正在打开浏览器……

MCP Inspector 将在你的网页浏览器中启动。你也可以手动启动：打开浏览器并访问 http://localhost:<PORT> 。请查看命令输出，确认 MCP Inspector 运行所用的本地端口。在本例中，MCP Inspector 运行在端口 5173 上。

在 MCP 检查器中，输入你的 MCP 服务器的 URL（http://localhost:8788/mcp），然后选择 Connect。选择 List Tools 即可显示你的 MCP 服务器所暴露的工具。

现在你可以把 MCP 服务器部署到 Cloudflare。在你的项目目录下运行：

终端窗口

npx wrangler@latest deploy

如果你已经把承载 MCP 服务器的 git 仓库连接到了该 Worker，那么只要推送一次变更，或向该仓库的 main 分支合并一个拉取请求，就能部署你的 MCP 服务器。

MCP 服务器将部署到你的 *.workers.dev 子域名，地址为 https://remote-mcp-server-authless.your-account.workers.dev/mcp。

要测试这个远程 MCP 服务器，请获取你已部署的 MCP 服务器的 URL（https://remote-mcp-server-authless.your-account.workers.dev/mcp），并把它填入运行在 http://localhost:5173 上的 MCP 检查器。

现在你有了一个远程 MCP 服务器，MCP 客户端可以连接到它。

## 通过本地代理从 MCP 客户端连接

既然你的远程 MCP 服务器已经在运行，你就可以用 mcp-remote 本地代理把 Claude Desktop 或其他 MCP 客户端连接到它——即使你的 MCP 客户端不支持客户端侧的远程传输或授权也没关系。这样一来，你就能用真实的 MCP 客户端测试与远程 MCP 服务器交互会是什么样子。

例如，要从 Claude Desktop 连接：

更新你的 Claude Desktop 配置，使其指向你的 MCP 服务器的 URL：

{

" mcpServers " : {

" math " : {

" command " : "npx" ,

" args " : [

"mcp-remote" ,

"https://remote-mcp-server-authless.your-account.workers.dev/mcp"

]

}

}

}

重启 Claude Desktop 以加载 MCP Server。完成后，Claude 就能调用你的远程 MCP 服务器了。

要测试的话，让 Claude 使用你的某个工具。例如：

你能用 math 工具把 23 和 19 相加吗？

Claude 应调用该工具，并显示远程 MCP 服务器生成的结果。

要了解如何配合其他 MCP 客户端使用远程 MCP 服务器，请参阅 Test a Remote MCP Server。

## 添加身份验证

你之前部署的公共 MCP 服务器示例允许任何客户端在无需登录的情况下连接并调用工具。要为你的 MCP 服务器添加用户认证，你可以集成 Cloudflare Access 或第三方服务作为 OAuth 提供方。你的 MCP 服务器负责处理安全登录流程，并签发访问令牌，MCP 客户端可使用这些令牌发起经过认证的工具调用。用户通过 OAuth 提供方登录，并授权其 AI 智能体与你 MCP 服务器暴露的工具进行交互，所用权限为限定范围的权限。

### Cloudflare Access OAuth

你可以将自己的 MCP 服务器配置为通过 Cloudflare Access 要求用户认证。Cloudflare Access 充当身份聚合器，负责验证用户邮箱、来自你现有身份提供方（例如 GitHub 或 Google）的信号，以及 IP 地址、设备证书等其他属性。当用户连接到该 MCP 服务器时，系统会提示他们登录已配置的身份提供方，只有通过你的 Access 策略才会被授予访问权限。

如需分步部署指南，请参阅「使用 Access for SaaS 保护 MCP 服务器」。

### 第三方 OAuth

你可以将 MCP 服务器与任何支持 OAuth 2.0 规范的 OAuth 提供方对接，包括 GitHub、Google、Slack、Stytch、Auth0、WorkOS 等。

下面的示例演示了如何使用 GitHub 作为 OAuth 提供方。

#### 第 1 步 —— 创建一个新的 MCP 服务器

运行以下命令，创建一个使用 GitHub OAuth 的新 MCP 服务器：

npm yarn pnpm

npm create cloudflare@latest -- my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth

yarn create cloudflare my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth

pnpm create cloudflare@latest my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth

现在，你已经搭建好了 MCP 服务器，并安装了各项依赖。请进入该项目文件夹：

终端窗口

cd my-mcp-server-github-auth

你会注意到，在这个示例 MCP 服务器中，如果打开 src/index.ts，最主要的区别在于 defaultHandler 被设置为 GitHubHandler：

TypeScript

import GitHubHandler from "./github-handler" ;

export default new OAuthProvider ( {

apiRoute : "/mcp" ,

apiHandler : MyMCP . serve ( "/mcp" ) ,

defaultHandler : GitHubHandler ,

authorizeEndpoint : "/authorize" ,

tokenEndpoint : "/token" ,

clientRegistrationEndpoint : "/register" ,

} ) ;

这确保你的用户会被重定向到 GitHub 进行身份验证。不过，要让它正常工作，你需要按以下步骤创建 OAuth 客户端应用。

#### 第 2 步 — 创建 OAuth 应用

你需要创建两个 GitHub OAuth 应用 → 将 GitHub 用作你的 MCP 服务器的身份验证提供方 — 一个用于本地开发，一个用于生产环境。

#### 第 2.1 步 — 为本地开发创建新的 OAuth 应用

前往 github.com/settings/developers → 使用以下设置创建一个新的 OAuth 应用：

应用名称：My MCP Server (local)

主页 URL：http://localhost:8788

授权回调 URL：http://localhost:8788/callback

对于你刚刚创建的 OAuth 应用，将该 OAuth 应用的客户端 ID 添加为 GITHUB_CLIENT_ID，并生成客户端密钥，将其作为 GITHUB_CLIENT_SECRET 添加到项目根目录下的 .env 文件中，该文件将用于在本地开发中设置密钥。

终端窗口

touch .env

echo 'GITHUB_CLIENT_ID="your-client-id"' >> .env

echo 'GITHUB_CLIENT_SECRET="your-client-secret"' >> .env

cat .env

> .envecho 'GITHUB_CLIENT_SECRET="your-client-secret"' >> .envcat .env">

运行以下命令以启动开发服务器：

终端窗口

npm start

你的 MCP 服务器现在运行于 http://localhost:8788/mcp 。

在一个新的终端中，运行 MCP inspector ↗。MCP inspector 是一个交互式的 MCP 客户端，让你可以连接到自己的 MCP 服务器，并从网页浏览器中调用工具。

终端窗口

npx @modelcontextprotocol/inspector@latest

在网页浏览器中打开 MCP 检查器：

终端窗口

open http://localhost:5173

在检查器中，输入你的 MCP 服务器的 URL，即 http://localhost:8788/mcp

在右侧的主面板中，点击 OAuth Settings 按钮，然后点击 Quick OAuth Flow。

你应当会被重定向到 GitHub 登录或授权页面。在授权 MCP 客户端（即检查器）访问你的 GitHub 账户后，你将被重定向回检查器。

点击侧边栏中的 Connect，你应该会看到 "List Tools" 按钮，它会列出你的 MCP 服务器所暴露的工具。

#### 步骤 2.2 — 为生产环境创建新的 OAuth App

你需要重复步骤 2.1，为生产环境创建一个新的 OAuth App。

前往 github.com/settings/developers — 创建一个新的 OAuth App，设置如下：

Application name：My MCP Server（production）

Homepage URL：输入你已部署的 MCP 服务器的 workers.dev URL（例如：worker-name.account-name.workers.dev）

授权回调 URL：输入你部署的 MCP 服务器的 workers.dev URL 的 /callback 路径（例如：worker-name.account-name.workers.dev/callback）

对于你刚刚创建的 OAuth 应用，使用 Wrangler CLI 添加客户端 ID 和客户端密钥：

终端窗口

npx wrangler secret put GITHUB_CLIENT_ID

终端窗口

npx wrangler secret put GITHUB_CLIENT_SECRET

npx wrangler secret put COOKIE_ENCRYPTION_KEY # 在此填入任意随机字符串，例如 openssl rand -hex 32

警告

创建第一个 secret 时，Wrangler 会询问你是否要创建一个新的 Worker。输入 "Y" 以创建新的 Worker 并保存该 secret。

设置 KV 命名空间

a. 创建 KV 命名空间：

终端窗口

npx wrangler kv namespace create "OAUTH_KV"

b. 用生成的 KV ID 更新 wrangler.jsonc 文件：

{

" kvNamespaces " : [

{

" binding " : "OAUTH_KV" ,

" id " : "<YOUR_KV_NAMESPACE_ID>"

}

]

}

" } ]}">

将 MCP 服务器部署到你的 Cloudflare workers.dev 域名：

终端窗口

npm run deploy

使用 AI Playground ↗、MCP Inspector 或其他 MCP 客户端，连接到运行在 worker-name.account-name.workers.dev/mcp 上的服务器，并通过 GitHub 进行身份验证。

## 后续步骤

MCP 工具 向你的 MCP 服务器添加工具。

授权 自定义身份验证与授权。