<!-- source: pages/prompt-engineering-guide.html -->

# 提示词技术 | 提示词工程指南<!-- -->

🚀 学习用 Claude Code 构建应用！使用 PROMPTING 可享 8 折优惠 立即报名 →

提示词工程

引言

LLM 设置

提示词基础

提示词要素

设计 prompt 的通用技巧

prompt 示例

提示技术

零样本提示

少样本提示

思维链提示

元提示

自洽性

生成知识提示

提示链

思维树

检索增强生成

自动推理与工具调用（Automatic Reasoning and Tool-use）

自动提示词工程师（Automatic Prompt Engineer）

主动提示（Active-Prompt）

方向性刺激提示（Directional Stimulus Prompting）

程序辅助语言模型（Program-Aided Language Models）

ReAct

Reflexion

多模态思维链（Multimodal CoT）

图提示（Graph Prompting）

AI 智能体

智能体导论

智能体组件

AI 工作流 vs AI 智能体（agent）

面向 AI 智能体的上下文工程（context engineering）

上下文工程深度剖析

函数调用

深度智能体

指南

优化提示词

OpenAI 深度研究

推理 LLM

4o 图像生成

上下文工程指南

应用

微调 GPT-4o

函数调用

LLM 的上下文缓存

生成数据

为 RAG 生成合成数据集

应对生成数据集的多样性

生成代码

毕业生职位分类案例研究

提示词函数

提示词中心

分类

情感分类

少样本情感分类

编码

生成代码片段

生成 MySQL 查询

绘制 TiKZ 图表

创造力

押韵

无限素数

跨学科

创造新词

评估

评价柏拉图的对话录

信息抽取

抽取模型名称

图像生成

用字母表画出一个人

数学

求复合函数的值

奇数求和

问答

封闭域问答

开放域问答

科学问答

推理

间接推理

物理推理

文本摘要

解释概念

真实性

幻觉识别

对抗性提示

提示词注入

提示词泄露

越狱

模型

ChatGPT

Claude 3

Code Llama

Flan

Gemini

Gemini Advanced

Gemini 1.5 Pro

Gemma

GPT-4

Grok-1

Kimi K2.5

LLaMA

Llama 3

Mistral 7B

Mistral Large

Mixtral

Mixtral 8x22B

OLMo

Phi-2

Sora

LLM 合集

风险与误用

对抗性提示词

事实性

偏见

LLM 研究发现

LLM 智能体

RAG 面向 LLM

LLM 推理

RAG 忠实性

LLM 上下文内召回

RAG 减少幻觉

合成数据

ThoughtSculpt

Infini-Attention

LM-Guided CoT

LLM 的可信度

LLM 词元化

什么是 Groq？

论文

工具

Notebooks

数据集

延伸阅读

服务

English

Light

提示词技术

复制页面

# 提示词技巧

提示词工程有助于高效地设计和改进 prompt，让 LLM 在不同任务上取得更好的结果。

前面那些基础示例虽然有趣，但本节我们将介绍更进阶的提示词工程技巧，借助它们可以完成更复杂的任务，并提升 LLM 的可靠性与性能。

prompt 示例零样本提示