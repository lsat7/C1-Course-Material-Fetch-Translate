<!-- source: pages/prompt-engineering-overview.html -->

# AI 提示词工程指南 | Google Cloud

# 提示词工程：概览与指南

最后更新：2026/01/14

大语言模型（LLM）的兴起为人机交互带来了令人兴奋的可能性。然而，要充分释放这些强大 AI 模型的潜力，还需要一项关键技能：prompt 工程。这一新兴领域聚焦于打造有效的 prompt，以释放 LLM 的能力，使其能够理解意图、遵循指令并生成期望的输出。随着我们在各类应用中与 AI 的交互日益频繁，prompt 工程在确保交互准确、相关且安全方面发挥着至关重要的作用。

免费开始使用

试用对话 prompt

1:53

成为世界级提示词工程师的技巧

## 什么是提示词工程？

提示词工程是设计与优化 prompt、引导 AI 模型（尤其是 LLM）生成期望回复的艺术与科学。通过精心设计 prompt，你为模型提供上下文、指令和示例，帮助它理解你的意图并给出有意义的回应。可以把它看作是为 AI 提供一份路线图，把它引导向你心中所想的那个具体输出。

想更深入地了解 prompt 设计的世界并探索它的应用，请查看 Google Cloud 上的《提示设计入门》（Introduction to Prompt Design）。

想亲自上手试试 LLM 和 prompt 工程吗？那就试试 Vertex AI 免费试用，体验这项技术的威力。

## 什么是面向 AI 的 prompt？

在 AI 的语境中，prompt 是你提供给模型的输入，用以引出特定的回应。它可以有多种形式，从简单的问题或关键词，到复杂的指令、代码片段，甚至创意写作样本。你的 prompt 是否有效，直接影响 AI 输出的质量与相关性。

## 做提示词工程需要什么？

有几个关键要素有助于实现有效的 prompt 工程。掌握这些要素，你就能与 AI 模型高效沟通，充分释放它们的潜力。

### prompt 格式

你的 prompt 的结构与风格，在引导 AI 回应方面起着重要作用。不同模型可能对某些特定格式反应更好，例如：

你的 prompt 格式在很大程度上决定了 AI 如何解读你的请求。不同模型可能对某些特定格式反应更好，例如自然语言提问、直接命令，或带有特定字段的结构化输入。了解模型的能力及其偏好的格式，是设计有效 prompt 的关键。

### 上下文与示例

在你的 prompt 中提供上下文和相关示例，有助于 AI 理解期望的任务，并生成更准确、更相关的输出。例如，如果你想要一个创意故事，加入几句描述期望语气或主题的话，就能显著改善结果。

### 微调（Fine-tuning）与适配

使用量身定制的 prompt，针对特定任务或领域对 AI 模型进行微调，可以提升其表现。此外，根据用户反馈或模型输出调整 prompt，也能随时间推移进一步改善模型的回复。

### 多轮对话

为多轮对话设计 prompt，能让用户与 AI 模型进行持续且具备上下文感知的交互，从而提升整体用户体验。

## prompt 的类型

AI 中使用的 prompt 有若干类型，各服务于特定目的：

### 直接 prompt（零样本）

零样本提示（zero-shot prompting）是指向模型提供直接的指令或问题，而不附加任何上下文或示例。

一个例子是创意生成，即提示模型生成创意想法或头脑风暴方案。另一个例子是摘要或翻译，即要求模型对某段内容进行总结或翻译。

### 单样本、少样本与多样本 prompt

这种方法是在给出实际的 prompt 之前，先向模型提供一个或多个期望的输入-输出对示例。这有助于模型更好地理解任务，并生成更准确的回复。

### 思维链（Chain of Thought）提示词

CoT 提示词会鼓励模型把复杂推理拆解为一系列中间步骤，从而得到更全面、结构更清晰的最终输出。

### 零样本 CoT 提示词

将思维链提示词与零样本提示词结合，要求模型执行推理步骤，往往能产出更好的输出。

## 提示词工程的使用场景与示例

以下是一些具体示例和使用场景，展示 prompt 工程如何帮助产出定制化且贴合的答案。

### 语言与文本生成

场景

指令

示例提示词

创意写作

精心设计提示词，明确体裁、语气、风格与情节点，引导 AI 生成引人入胜的叙事。

“写一个短篇故事，讲述一位年轻女性在自家阁楼里发现了一道魔法传送门。”

摘要生成

向 AI 提供文本，并指示它生成能够抓住关键信息的简洁摘要。

“总结下面这篇关于气候变化的新闻报道的要点。”

翻译

指定源语言和目标语言，让 AI 在保留含义与上下文的前提下准确翻译文本。

“把下面这段文字从英语翻译成西班牙语：‘The quick brown fox jumps over the lazy dog.’”

对话

设计模拟对话的 prompt，让 AI 生成模仿人类互动的回复并保持上下文。

“你是一个友好的聊天机器人，帮助用户排查电脑问题。请回复用户的提问：‘我的电脑开不了机。’”

场景

指令

示例 prompt

创意写作

精心设计 prompt，明确体裁、语气、风格和情节点，引导 AI 生成引人入胜的叙事。

“写一个短篇故事，讲述一位年轻女子在自家阁楼里发现一道魔法传送门。”

摘要生成

向 AI 提供文本，并指示它生成能抓住关键信息的简洁摘要。

“总结下面这篇关于气候变化的新闻文章的要点。”

翻译

明确源语言和目标语言，使 AI 能够准确翻译文本，同时保留含义与语境。

“将以下文本从英语翻译成西班牙语：‘The quick brown fox jumps over the lazy dog.’”

对话

设计用于模拟对话的 prompt，让 AI 生成模仿人类交互、并能保持上下文的回复。

“你是一个友好的聊天机器人，帮助用户排查电脑问题。请回应用户的提问：‘我的电脑开不了机。’”

### 问答

场景

指令

示例 prompt

开放式问题

设计 prompt，引导 AI 基于其知识库给出全面而信息丰富的回答。

“解释量子计算的概念及其对未来技术的潜在影响。”

特定问题

设计针对具体信息的 prompt，让 AI 能够从所提供的上下文或其内部知识库中检索出准确的答案。

“法国的首都是哪里？”或“根据所提供的文本，森林砍伐的主要原因是什么？”

多项选择题

提供带有选项的提示词，促使 AI 根据自己对上下文的理解进行分析，并选出最合适的答案。

“《哈利·波特》系列是谁写的？A) J.R.R. 托尔金，B) J.K. 罗琳，C) 斯蒂芬·金”

假设性问题

设计探索假设情境的提示词，让 AI 展开推理、推测，并给出可能的结果或解决方案。

“如果人类能以光速旅行，会发生什么？”

观点类问题

设计能引出 AI 对特定话题看法或观点的提示词，鼓励它为自身立场给出推理和依据。

“你认为人工智能最终会超越人类智能吗？为什么？”

场景

指令

示例提示词

开放式问题

制定 prompts，鼓励 AI 基于其知识库提供全面且信息丰富的回答。

"解释量子计算的概念及其对未来技术的潜在影响。"

具体问题

设计针对特定信息的 prompts，使 AI 能够从提供的上下文或其内部知识库中检索精确答案。

"法国的首都是什么？" 或 "根据提供的文本，森林砍伐的主要原因是什么？"

多项选择题

提供带有选项的 prompts，促使 AI 基于其对上下文的理解分析并选择最合适的答案。

"《哈利·波特》系列是谁写的？A) J.R.R. 托尔金，B) J.K. 罗琳，C) 斯蒂芬·金"

假设性问题

设计用于探索假设情境的 prompts，让 AI 进行推理、推测，并提供可能的结果或解决方案。

"如果人类能以光速旅行，会发生什么？"

观点类问题

设计提示词，引导 AI 就特定主题给出自己的视角或观点，并鼓励它为自己的立场提供推理与论证。

“你认为人工智能最终会超越人类智能吗？为什么？”

### 代码生成

场景

说明

示例提示词

代码补全

向 AI 提供一段不完整的代码片段，并 prompt 它，使其根据上下文和编程语言建议或补全剩余的代码。

“编写一个 Python 函数，用于计算给定数字的阶乘。”

代码翻译

指定源编程语言和目标编程语言，让 AI 在翻译代码的同时保留其功能与语法。

“将下面的 Python 代码翻译成 JavaScript：def greet(name): print('Hello,', name)”

代码优化

用 prompt 引导 AI 分析现有代码，并就效率、可读性或性能提出改进建议。

“优化以下 Python 代码，以缩短其执行时间。”

代码调试

向 AI 提供含错误的代码，并 prompt 其找出已识别的问题并提出可能的解决方案。

“调试以下 Java 代码，并解释它为什么会抛出 NullPointerException。”

场景

说明

示例 prompt

代码补全

向 AI 提供一段不完整的代码片段，并 prompt 其根据上下文和编程语言补全或建议剩余的代码。

“编写一个 Python 函数，用于计算给定数字的阶乘。”

代码翻译

指定源编程语言和目标编程语言，使 AI 在翻译代码的同时保持功能与语法不变。

“将以下 Python 代码翻译成 JavaScript：def greet(name): print('Hello,', name)”

代码优化

提示 AI 分析现有代码，并就效率、可读性或性能提出改进建议。

“优化以下 Python 代码，缩短其执行时间。”

代码调试

向 AI 提供包含错误的代码，并 prompt 它找出这些问题并提出可能的解决方案。

“调试以下 Java 代码，并解释它为什么会抛出 NullPointerException。”

### 图像生成

场景

指令

示例 prompt

照片级真实图像

精心编写 prompt，详细描述期望的图像，涵盖物体、场景、光照和风格，从而生成逼真且高质量的图像。

“一张照片级真实的图像，展现海面上的日落，棕榈树在天空中形成剪影。”

艺术风格图像

设计 prompt，明确指定艺术风格、技法和主题内容，引导 AI 创作出模仿特定艺术流派或唤起特定情感的图像。

“一幅印象派画作，描绘熙熙攘攘的城市街道，人们在雨中撑着伞行走。”

抽象图像

构建 prompt，鼓励 AI 生成可供自由解读的图像，运用形状、色彩和质感来唤起某种感受或概念。

“一幅表现‘希望’这一概念的抽象图像，使用明亮的色彩和流动的形状。”

图像编辑

向 AI 提供一张已有图像并说明期望的修改，使其能够按照给定的指令编辑并增强该图像。

“把这张照片的背景换成星空，再加一轮满月。”或者“把这张图中的人去掉，换成一只猫。”

场景

说明

示例 prompt

照片级真实感图像

精心编写 prompt，详细描述想要的图像，包括物体、场景、光照和风格，从而生成真实、高质量的图像。

“一张照片级真实感的图像：海面上的日落，棕榈树在天空中映出剪影。”

艺术类图像

设计 prompt，明确指定艺术风格、技法和主题内容，引导 AI 创作出模仿特定艺术流派或唤起特定情绪的图片。

“一幅印象派油画：熙熙攘攘的城市街道，人们撑着伞在雨中行走。”

抽象图像

构思 prompt，鼓励 AI 生成可供多种解读的图像，运用形状、色彩和质感来唤起某种感受或概念。

"一幅表现「希望」这一概念的抽象图像，采用明亮的色彩与流动的形态。"

图像编辑

向 AI 提供一张已有图像并说明期望的修改，使其能够按照给定指令对该图像进行编辑与增强。

"把这张照片的背景换成繁星点点的夜空，并加上一轮满月。"或者"把图中的人移除，替换成一只猫。"

## 编写更佳 prompt 的策略

编写有效的 prompt 需要策略性的方法。可参考以下策略来提升你的 prompt 工程技能：

### 1. 设定清晰的目标与目的：

技巧

prompt 示例

使用动作动词明确指出期望的动作

"写一份项目符号列表，概括所附研究论文的关键发现"

明确输出的期望长度与格式

撰写一篇 500 词的文章，讨论气候变化对沿海社区的影响。

明确目标受众

为一条新的有机护肤品产品线撰写产品描述，目标受众是关注可持续性的年轻人。

策略

Prompt 示例

使用动作动词来明确期望的动作

撰写一份项目符号列表，总结所附研究论文的关键发现

明确输出的期望长度和格式

撰写一篇 500 词的文章，讨论气候变化对沿海社区的影响。

明确目标受众

为一条新的有机护肤品产品线撰写产品描述，目标受众是关注可持续性的年轻人。

### 2. 提供上下文和背景信息：

策略

prompt 示例

纳入相关事实与数据

“鉴于自前工业化时代以来全球气温已上升 1 摄氏度，讨论海平面上升可能带来的后果。”

引用具体来源或文档

“根据所附财务报告，分析该公司过去五年的盈利能力。”

界定关键术语与概念

“用通俗易懂的语言解释量子计算的概念，面向非技术背景的读者。”

策略

prompt 示例

纳入相关事实与数据

“鉴于自前工业化时代以来全球气温已上升 1 摄氏度，讨论海平面上升可能带来的后果。”

引用具体的来源或文档

"根据所附的财务报告，分析该公司过去五年的盈利能力。"

定义关键术语和概念

"用通俗的语言解释量子计算的概念，适合非技术背景的听众。"

### 3. 使用少样本 prompt：

策略

prompt 示例

给出几个期望的输入-输出对示例

输入："猫" 输出："一种长着胡须的小型毛茸茸哺乳动物。" 输入："狗" 输出："一种以忠诚著称的驯化犬类。" prompt："大象"

展示期望的风格或语气

示例 1（幽默）："这位政客的演讲如此乏味，简直能治好失眠。" 示例 2（正式）："这位政要发表了一场既信息丰富又引人入胜的演讲。" prompt："写一句话，描述这位喜剧演员的单口喜剧表演。"

展示期望的详细程度

示例 1（简要）："这部电影讲述了一个小男孩与外星人成为朋友的故事。" 示例 2（详细）："这部科幻片讲述了埃利奥特的故事，一个孤独的男孩发现了一个被困在地球上的外星人，并与它建立了独特的情感纽带。" 提示词："总结你刚读完的小说的情节。"

策略

提示词示例

提供几个期望的输入-输出对示例

输入："猫" 输出："一种长有胡须的小型毛茸茸哺乳动物。" 输入："狗" 输出："一种以忠诚著称的驯化犬科动物。" 提示词："大象"

展示期望的风格或语气

示例 1（幽默）："那位政客的演讲如此乏味，简直能治好失眠。" 示例 2（正式）："那位政要发表了一场既富有信息量又引人入胜的演讲。" 提示词："写一句话描述这位喜剧演员的脱口秀表演。"

展示期望的详细程度

示例 1（简要）："这部电影讲述了一个小男孩与外星人成为朋友的故事。" 示例 2（详细）："这部科幻片讲述了埃利奥特的故事，一个孤独的男孩发现了一个被困在地球上的外星人，并与它建立了独特的情感纽带。" 提示词："总结你刚读完的小说的情节。"

### 4. 要具体明确：

策略

提示词示例

使用精确的语言，避免歧义

不要写：“写点关于气候变化的内容”，而应写：“写一篇有说服力的文章，论证应实施更严格的碳排放法规。”

尽可能量化你的请求

不要写：“写一首长诗”，而应写：“写一首 14 行的十四行诗，探讨爱与失去的主题。”

把复杂任务拆解为更小的步骤

不要写：“制定一份营销计划”，而应写：“1. 确定目标受众。2. 制定核心营销信息。3. 选择合适的营销渠道。”

策略

prompt 示例

使用精确的语言，避免歧义

不要写：“写点关于气候变化的内容”，而应写：“写一篇有说服力的文章，论证应实施更严格的碳排放法规。”

尽可能量化你的请求

不要写：“写一首长诗”，而应写：“写一首 14 行的十四行诗，探讨爱与失去的主题。”

将复杂任务拆解为更小的步骤

不要用："制定一份营销计划"，而要用："1. 确定目标受众。2. 制定关键营销信息。3. 选择合适的营销渠道。"

### 5. 迭代与实验：

策略

操作

尝试不同的措辞和关键词

用同义词或替代句式改写你的 prompt。

调整细节和具体程度

增加或删减信息，以微调输出结果。

测试不同长度的 prompt

尝试更短和更长的 prompt，找到最佳平衡点。

策略

操作

尝试不同的措辞和关键词

使用同义词或替换句式，重新表述你的 prompt。

调整细节程度与具体程度

增加或删减信息，以微调输出。

测试不同的 prompt 长度

分别尝试更短和更长的 prompt，找到最佳平衡点。

### 6. 利用思维链提示：

策略

prompt 示例

鼓励逐步推理

“逐步解决这个问题：John 有 5 个苹果，他吃了 2 个。他还剩多少个苹果？步骤 1：John 一开始有 5 个苹果。步骤 2：他吃了 2 个苹果，所以需要从 5 中减去 2。步骤 3：5 - 2 = 3。答案：John 还剩 3 个苹果。”

让模型解释其推理过程

"请说明你在判断这条影评情感倾向时的思考过程：'The acting was superb, but the plot was predictable.'"

引导模型按照合乎逻辑的思路顺序进行推理

"要将这封邮件分类为垃圾邮件或非垃圾邮件，请考虑以下几点：1. 发件人是否已知？2. 主题行是否包含可疑关键词？3. 邮件是否在提供好得令人难以置信的东西？"

策略

prompt 示例

鼓励逐步推理

"逐步解决这个问题：John 有 5 个苹果，他吃了 2 个。他还剩下几个苹果？第 1 步：John 一开始有 5 个苹果。第 2 步：他吃了 2 个苹果，所以需要从 5 中减去 2。第 3 步：5 - 2 = 3。答案：John 还剩下 3 个苹果。"

让模型解释其推理过程

"请说明你在判断这条影评情感倾向时的思考过程：'The acting was superb, but the plot was predictable.'"

引导模型按照合乎逻辑的思路顺序进行推理

"要将这封邮件分类为垃圾邮件或非垃圾邮件，请考虑以下几点：1. 发件人是否已知？2. 主题行是否包含可疑关键词？3. 邮件是否在提供好得令人难以置信的东西？"

如需进一步了解 prompt 工程的最佳实践，请参阅 Google Cloud 上的《提示词工程五大最佳实践》。

## 提示词工程的优势

有效的 prompt 工程带来诸多优势，可增强 AI 模型的能力与易用性：

### 提升模型表现

精心设计的提示词能够提供清晰的指令与上下文，从而让 AI 模型给出更准确、更相关、更有信息量的输出。

### 减少偏见与有害回复

通过谨慎控制输入并引导 AI 的关注点，prompt 工程有助于缓解偏见，并尽可能降低生成不当或冒犯性内容的风险。

### 增强控制力与可预测性

提示词工程让你能够影响 AI 的行为，确保其回复保持一致、可预测，并与你期望的结果相符。

### 改善用户体验

清晰简洁的提示词让用户更容易与 AI 模型进行有效交互，从而获得更直观、更令人满意的体验。

### 从 Google Cloud 开启你的 AI 之旅

新客户可获得 $300 免费额度，用于 Google Cloud 消费。

开始使用

与 Google Cloud 销售专家交流，更详细地讨论您面临的独特挑战。

联系我们

## 相关 Google Cloud 产品和服务

查看所有 AI 产品与解决方案

Vertex AI 平台

一个统一平台，供数据科学家和工程师创建、训练、测试、监控、调优和部署机器学习与 AI 模型。

Vertex AI 上的生成式 AI

快速构建并测试生成式 AI 模型原型。测试示例 prompt、设计自己的 prompt，并自定义基础模型和 LLM。

AI API

借助 Google Cloud 的 AI 和机器学习 API，轻松将 AI 集成到您的应用中。

解决方案

Vertex AI 上的 Model Garden

通过一个统一平台发现、定制并部署来自 Google 及 Google 合作伙伴的多种模型，快速启动你的机器学习项目。

#### 更多入门学习资源

初次接触 Google Cloud 或生成式 AI？新客户可获得 $300 免费赠金，用于运行、测试和部署工作负载。

培训：免费的生成式 AI 基础课程

文档：prompt 设计简介

文档：通用 prompt 设计策略

文档：生成式 AI prompt 示例

#### 下一步

使用 $300 免费赠金和 20 多种始终免费的产品，开始在 Google Cloud 上构建。

免费开始使用

##### 需要帮助上手吗？

联系销售

##### 与值得信赖的合作伙伴携手

查找合作伙伴

##### 继续浏览

查看所有产品

菜单



搜索 发送

文档 支持

控制台

登录

免费开始

免费开始

联系我们

关闭

加速您的数字化转型

无论您的企业刚刚踏上数字化征程，还是已在数字化转型的道路上稳步前行，Google Cloud 都能帮您攻克最棘手的挑战。

了解更多

核心优势

为什么选择 Google Cloud

企业选择我们的主要原因。

AI 与 ML

获取企业级 AI 能力。

多云

在任意需要的位置运行你的应用。

全球基础设施

在支撑 Google 的同一套基础设施之上构建。

数据云

以统一的数据做出更明智的决策。

现代化基础设施云

新一代云基础设施。

安全

保护你的用户、数据和应用。

生产力与协作

用 AI 驱动的应用连接你的团队。

报告与洞察

高管洞察

精心遴选的高管视角。

分析师报告

了解行业分析师如何评价我们。

白皮书

浏览并下载热门白皮书。

客户案例

探索案例研究与视频。

关闭

行业解决方案

应用现代化

人工智能

API 与应用

数据分析

数据库

基础设施现代化

生产力与协作

安全

初创企业与中小企业

查看所有解决方案

行业解决方案

降低成本、提升运营敏捷性，并把握新的市场机遇。

零售

面向零售价值链的分析与协作工具。

快速消费品

面向 CPG 数字化转型和品牌增长的解决方案。

金融服务

面向金融服务的计算、数据管理和分析工具。

医疗健康与生命科学

大规模推进研究，赋能医疗健康创新。

媒体与娱乐

面向内容制作与分发运营的解决方案。

电信

用于部署 5G 并实现其商业化的混合云与多云服务。

游戏

AI 驱动的解决方案，助您更快地构建和扩展游戏。

制造业

通过迁移与 AI 工具优化制造业价值链。

供应链与物流

在供应链与物流运营中实现可持续、高效且具备韧性的数据驱动运营。

政府

面向政府机构的数据存储、AI 与分析解决方案。

教育

提供更具吸引力的学习体验的教学工具。

没有找到您想要的内容？

查看所有行业解决方案

应用现代化

评估、规划、实施并度量软件实践与能力，从而对组织的业务应用组合进行现代化改造与简化。

CAMP

使用 DORA 提升软件交付能力的计划。

现代化传统应用

分析、分类传统工作负载，并着手进行云端迁移。

从 PaaS 迁移：Cloud Foundry、Openshift

将现有容器迁移到 Google 托管容器服务的工具。

从大型机迁移

将大型机应用迁移到云端的自动化工具与规范性指导。

现代化软件交付

软件供应链最佳实践 —— 内循环生产力、CI/CD 与 S3C。

DevOps 最佳实践

在组织内实施 DevOps 的流程与资源。

SRE 原则

在组织内采用 SRE 的工具与资源。

平台工程

全面的托管服务与黄金路径套件，用于构建、管理和扩展 IDP。

在边缘运行应用

在 Google 硬件无关的边缘解决方案上运行本地化低延迟应用的指南。

面向多云进行架构设计

借助一致的平台跨多云管理工作负载。

采用无服务器架构

用于开发、部署和扩展应用的完全托管环境。

人工智能

借助 AI 和机器学习，为你的业务注入智能与效率。

搭载 Google AI 的客户互动套件

端到端应用，融合了我们最先进的对话式 AI。

Document AI

大规模自动化文档处理与数据采集。

面向电商的 Vertex AI Search

为零售商提供 Google 级搜索与商品推荐。

搭载 Gemini 的 Google Cloud

用于应用开发、编码等的 AI 助手。

Google Cloud 上的生成式 AI

借助生成式 AI 的力量，革新内容创作与发现、研究、客户服务以及开发者效率。

API 与应用

无需编码，借助 API、应用与自动化，加快创新步伐。

利用 API 开拓新业务渠道

吸引并赋能由开发者和合作伙伴组成的生态。

借助 API 释放遗留应用的潜力

用于扩展和现代化改造遗留应用的云服务。

开放银行 APIx

简化并加速符合开放银行规范的 API 的安全交付。

数据分析

借助无服务器、全托管的分析平台，从任意规模的数据中即时生成洞察，大幅简化分析工作。

数据迁移

借助 AI 驱动的迁移服务，迁移并现代化改造你的数据仓库与数据湖。

数据湖仓

用高性能的开放式数据湖仓统一并治理你的多模态数据。

实时分析

摄取、处理和分析事件流所获得的洞察。

营销分析

用于收集、分析和激活客户数据的解决方案。

数据集

来自 Google、公共及商业提供方的数据，用于丰富你的分析与 AI 举措。

商业智能

用于现代化你的 BI 技术栈并打造丰富数据体验的解决方案。

面向数据分析的 AI

借助面向数据分析的 AI 编写 SQL、构建预测模型并可视化数据。

地理空间分析

一个综合平台，可大规模解决地理空间用例。

数据库

借助安全、可靠、高可用且全托管的数据服务，迁移并管理企业数据。

数据库迁移

简化数据库迁移生命周期的指南与工具。

数据库现代化

通过升级实现运营数据库基础设施的现代化。

游戏数据库

使用 Google Cloud 数据库构建全球化的实时游戏。

Google Cloud 数据库

用于迁移、管理和现代化数据的数据库服务。

将 Oracle 工作负载迁移到 Google Cloud

对 Oracle 工作负载进行重新托管、重新平台化和重写。

开源数据库

全托管开源数据库，提供企业级支持。

Google Cloud 上的 SQL Server

在 Google Cloud 上运行 SQL Server 虚拟机的多种方案。

Gemini 数据库版

借助 AI 大幅提升数据库开发与管理效率。

基础设施现代化

借助面向 SAP、VMware、Windows、Oracle 及其他工作负载的解决方案快速迁移。

应用迁移

用于上云迁移的发现与分析工具。

Google Cloud 上的 SAP

运行 SAP 应用与 SAP HANA 的认证。

高性能计算

支持任意工作负载的计算、存储和网络选项。

Google Cloud 上的 Windows

用于运行 Windows 工作负载的工具和合作伙伴。

数据中心迁移

适用于虚拟机、应用、数据库等的迁移解决方案。

Active Assist

自动优化云资源并增强安全性。

虚拟桌面

面向桌面和应用的远程办公解决方案（VDI 与 DaaS）。

快速迁移与现代化计划

端到端迁移计划，简化您的上云路径。

备份与灾难恢复

确保满足您的业务连续性需求。

Google Cloud 上的 Red Hat

Google 与 Red Hat 提供企业级平台，适用于传统本地部署和自定义应用。

跨云网络

简化混合云与多云网络，保障您的工作负载、数据和用户安全。

可观测性

借助端到端可见性，监控、排查并提升应用性能。

生产力与协作

以专为人设计、为成效而构建的解决方案，改变团队的工作方式。

Google Workspace

面向企业的协作与生产力工具。

Google Workspace Essentials

为团队提供安全的视频会议和现代化协作。

Cloud Identity

供 IT 管理员管理用户设备和应用的统一平台。

Chrome Enterprise

为企业打造的 ChromeOS、Chrome 浏览器和 Chrome 设备。

安全

检测、调查并响应在线威胁，帮助保护您的业务。

智能体化 SOC

借助 AI 智能体实现更好的安全成果。

Web 应用与 API 防护

为您的 Web 应用和 API 提供威胁与欺诈防护。

安全与韧性框架

针对安全与韧性生命周期各阶段的解决方案。

风险与合规即代码（RCaC）

通过自动化实现治理、风险与合规职能现代化的解决方案。

软件供应链安全

用于提升端到端软件供应链安全的解决方案。

安全基础

推荐产品，助您构建稳健的安全态势。

Google Cloud Cybershield™

强化全国范围的网络防御。

初创企业与中小企业

借助量身定制的解决方案与计划，加速初创企业与中小企业的成长。

初创企业计划

获取财务、业务和技术支持，让您的初创企业更上一层楼。

中小企业

探索用于 Web 托管、应用开发、AI 和分析的解决方案。

软件即服务（SaaS）

构建更优质的 SaaS 产品，高效扩缩容，并发展您的业务。

关闭

精选产品

AI 与机器学习

商业智能

计算

容器

数据分析

数据库

开发者工具

分布式云

混合云与多云

行业专用

集成服务

管理工具

地图与地理空间

媒体服务

迁移

混合现实

网络

运维

办公与协作

安全与身份

无服务器

存储

Web3

查看所有产品（100+）

精选产品

Compute Engine

在 Google 数据中心运行的虚拟机。

Cloud Storage

安全、持久且可扩展的对象存储。

BigQuery

用于分析和数据科学的自主数据到 AI 平台。

Cloud Run

用于运行容器化应用的完全托管环境。

Google Kubernetes Engine

用于运行容器化应用的托管环境。

Vertex AI

统一平台，用于机器学习模型与生成式 AI。

Looker

用于 BI、数据应用和嵌入式分析的平台。

Apigee API Management

随时随地管理 API 的完整生命周期，兼具可视化与管控能力。

Cloud SQL

面向 MySQL、PostgreSQL 和 SQL Server 的关系型数据库服务。

Gemini Enterprise

用于发现、创建、运行和治理 AI 智能体的安全平台。

Cloud CDN

用于分发网页和视频的内容分发网络。

没找到您想要的内容？

查看全部产品（100+）

AI 与机器学习

Vertex AI Platform

用于机器学习模型和生成式 AI 的统一平台。

Vertex AI Studio

在 Vertex AI 上构建、调优和部署基础模型。

Vertex AI Agent Builder

构建和部署生成式 AI 体验。

Conversational Agents

利用确定性的功能和生成式 AI 功能构建对话式 AI。

Vertex AI Search

为你的企业应用与体验构建 Google 级品质的搜索。

Speech-to-Text

覆盖 125 种语言的语音识别与转写。

Text-to-Speech

提供 220+ 种音色、40+ 种语言的语音合成。

Translation AI

语言检测、翻译与术语表支持。

Gemini 企业版

用于发现、创建、运行和治理智能体（agent）的安全平台。

Vision AI

用于检测情绪、文本等内容的定制模型与预训练模型。

联络中心即服务

原生云的全渠道联络中心解决方案。

没有找到您想要的内容？

查看所有 AI 与机器学习产品

商业智能

Looker

用于 BI、数据应用和嵌入式分析的平台。

Looker Studio

用于仪表盘、报表和分析的交互式数据套件。

计算

Compute Engine

运行在 Google 数据中心的虚拟机。

App Engine

面向应用与后端的无服务器应用平台。

Cloud GPUs

用于机器学习、科学计算和 3D 可视化的 GPU。

迁移到虚拟机

将服务器和虚拟机迁移到 Compute Engine。

Spot 虚拟机

适用于批处理作业和容错工作负载的计算实例。

Batch

用于调度批处理作业的全托管服务。

独占租户节点

用于满足合规、许可和管理需求的专用硬件。

裸金属

在 Google Cloud 上运行专用工作负载的基础设施。

Recommender

针对 Google Cloud 产品和服务的使用建议。

VMware Engine

全托管的原生 VMware Cloud Foundation 软件堆栈。

Cloud Run

用于运行容器化应用的完全托管环境。

没找到您想要的内容？

查看所有计算产品

容器

Google Kubernetes Engine

用于运行容器化应用的托管环境。

Cloud Run

用于运行容器化应用的完全托管环境。

Cloud Build

在 Docker 容器中运行构建步骤的解决方案。

Artifact Registry

用于构建产物和依赖项的包管理器。

Cloud Code

IDE 支持编写、运行和调试 Kubernetes 应用程序。

Cloud Deploy

面向 GKE 和 Cloud Run 的全托管持续交付。

Migrate to Containers

用于将虚拟机迁移为 GKE 上系统容器的组件。

Deep Learning Containers

包含数据科学框架、库和工具的容器。

Knative

用于创建 Kubernetes 原生的云端软件的组件。

数据分析

BigQuery

面向分析与数据科学的自主化数据到 AI 平台。

Looker

BI、数据应用与嵌入式分析的平台。

Dataflow

面向流处理与批处理的实时分析。

Pub/Sub

用于事件摄取与投递的消息服务。

Dataproc

用于运行 Apache Spark 和 Apache Hadoop 集群的托管服务。

Google Cloud Serverless for Apache Spark

虚拟机快速启动，并针对 Spark 工作负载动态自动扩缩容。

Cloud Composer

基于 Apache Airflow 构建的工作流编排服务。

BigLake

借助 Apache Iceberg 构建数据湖仓的存储引擎。

Dataplex Universal Catalog

面向所有 Google Cloud 服务的统一数据到 AI 治理网格。

BigQuery Migration Services

免费使用、云原生且由 AI 驱动的数据迁移服务。

Managed Service for Apache Kafka

用于运维高可用 Apache Kafka 集群的受管 Kafka 服务。

没找到您想要的内容？

查看所有数据分析产品

数据库

AlloyDB for PostgreSQL

面向企业级工作负载的全托管、兼容 PostgreSQL 的数据库。

Cloud SQL

适用于 MySQL、PostgreSQL 和 SQL Server 的全托管数据库。

Firestore

高度可扩缩容的无服务器 NoSQL 文档数据库，兼容 MongoDB。

Spanner

具备无限扩缩容能力和 99.999% 可用性的云原生关系型数据库。

Bigtable

面向大规模、低延迟工作负载的云原生宽列数据库。

Datastream

无服务器变更数据捕获与复制服务。

数据库迁移服务

无服务器、最短停机时间迁移至 Cloud SQL。

裸金属解决方案

为你的 Oracle 工作负载提供全托管基础设施。

Memorystore

全托管 Redis 和 Memcached，实现亚毫秒级数据访问。

开发者工具

Artifact Registry

用于构建产物和依赖项的通用包管理器。

Cloud Code

IDE 支持编写、运行和调试 Kubernetes 应用程序。

Cloud Build

持续集成与持续交付平台。

Cloud Deploy

面向 GKE 和 Cloud Run 的全托管持续交付服务。

Cloud Deployment Manager

用于创建和管理 Google Cloud 资源的服务。

Cloud SDK

用于 Google Cloud 的命令行工具与库。

Cloud Scheduler

用于任务自动化与管理的 Cron 作业调度器。

Cloud Source Repositories

用于存储、管理和追踪代码的私有 Git 仓库。

基础设施管理器

使用 Terraform 自动化基础设施管理。

Cloud Workstations

云端托管且安全的开发环境。

Gemini Code Assist

可在 Google Cloud 及你的 IDE 中使用的 AI 驱动助手。

没找到你想要的内容？

查看所有开发者工具

分布式云

Google Distributed Cloud Connected

面向边缘工作负载的分布式云服务。

Google Distributed Cloud Air-gapped

面向气隙隔离工作负载的分布式云。

混合云与多云

Google Kubernetes Engine

用于运行容器化应用的托管环境。

Apigee API Management

API 管理、开发与安全平台。

Migrate to Containers

用于将工作负载和现有应用迁移到 GKE 的工具。

Cloud Build

用于在 Google Cloud 基础设施上执行构建的服务。

可观测性

监控、日志记录与应用性能套件。

Cloud Service Mesh

基于 Envoy 和 Istio 的全托管服务网格。

Google Distributed Cloud

面向边缘和数据中心的完全托管解决方案。

行业专用

Anti Money Laundering AI

借助 AI 检测可疑的潜在洗钱活动。

Cloud Healthcare API

用于在 Google Cloud 上打通现有照护系统与应用的解决方案。

Device Connect for Fitbit

借助 Google Cloud 上连接的 Fitbit 数据，获得 360 度患者视图。

电信网络自动化

为电信网络提供开箱即用的云原生自动化。

电信数据编织（Data Fabric）

以自动化方式开展电信数据管理与分析。

电信用户洞察

摄取数据，以提升用户获取与留存。

频谱接入系统（SAS）

管控对公民宽带无线电服务（CBRS）的基础接入。

集成服务

应用集成

无需编写代码即可连接第三方应用并实现数据一致性。

工作流

为无服务器产品与 API 服务提供工作流编排。

Apigee API 管理

随时随地管理 API 的完整生命周期，兼具可见性与控制力。

Cloud Tasks

用于异步任务执行的任务管理服务。

Cloud Scheduler

用于任务自动化与管理的 Cron 作业调度器。

Dataproc

用于运行 Apache Spark 和 Apache Hadoop 集群的服务。

Cloud Data Fusion

用于构建和管理数据流水线的数据集成服务。

Cloud Composer

基于 Apache Airflow 构建的工作流编排服务。

Pub/Sub

用于事件摄取与投递的消息传递服务。

Eventarc

构建可连接任意服务的事件驱动架构。

管理工具

Cloud Shell

内置命令行的交互式 shell 环境。

Cloud console

用于管理和监控云应用的 Web 界面。

Cloud Endpoints

用于管理 Google Cloud 上 API 的部署与开发。

Cloud IAM

Google Cloud 资源的权限管理系统。

Cloud API

面向 Google Cloud 服务的编程接口。

服务目录

供管理员管理内部企业解决方案的服务目录。

成本管理

用于监控、控制和优化成本的工具。

可观测性

监控、日志记录与应用性能套件。

碳足迹

用于查看和导出 Google Cloud 碳排放报告的仪表板。

Config Connector

Kubernetes 用于管理 Google Cloud 资源的附加组件。

Active Assist

轻松管理性能、安全性与成本的工具。

没有找到您想要的内容？

查看所有管理工具

地图与地理空间

Earth Engine

用于地球观测数据分析的地理空间平台。

Google Maps Platform

打造沉浸式位置体验，优化业务运营。

媒体服务

Cloud CDN

用于分发 Web 和视频内容的内容分发网络。

Live Stream API

将直播视频转码并封装以供流式传输的服务。

OpenCue

面向视觉特效与动画的开源渲染管理器。

Transcoder API

转换视频文件并封装，以实现优化传输。

Video Stitcher API

用于动态广告插入或服务器端广告插入的服务。

迁移

迁移中心

在 Google Cloud 上进行迁移与现代化的统一平台。

应用迁移

将应用迁移到云端，以实现低成本的更新周期。

迁移到虚拟机

用于将虚拟机和物理服务器迁移到 Compute Engine 的组件。

Cloud Foundation Toolkit

Deployment Manager 和 Terraform 的参考模板。

数据库迁移服务

无服务器、停机时间极短的 Cloud SQL 迁移方案。

迁移到容器

用于将虚拟机迁移为 GKE 上系统容器的组件。

BigQuery 迁移服务

简化的数据仓库与数据湖迁移工具及激励措施。

快速迁移与现代化计划

端到端迁移计划，简化你的上云之路。

Transfer Appliance

用于将海量数据迁移到 Google Cloud 的存储服务器。

Storage Transfer Service

将在线数据源和本地数据源的数据传输到 Cloud Storage。

VMware Engine

在 Google Cloud 上原生迁移并运行你的 VMware 工作负载。

混合现实

Immersive Stream for XR

托管、渲染并流式传输 3D 与 XR 体验。

网络

Cloud Armor

安全策略，防御 Web 与 DDoS 攻击。

Cloud CDN 和 Media CDN

用于分发 Web 和视频内容的内容分发网络。

Cloud DNS

域名系统，提供可靠、低延迟的名称解析。

Cloud Load Balancing

用于在多个应用与区域之间分配流量的服务。

Cloud NAT

NAT 服务，为私有实例提供互联网访问能力。

Cloud Connectivity

面向 VPN、对等互连及企业需求的连接方案。

网络连接中心

连接管理，帮助简化和扩展网络。

网络智能中心

网络监控、验证与优化平台。

网络服务层级

基于性能、可用性和成本的云网络选项。

虚拟私有云

整个组织共用一个 VPC，并在项目内相互隔离。

专用服务连接

在你的 VPC 与服务之间建立安全连接。

没找到你要找的内容？

查看所有网络产品

运维

Cloud Logging

Google Cloud 审计、平台与应用日志管理。

Cloud Monitoring

借助丰富的指标监控基础设施与应用健康状态。

Error Reporting

应用错误识别与分析。

Managed Service for Prometheus

Google Cloud 上全托管的 Prometheus。

Cloud Trace

从应用收集延迟数据的链路追踪系统。

Cloud Profiler

用于分析应用性能的 CPU 和堆分析器。

云配额

管理所有 Google Cloud 服务的配额。

效率与协作

AppSheet

用于构建和扩展应用的无代码开发平台。

Gemini 企业版

用于发现、创建、运行和治理 AI 智能体的安全平台。

Google Workspace

面向个人和组织的协作与效率工具。

Google Workspace Essentials

面向团队的安全视频会议与现代化协作。

Cloud Identity

供 IT 管理员管理用户设备与应用的统一平台。

Chrome Enterprise

为企业打造的 ChromeOS、Chrome 浏览器与 Chrome 设备。

安全与身份

Cloud IAM

面向 Google Cloud 资源的权限管理系统。

敏感数据保护

发现、分类并保护你宝贵的数据资产。

Mandiant 托管防御

全天候 24×7 从容发现并消除威胁。

Google 威胁情报

了解谁在针对你。

Security Command Center

用于防御针对你的 Google Cloud 资产所受威胁的平台。

Cloud Key Management

在 Google Cloud 上管理加密密钥。

Mandiant Incident Response

最大程度降低入侵泄露的影响。

Chrome Enterprise Premium

获得安全的企业级浏览体验，并具备广泛的端点可见性。

Assured Workloads

面向敏感工作负载的合规与安全管控。

Google Security Operations

检测、调查并响应网络威胁。

Mandiant Consulting

在故障事件发生前、中、后获取专家指导。

没找到你想要的内容？

查看所有安全与身份产品

无服务器

Cloud Run

用于运行容器化应用的全托管环境。

Cloud Functions

用于创建响应云端事件的函数的平台。

App Engine

面向应用与后端的无服务器应用平台。

工作流

面向无服务器产品与 API 服务的工作流编排。

API 网关

借助全托管网关开发、部署、保护和管理 API。

存储

云存储

安全、持久且可扩展的对象存储。

块存储

面向 AI、数据分析、数据库和企业应用的高性能存储。

Filestore

高度可扩展且安全的文件存储。

Persistent Disk

为运行在 Google Cloud 上的虚拟机实例提供的块存储。

Cloud Storage for Firebase

用于存储和分发用户生成内容的对象存储。

Local SSD

本地挂载的块存储，满足高性能需求。

Storage Transfer Service

将数据从在线数据源和本地数据源传输到 Cloud Storage。

Google Cloud Managed Lustre

高性能托管并行文件服务。

Google Cloud NetApp Volumes

适用于 NFS、SMB 及多协议环境的文件存储服务。

Backup and DR Service

用于集中式、应用一致性数据保护的服务。

Web3

区块链节点引擎（Blockchain Node Engine）

全托管的节点托管服务，用于在区块链上进行开发。

区块链 RPC

企业级 RPC，用于在区块链上构建应用。

关闭

以透明的定价方式帮您节省开支

Google Cloud 的按需付费定价会根据月度用量自动为您节省费用，预付费资源还可享受折扣费率。立即联系我们获取报价。

申请报价

定价概览与工具

Google Cloud 定价

只为实际用量付费，无供应商锁定。

价格计算器

算算你能在云上省下多少钱。

Google Cloud 免费层级

探索提供每月免费额度的产品。

成本优化框架

获取优化工作负载成本的最佳实践。

成本管理工具

用于监控和管控成本的工具。

各产品定价

Compute Engine

Cloud SQL

Google Kubernetes 引擎

Cloud Storage

BigQuery

查看 100+ 款产品的完整价格清单

关闭

学习与构建

Google Cloud 免费计划

赠送 $300 免费额度及 20+ 款免费产品。

解决方案生成器

获取 AI 生成的解决方案建议。

快速入门

获取教程与分步讲解。

博客

阅读我们的最新产品动态与故事。

学习中心

通过基于角色的培训拓展你的职业发展。

Google Cloud 认证

备考并报名参加认证。

云计算基础

进一步了解云计算基础知识。

云架构中心

获取参考架构与最佳实践。

关注我们

创新者

加入 Google Cloud 开发者计划。

开发者中心

掌握最新动态，保持紧密联系。

活动与网络研讨会

浏览即将举行和点播回看的活动。

Google Cloud 社区

提问、寻找答案，并与他人建立联系。

咨询与合作伙伴

Google Cloud 咨询

与我们的专家携手开展云项目。

Google Cloud Marketplace

只需点击几下，即可部署开箱即用的解决方案。

寻找合作伙伴

了解与合作伙伴协作的优势。

Google Cloud 合作伙伴

了解生态系统与资源。

关闭

概览

arrow_forward

解决方案

arrow_forward

产品

arrow_forward

定价

arrow_forward

资源

arrow_forward

文档

支持

控制台

加速你的数字化转型

了解更多

核心优势

为什么选择 Google Cloud

AI 与机器学习

多云

全球基础设施

数据云

现代基础设施云

安全

生产力与协作

报告与洞察

高管洞察

分析师报告

白皮书

客户案例

行业解决方案

零售

消费品

金融服务

医疗与生命科学

媒体与娱乐

电信

游戏

制造业

供应链与物流

政府

教育

查看所有行业解决方案

查看所有解决方案

应用现代化

CAMP

传统应用现代化

从 PaaS 迁移：Cloud Foundry、Openshift

从大型机迁移

软件交付现代化

DevOps 最佳实践

SRE 原则

平台工程

在边缘运行应用

面向多云架构设计

转向无服务器

人工智能

基于 Google AI 的客户互动套件

Document AI

面向电商的 Vertex AI Search

Google Cloud 搭配 Gemini

Google Cloud 上的生成式 AI

API 与应用

利用 API 开拓新业务渠道

利用 API 释放遗留应用的潜力

Open Banking APIx

数据分析

数据迁移

数据湖仓

实时分析

营销分析

数据集

商业智能

面向数据分析的 AI

地理空间分析

数据库

数据库迁移

数据库现代化

游戏数据库

Google Cloud 数据库

将 Oracle 工作负载迁移至 Google Cloud

开源数据库

Google Cloud 上的 SQL Server

用于数据库的 Gemini

基础设施现代化

应用迁移

Google Cloud 上的 SAP

高性能计算

Google Cloud 上的 Windows

数据中心迁移

Active Assist

虚拟桌面

快速迁移与现代化计划

备份与灾难恢复

Google Cloud 上的 Red Hat

跨云网络

可观测性

生产力与协作

Google Workspace

Google Workspace Essentials

Cloud Identity

Chrome Enterprise

安全

智能体化 SOC

Web 应用与 API 防护

安全与韧性框架

风险与合规即代码（RCaC）

软件供应链安全

安全基础

Google Cloud Cybershield™

初创企业与中小企业

初创企业计划

中小企业

软件即服务

精选产品

Compute Engine

Cloud Storage

BigQuery

Cloud Run

Google Kubernetes Engine

Vertex AI

Looker

Apigee API Management

Cloud SQL

Gemini Enterprise

Cloud CDN

查看全部产品（100 多个）

AI 与机器学习

Vertex AI 平台

Vertex AI Studio

Vertex AI 智能体构建器

对话式智能体

Vertex AI 搜索

语音转文本

文本转语音

翻译 AI

Gemini 企业版

视觉 AI

联络中心即服务

查看所有 AI 与机器学习产品

商业智能

Looker

Looker Studio

计算

Compute Engine

App Engine

Cloud GPU

迁移到虚拟机

Spot 虚拟机

Batch

独占租户节点

裸金属

Recommender

VMware Engine

Cloud Run

查看所有计算产品

容器

Google Kubernetes Engine

Cloud Run

Cloud Build

Artifact Registry

Cloud Code

Cloud Deploy

迁移到容器

深度学习容器

Knative

数据分析

BigQuery

Looker

Dataflow

Pub/Sub

Dataproc

Google Cloud Serverless for Apache Spark

Cloud Composer

BigLake

Dataplex Universal Catalog

BigQuery 迁移服务

Apache Kafka 托管服务

查看所有数据分析产品

数据库

AlloyDB for PostgreSQL

Cloud SQL

Firestore

Spanner

Bigtable

Datastream

数据库迁移服务

裸金属解决方案

Memorystore

开发者工具

Artifact Registry

Cloud Code

Cloud Build

Cloud Deploy

Cloud Deployment Manager

Cloud SDK

Cloud Scheduler

Cloud Source Repositories

Infrastructure Manager

Cloud Workstations

Gemini Code Assist

查看所有开发者工具

分布式云

Google Distributed Cloud Connected

Google Distributed Cloud Air-gapped

混合云与多云

Google Kubernetes Engine

Apigee API 管理

迁移到容器

Cloud Build

可观测性

Cloud Service Mesh

Google 分布式云

行业专用

反洗钱 AI

Cloud Healthcare API

Fitbit 设备连接

电信网络自动化

电信数据编织

电信用户洞察

频谱接入系统（SAS）

集成服务

应用集成

工作流

Apigee API 管理

Cloud Tasks

Cloud Scheduler

Dataproc

Cloud Data Fusion

Cloud Composer

Pub/Sub

Eventarc

管理工具

Cloud Shell

Cloud 控制台

Cloud Endpoints

云 IAM

云 API

服务目录

成本管理

可观测性

碳足迹

Config Connector

Active Assist

查看所有管理工具

地图与地理空间

Earth Engine

Google Maps Platform

媒体服务

Cloud CDN

Live Stream API

OpenCue

Transcoder API

Video Stitcher API

迁移

Migration Center

Application Migration

Migrate to Virtual Machines

Cloud Foundation Toolkit

Database Migration Service

迁移至容器

BigQuery 迁移服务

快速迁移与现代化计划

Transfer Appliance

存储传输服务

VMware Engine

混合现实

面向 XR 的沉浸式串流

网络

Cloud Armor

Cloud CDN 和 Media CDN

Cloud DNS

Cloud Load Balancing

Cloud NAT

Cloud 连接

Network Connectivity Center

Network Intelligence Center

网络服务层级

虚拟私有云

Private Service Connect

查看所有网络产品

运维

Cloud Logging

Cloud Monitoring

错误报告

代管式 Prometheus 服务

Cloud Trace

Cloud Profiler

Cloud Quotas

工作效率与协作

AppSheet

Gemini Enterprise

Google Workspace

Google Workspace Essentials

Cloud Identity

Chrome Enterprise

安全与身份

Cloud IAM

敏感数据保护（Sensitive Data Protection）

Mandiant 托管防御（Mandiant Managed Defense）

Google 威胁情报（Google Threat Intelligence）

安全指挥中心（Security Command Center）

云密钥管理（Cloud Key Management）

Mandiant 事件响应（Mandiant Incident Response）

Chrome Enterprise Premium

受保障工作负载（Assured Workloads）

Google 安全运营（Google Security Operations）

Mandiant 咨询（Mandiant Consulting）

查看所有安全与身份产品

无服务器

Cloud Run

Cloud Functions

App Engine

Workflows

API Gateway

存储

Cloud Storage

Block Storage

Filestore

Persistent Disk

Firebase 云存储

本地 SSD

存储传输服务

Google Cloud 托管 Lustre

Google Cloud NetApp 卷

备份与灾难恢复服务

Web3

区块链节点引擎

区块链 RPC

借助透明的定价方式节省开支

申请报价

定价概览与工具

Google Cloud 定价

定价计算器

Google Cloud 免费层级

成本优化框架

成本管理工具

按产品划分的定价

Compute Engine

Cloud SQL

Google Kubernetes Engine

Cloud Storage

BigQuery

查看涵盖 100 多款产品的完整价格列表

学习与构建

Google Cloud 免费计划

解决方案生成器

快速入门

博客

学习中心

Google Cloud 认证

云计算基础

云架构中心

连接

创新者

开发者中心

活动与网络研讨会

Google Cloud 社区

咨询与合作伙伴

Google Cloud 咨询

Google Cloud Marketplace

寻找合作伙伴

Google Cloud 合作伙伴