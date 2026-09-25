<!-- source: pages/observability-basics.html -->

# 追踪与跨度：你应该了解的可观测性基础 | Last9

我们使用 cookie 来定制你的 Last9 体验。你的偏好是什么？

仅必要项

全部接受

Last9

预约演示
打开菜单

Last9

预约演示
关闭菜单

产品

发现

探索

日志

链路追踪

指标

控制平面

RUM

告警

资源

指南

博客

活动

更新日志

更多

客户

文档

定价

Last9

2025年4月23日

# 追踪（trace）与跨度（span）：你应该了解的可观测性基础

了解追踪与跨度如何帮你洞察分布式系统的内部——从而更快地排查故障，构建更可靠的软件。

Anjali Udasi

#### 目录

在现代软件架构中，应用不只是在变得更大——它们正变得越来越分布式。微服务、无服务器函数和容器跨多个环境运行，想要弄清系统内部到底发生了什么，就像在暴风雨中追踪一滴雨。

这正是追踪与跨度登场的地方。这些可观测性工具并非只是流行语——它们是帮你理清复杂分布式系统的秘密武器。下面我们就来拆解：追踪与跨度究竟是什么、为什么重要，以及如何用它们更快排查故障、构建更可靠的系统。

## 理解追踪与跨度：核心概念

追踪记录的是一个请求在分布式系统中流转的完整旅程。可以把追踪想象成一个请求从头到尾的完整故事——从用户点击按钮的那一刻，直到他们看到结果。

跨度是追踪的构建单元。每个跨度代表这段旅程中的一个工作单元——比如一次数据库查询、一次 API 调用，或一次函数执行。跨度之间相互嵌套，以体现各操作之间的父子关系。

用简单的话说，二者的关系是这样的：

一个追踪包含多个跨度

每个跨度代表一次操作

跨度具有时间数据和元数据。

跨度可以嵌套，以展示操作之间的相互关系。

链路
├── 跨度 (API 网关)
│ ├── 跨度 (认证服务)
│ └── 跨度 (用户服务)
│ └── 跨度 (数据库查询)
└── 跨度 (响应格式化)

💡

如果你好奇链路和跨度如何与指标、日志和事件协同，这篇文章对四者进行了详细解析。

## 链路和跨度对 DevOps 专业人员的优势

你正在运行一个包含数十个微服务的复杂系统。突然，用户报告结账流程很慢。如果没有链路追踪（tracing），你就需要逐个检查每个服务，浪费宝贵的时间。

有了链路和跨度，你可以：

立即发现瓶颈：准确查看哪个服务或函数耗时过长

跨服务边界调试：跟踪请求在服务之间的跳转

理解依赖关系：可视化服务之间如何连接和相互依赖

提升性能：精确识别并修复缓慢的操作

缩短平均恢复时间（MTTR）：在问题出现时更快地找到根本原因

## 链路追踪与跨度的技术实现

我们来深入探讨分布式系统中链路追踪（tracing）的运作机制。

### 追踪上下文与传播

要让链路追踪跨越服务边界生效，每个服务都需要知道自己正在处理同一个请求的一部分。这通过上下文传播实现——在服务之间传递追踪 ID 和跨度 ID。

当请求首次到达你的系统时，它会被分配一个唯一的追踪 ID。随着请求在服务之间流转，这个 ID 也随之传递（通常以 HTTP 请求头的形式）。随后每个服务创建自己的跨度，但将它们关联到同一个追踪。

### 跨度属性与事件

跨度不只是时间戳——它们承载着丰富的数据：

名称：该跨度代表的操作

时间：开始与结束时间

状态：成功、错误等

属性：自定义键值对（例如 user_id 或 cart_size ）

事件：跨度内值得注意的 occurrences

链接：与其他 span 的连接

### 采样策略

追踪所有内容会产生海量数据。因此大多数系统会采用采样——只收集一定比例的链路追踪数据。智能采样策略包括：

头部采样：在请求开始时决定是否采样

尾部采样：在请求完成后决定（更擅长捕获错误）

优先级采样：重要操作始终追踪，常规操作则按比例采样

💡

如果你想弄清可观测性、遥测与监控之间的区别，可以看看这篇有用的文章：Observability vs Telemetry vs Monitoring。

## 链路追踪实现指南：工具与框架

准备好为你的系统添加链路追踪了？以下是你需要的内容：

### OpenTelemetry：行业标准

OpenTelemetry 已成为实现 trace 与 span 的首选框架。它提供：

覆盖所有主流编程语言的库

厂商中立的 API 与 SDK

为流行框架提供自动插桩

一套统一的数据收集与导出方式

### 链路追踪工具箱

以下这些工具可以帮助你收集、存储并可视化链路追踪数据：

工具
类型
适用场景

Last9
一体化可观测性
高性价比、支持高基数数据且定价可预测的可观测性

Jaeger
开源链路追踪
自托管的链路追踪可视化

Zipkin
开源链路追踪
简单的分布式链路追踪

Grafana Tempo
链路追踪后端
与 Grafana 仪表盘集成

OpenTelemetry Collector
数据收集流水线
处理并路由遥测数据

如果你在寻找一款符合自身预算的可观测性方案，Last9 值得一试。它的定价基于摄入事件的数量，因此成本可预测。此外，我们的平台能够大规模处理高基数数据，并可与 OpenTelemetry 和 Prometheus 集成，把你的指标、日志和链路追踪汇聚到同一个地方。

### 在代码中实现链路追踪

下面是一个简化示例，展示如何在 Node.js 应用中使用 OpenTelemetry 创建 span：

// Initialize the OpenTelemetry SDK (once in your app)
const { NodeTracerProvider } = require ( '@opentelemetry/sdk-trace-node' );
const { SimpleSpanProcessor } = require ( '@opentelemetry/sdk-trace-base' );
const { OTLPTraceExporter } = require ( '@opentelemetry/exporter-trace-otlp-http' );

const provider = new NodeTracerProvider ();
const exporter = new OTLPTraceExporter ({
url: 'http://localhost:4318/v1/traces' ,
});
provider. addSpanProcessor ( new SimpleSpanProcessor (exporter));
provider. register ();

// Get a tracer
const { trace } = require ( '@opentelemetry/api' );
const tracer = trace. getTracer ( 'my-service' );

// Create spans in your code
async function processOrder ( orderId ) {
const span = tracer. startSpan ( 'process-order' );

// Add attributes to the span
span. setAttribute ( 'order.id' , orderId);
span. setAttribute ( 'customer.type' , 'premium' );

try {
// Do work...

// Create a child span
const dbSpan = tracer. startSpan ( 'database-query' , {
parent: span,
});

try {
// Run database query... dbSpan. end ();
} catch (error) {
dbSpan. setStatus ({ code: SpanStatusCode. ERROR });
dbSpan. recordException (error);
dbSpan. end ();
throw error;
}

span. end ();
} catch (error) {
span. setStatus ({ code: SpanStatusCode. ERROR });
span. recordException (error);
span. end ();
throw error;
}
}

💡

想知道 OpenTelemetry 与传统 APM 工具相比究竟如何？这篇文章拆解了二者的关键差异：OpenTelemetry 与传统 APM 工具对比。

## 高级链路追踪技术

一旦基本的链路追踪（tracing）落地，这些高级技术就能把你的可观测性提升到新的水平。

### 分布式上下文管理

在复杂系统中，需要管理的上下文远不止追踪 ID（trace ID）。W3C Trace Context 规范为以下方面提供了标准：

traceparent：包含追踪 ID 与父跨度 ID

tracestate：允许供应商添加自定义上下文数据

使用这些请求头，可以确保链路追踪在不同服务和供应商之间都能正常工作。

### 链路追踪、指标与日志之间的关联

可观测性的真正威力，来自把不同信号连接起来：

示例链路追踪（exemplar traces）：把指标与产生它们的链路追踪关联起来

日志中的追踪 ID：在日志消息中加入追踪 ID，以便交叉引用

自定义属性：在所有遥测类型中使用一致的属性

### 错误处理与异常追踪

当异常发生时，span 可以提供关键的上下文：

将 span 标记为错误状态

记录异常及其堆栈跟踪

向 span 添加事件，以展示错误的演进过程

创建可跨服务边界携带错误上下文的 baggage 项

💡

如需更深入地了解如何主动发现问题并提升系统可靠性，请查看这篇关于主动监控的文章：主动监控。

## 真实世界的链路追踪模式与反模式

### 有效的链路追踪模式

有意义的 span 名称：使用一致的命名约定，如 service_name/operation

恰当的粒度：为重要操作创建 span，而非每个函数调用

正确的上下文传播：确保链路追踪上下文流经所有通信渠道

实用属性：添加有助于故障排查的属性，例如用户 ID 或功能开关

性能意识：注意过度创建 Span 带来的开销

### 应避免的链路追踪反模式

过度埋点：创建过多 Span 可能导致性能问题

上下文缺失：未能传播上下文会破坏跨服务边界的链路追踪

命名不一致：使用不同的命名标准会让链路追踪更难解读

数据过多：在 Span 中放入大型载荷可能压垮你的链路追踪后端

忽视第三方服务：外部调用缺少 Span 会造成盲区

💡

探索可观测性如何在 LLM 的性能与可靠性中发挥关键作用：LLM 可观测性。

## 链路追踪与 Span 的业务价值：超越技术收益

链路追踪不仅仅用于故障排查——它们还能提供业务洞察：

端到端地跟踪关键用户旅程

衡量关键业务操作的性能

基于链路追踪数据设置 SLO（服务级别目标）

用真实用户视角量化性能问题带来的成本

通过在 span（跨度）中添加相关属性来构建业务上下文

当你能展示技术改进如何影响用户体验和业务指标时，你就弥合了 DevOps 与业务相关方之间的鸿沟。

## 结论

链路追踪（trace）与跨度（span）让你拥有透视分布式系统的 X 光视野。它们揭示服务之间隐藏的关联，精准定位性能瓶颈，并大幅加快调试速度。

随着系统日益复杂，这类可观测性并非锦上添花，而是必不可少。

💡

如果你想继续探讨分布式链路追踪与可观测性，欢迎加入我们的 Discord 社区，DevOps 专业人士在这里分享经验与最佳实践！

## 常见问题

### 链路追踪与日志记录有什么区别？

日志记录捕获的是离散事件，而链路追踪展示的是跨服务各操作之间的关系。日志告诉你发生了什么；链路追踪告诉你它是如何发生的。

### 添加链路追踪会拖慢我的应用吗？

现代链路追踪库带来的开销极小——配置得当时，性能影响通常低于 3%。通过采样，还能进一步降低这一影响。

### 为了添加链路追踪，我需要修改所有代码吗？

不一定。许多框架提供自动插桩，只需极少代码改动就能添加链路追踪。OpenTelemetry 为大多数语言中的主流框架提供自动插桩。

### 分布式链路追踪会生成多少数据？

这取决于流量、采样率和 Span 详细程度，差异很大。对于繁忙的系统，要按每天数 GB 到数 TB 来规划。因此，选择合适的可观测性平台对成本控制至关重要。

### 链路追踪数据有助于安全和合规吗？

是的！链路追踪数据会为请求在系统中的流转创建审计追踪。借助合适的属性，你可以追踪哪些用户或服务在何时访问了哪些数据。

### 链路追踪数据和 Span 如何与其他可观测性信号配合？

链路追踪数据与指标、日志互为补充。指标从宏观层面展示系统健康状况，日志提供详细事件，而链路追踪数据则将它们串联起来，展示跨服务的请求流。

主题

可观测性监控

关于作者

Anjali Udasi

帮助让技术变得不那么令人生畏。

#### 目录

## 免费开始可观测。无供应商锁定。

预约演示

OPENTELEMETRY • PROMETHEUS

只需更新配置，几秒内即可在 Last9 上看到数据。

DATADOG • NEW RELIC • 其他

我们已为你考虑周全。一键迁移你的仪表盘与告警。

基于开放标准构建

100+ 集成。OTel 原生，兼容你现有的技术栈。

4.8/5

G2 评价

Gartner 2025 年 Cool Vendor

高绩效者

最佳可用性

用户采用率最高