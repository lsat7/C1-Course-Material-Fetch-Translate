<!-- source: pdfs/ai-assisted-code-review-assessment.pdf pages=9 -->

# AI 辅助代码评审评估

现代代码评审中编码实践的 AI 辅助评估
Manushree Vijayvergiya
manushree@google.com
Google
瑞士苏黎世
Małgorzata Salawa
magorzata@google.com
Google
瑞士苏黎世
Ivan Budiselić
ibudiselic@google.com
Google
瑞士苏黎世
Dan Zheng
danielzheng@google.com
Google
美国山景城
Pascal Lamblin
lamblinp@google.com
Google
加拿大蒙特利尔
Marko Ivanković
markoi@google.com
Google
瑞士苏黎世
Juanjo Carin
juanjocarin@google.com
Google
美国森尼韦尔
Mateusz Lewko
mlewko@google.com
Google
瑞士苏黎世
Jovan Andonov
jandonov@google.com
Google
瑞士苏黎世
Goran Petrović
goranpetrovic@google.com
Google
瑞士苏黎世
Daniel Tarlow
dtarlow@google.com
Google
加拿大蒙特利尔
Petros Maniatis
maniatis@google.com
Google
美国山景城
René Just∗
rjust@cs.washington.edu
华盛顿大学
美国西雅图
摘要
现代代码评审是一个过程：代码作者做出的增量代码贡献在提交到版本控制系统之前，由一位或多位同行进行评审。现代代码评审的一个重要组成部分是验证代码贡献是否遵循最佳实践。

虽然其中一些最佳实践可以自动验证，但其他实践的验证通常留给人类评审者。本文报告了 AutoCommenter 的开发、部署和评估，这是一个由大语言模型支持、可自动学习和执行编码最佳实践的系统。我们为四种编程语言（C++、Java、Python 和 Go）实现了 AutoCommenter，并在大型工业环境中评估了其性能和采用情况。我们的评估表明，用于学习和执行编码最佳实践的端到端系统是可行的，并且对开发者工作流有积极影响。此外，本文还报告了将此类系统部署给数万名开发者所面临的挑战以及相应的经验教训。CCS CONCEPTS
• 软件及其工程 → 软件验证与确认。∗在 Google 完成的工作。允许出于个人或课堂使用目的，免费制作本作品全部或部分的数字或硬拷贝，前提是不得为盈利或商业优势制作或分发副本，并且副本在第一页保留此声明和完整引用。

本作品中第三方组件的版权必须得到尊重。用于所有其他用途时，请联系所有者/作者。AIware ’24，2024 年 7 月 15–16 日，巴西 Porto de Galinhas
© 2024 版权归所有者/作者所有。ACM ISBN 979-8-4007-0685-1/24/07
https://doi.org/10.1145/3664646.3665664
关键词
人工智能、代码评审、编码最佳实践
ACM 引用格式：
Manushree Vijayvergiya, Małgorzata Salawa, Ivan Budiselić, Dan Zheng, Pascal Lamblin, Marko Ivanković, Juanjo Carin, Mateusz Lewko, Jovan Andonov, Goran Petrović, Daniel Tarlow, Petros Maniatis, 和 René Just. 2024. 现代代码评审中编码实践的 AI 辅助评估. In Proceedings of the 1st ACM International Conference on AI-Powered Software (AIware ’24), July 15–16, 2024, Porto de Galinhas, Brazil. ACM, New York, NY, USA, 9 pages. https://doi.org/10.1145/3664646.3665664
1
引言
现代代码评审 [21, 23]（相对于整体代码评审 [8]）多年来在开源和工业环境中自然发展。一套常见的同行评审标准已经形成 [5, 20, 21]，其中包括编码最佳实践。

许多公司、项目，甚至编程语言都以“风格指南” [1–4] 的形式正式定义它们，这些指南通常涵盖以下方面：
• 格式：行长度限制、空白字符和缩进的使用、圆括号和方括号的位置等；
• 命名：大小写、简洁性、描述性等；
• 文档：文件级、函数级及其他注释的预期位置和内容；
• 语言特性：在不同（代码）语境中使用特定语言特性；
• 代码惯用法：使用代码惯用法以提高代码清晰性、模块化和可维护性。开发者通常对现代代码评审流程表示高度满意 [23, 28]。其主要好处之一是为不熟悉代码库、特定语言特性或常见代码惯用法的代码作者提供学习体验。在评审过程中，资深开发者会向代码作者传授最佳实践，除了
arXiv:2405.13565v1  [cs.SE]  22 May 2024

AIware ’24，2024 年 7 月 15–16 日，巴西 Porto de Galinhas
Manushree Vijayvergiya 等
评审（并学习）代码贡献及其影响外，像 linter [15] 这样的静态分析工具可以自动验证代码是否遵循某些最佳实践（例如格式规则），有些工具甚至可以自动修复违规。然而，细微的指南或带有例外的指南很难被整体自动验证（例如命名约定和遗留代码中有正当理由的偏离），而有些指南根本无法用精确规则来捕捉（例如代码注释的清晰性和具体性），它们依赖人的判断和开发者的集体知识。因此，通常期望人类评审者检查代码变更是否违反最佳实践。代码评审流程的最大成本是需要投入的时间，尤其是资深开发者的时间。即使已经实现了大量自动化，并且尽可能保持流程轻量，开发者每天也很容易在这项任务上投入数小时 [23]。

近期机器学习的进展，尤其是大语言模型（LLM）展现出的能力，表明 LLM 适合用于代码评审自动化（例如 [11, 16, 17, 24–26]）。然而，围绕大规模部署端到端系统所面临的软件工程挑战仍未被探索。同样，针对此类系统在整体有效性和用户接受度方面的外部评估也尚付阙如。本文研究是否有可能部分实现代码评审流程的自动化，具体而言即对最佳实践违规的检测，从而为代码作者提供及时反馈，并让评审者能够专注于整体功能。具体而言，本文报告了我们在 Google 的工业环境中开发、部署并评估 AutoCommenter——一款自动化代码评审助手——的经验，该工具目前每天被数万名开发者使用。总结来说，本文的贡献如下：
• 一套基于 LLM 的代码评审助手系统通用架构（第 3 节）。• 工具校准以及面向数万名开发者的部署的描述（第 4 节）。• 对该系统的评估（第 5 节）。

• 对经验教训的总结与讨论（第 6 节）。2
背景
AutoCommenter 是在 Google 的大型工业环境中开发出来的。Google 的现代代码评审实践与其他工业界和开源项目相似 [23]。2.1
代码评审流程
Google 的代码评审流程成熟完善、基于变更并以工具辅助。Ivanković 等人 [12] 和 Petrović 等人 [18] 对该流程做了详细总结。对代码库的每一次变更都必须至少由另一位开发者评审。每天有数万项代码库变更经历评审流程，数万名开发者以代码作者和评审者的双重身份参与其中。作者和评审者通过代码评审系统交换评论，评审则沿着变更所涉及文件的各个快照逐步推进。每条评审者评论都附着在某一特定文件快照的特定行、列范围上。为处理（resolve）一条评论，作者通常会在本地副本中修改相应文件，并导出一个新快照用于下一轮代码评审。
图 1：人工评审者发布的评论示例。

当作者和所有评审者都满意，且没有任何自动化分析阻塞合并时，代码就会被合并进代码库。代码评审流程中最昂贵的部分是代码作者和评审者“照管”一项变更所花费的时间（从最初的编码，到处理评审者评论并确保所有自动化分析通过，最终将变更合并进代码库）。尽管该流程已通过自动化系统在评审前分析代码得到了优化（尤其是无需人工介入的自动代码格式化），代码评审每年仍要耗费数千开发者年。因此，即便是个位数的百分比节省，也会转化为显著的商业影响。2.2
最佳实践
最佳实践是指某种被认为更优的编程语言具体用法，而最佳实践文档则描述它应当如何应用以及能带来哪些好处。最佳实践 URL 指一份最佳实践文档或其中的某个具体章节，最佳实践违规指某段具体代码未遵循某项最佳实践，但可以通过修改来遵循。

若根据上下文含义明确，我们用术语 URL 和“违规”分别指代最佳实践 URL 和最佳实践违规。Google 的中心代码仓库包含多种语言的代码，其中 C++、Java、Python 和 Go 每一种都超过 1 亿行 [19]。针对 15 种不同的语言，都有对所有开发者随时可用的正式风格指南。其中许多语言还有额外的语言入门资料、核心库文档以及“每周提示”式的简报。虽然这些材料不像风格指南那样被严格执行，但它们在代码评审中被频繁引用。有些语言的此类文档多达数百页。代码作者和评审者都被要求确认代码遵循了所有最佳实践。十多年前引入的一种名为“可读性（readability）”的正式机制，确保最佳实践得到一致遵循。每种语言中专门的风格专家被称为“可读性导师”，负责引导经验不足的开发者逐步精通该语言 [23]。

可读性导师通常用几句话概括某项最佳实践，并在评论末尾附上一个 URL 供变更作者参考。图 1 展示了一位可读性导师发布的评论示例。

现代代码评审中编码实践的 AI 辅助评估
AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil
训练与微调（按需）
工作节点
工作节点
工作节点
源代码仓库
评论存储
调度器
相关代码评论
工作节点
工作节点
工作节点
示例（按时间切分）
工作节点
工作节点
TPU pod
Tensorboard
模型检查点
输入/目标格式
大规模预处理（周期性）
数据集整理（按需）
图 2：模型训练流水线的架构。可读性流程存在一些缺点。对作者而言，由于需要额外的评审轮次，它会拉长开发时间。对可读性导师而言，它可能变成一项单调而耗时的任务。它要求掌握数百条不断演进的最佳实践，包括识别并废弃过时的规则，并在代码评审系统中（附带相关链接地）记录它们。此外，它还要求持续跟踪（有时要经过多轮迭代），确保所有违规都已被纠正。3
方法
针对 2.1 节和 2.2 节所述的挑战，我们开发了 AutoCommenter，一款自动检测最佳实践违规的代码分析工具。

它旨在为代码作者提供及时反馈，并减少人工最佳实践评审的需求，从而使评审者能够专注于代码功能。3.1
模型与任务定义
要实现最佳实践分析的自动化，需要一个能够表示源代码、精确定位违规位置并识别所违反的最佳实践的模型。我们采用基于 T5 的传统 transformer 方法、使用 T5X [22]，目标是完成文本到文本的转换。最佳实践分析是多任务大序列模型中的一项任务。除了 T5 的标准预训练任务——片段去噪（预测被掩码的词元）——之外，用于训练该模型的其他任务还包括代码评审评论处理、下一次编辑预测、变量重命名和构建错误修复 [9]。训练语料由超过 30 亿条示例构成，其中最佳实践分析数据集贡献约 80 万条示例。该模型使用此类模型常用的标准交叉熵损失进行训练，并以最大化序列准确率指标为目标进行调优，即为每条示例预测出完全正确的目标文本。

对于最佳实践分析，模型的输入是一项任务 prompt 和源代码，目标是源代码位置以及针对某处最佳实践违规的 URL。任务 prompt 被格式化为固定文本的代码注释，采用该编程语言恰当的注释风格。它以自然语言描述任务，并置于源代码之前，源代码则是某个文件的直接文本表示。如果输入超出模型的上下文窗口，就会被截断。位置是源代码中的字节偏移量，URL 则指向被违反的最佳实践。目标格式由一种领域特定语言定义，其中一种特殊情况是“空”目标，即不存在任何违规时。除目标之外，模型还会输出一个 0 到 1 之间的置信度分数。请看下面这个 Go 语言的输入/目标示例。输入
/ /
[ ∗]
Task :
Check
language
b e s t
p r a c t i c e s . / /
Package
a d d i t i o n
p r o v i d e s
Add
package
a d d i t i o n
/ /
Return a sum
func Add ( value1 ,
value2
int )
int
{
return
value1 + value2
}
目标
INSERT 153 COMMENT h t t p s : / / go .

dev / doc / comment # func
输入的第一行是固定文本的任务 prompt；其余部分是源代码。目标给出了位置（字节偏移量 153 对应 Add 函数的起始处）以及一个 go.dev 的 URL，指向该函数注释所违反的 Go 语言风格指南中的确切部分（此例中，即注释应以函数名开头这一惯常做法）。请注意，根据源代码中违规的数量，目标可能包含零个、一个或多个（拼接的）位置-URL 对。3.2
模型训练
图 2 展示了模型训练流水线的架构，它由三部分组成。我们把数据集创建拆分为两个步骤（预处理与整理），因为第一步处理的数据量大得多，代价也显著更高。预处理步骤的输出与模型的输入/目标表示无关。这种分离让示例表示和其他示例层面的调整能够快速迭代，从而提升特性开发速度。

预处理步骤使用容错调度系统，周期性地抽取相关代码评论，以确保新数据随时可用。3.2.1
大规模预处理。训练示例由真实代码评审数据生成，但并非所有代码评论都适合用于模型训练。因此，预处理步骤会识别相关代码评论——即包含指向最佳实践文档的 URL 的人工撰写评论。随后，预处理步骤会为每条评论收集相应的源代码及相关元数据，包括评论在源代码中的位置及其创建时间。该步骤的输出是一组相关代码评论，每条都带有为模型训练整理示例所需的全部数据。

AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil
Manushree Vijayvergiya et al. 3.2.2
数据集整理。数据集整理是一个单一的、按需执行的处理步骤，以 Beam1 流水线实现。它依据 3.1 节所述的输入/目标格式，把每条相关代码评论转换为标准的 TensorFlow Example 数据结构。3.2.3
训练与微调。整理好的示例直接用于模型训练和评估。我们在一组 TPU 集群上使用 T5X 框架 [22]，每 1000 步保存一次模型检查点，并使用 Tensorboard 监控训练。3.3
模型选择
基于历史数据的两项内在评估，指导我们选择模型检查点、置信度阈值和解码策略。第一项是在验证集和测试集上的评估，给出按文件计算的精确率和召回率估计。第二项是在全部历史代码评审上的评估，给出每次代码评审的评论总数估计，从而反映开发者与 AutoCommenter 交互的频率。3.3.1
在验证集和测试集上的评估。

我们按时间切分数据集，以确保模型未在验证集和测试集中代码评论的未来代码评审快照上训练过。在我们的数据集中，85% 的文件恰好有一条相关代码评论，11% 有两条，4% 有三条或更多。如果预测出的代码位置和 URL 与期望值一致（不论顺序），我们就将该预测定义为正确。请回想一下，模型会为每个预测给出置信度分数，这引入了另一个参数：若某个预测的置信度分数低于某个阈值 𝑡，该预测可被抑制。我们定义 𝑃𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛𝑡 为置信度分数大于 𝑡 的正确预测数，除以置信度分数大于 𝑡 的全部预测数；𝑅𝑒𝑐𝑎𝑙𝑙𝑡 的定义与此类似。这些定义使我们能够估计，作为 𝑡 的函数，会有多少（不）正确结果展示给用户。训练期间，我们用 𝑃𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛𝑡 和 𝑅𝑒𝑐𝑎𝑙𝑙𝑡 来比较不同的模型检查点。

尽管这种评估避免了数据泄漏，并允许我们自动评估模型性能，但它有一个局限：虽然可以合理假设给定代码评审（code review）快照的人工评论是正确的，但它们并不详尽。换句话说，给定代码评审快照中的代码可能会根据多条最佳实践得到改进，但人工评审者并没有为所有这些改进都发布评论（带有 URL）。这可能出于多种原因：
• 缺少参考：评审者可能评论了某个问题，但没有包含 URL 作为参考。
• 选择性评论：评审者可能只评论一次某个问题，期望作者在整处代码中应用修复。
• 专业领域或关注点不同：评审者可能不熟悉所有最佳实践，或者只是选择不在给定代码评审的上下文中评论某个问题（例如，只关注变更代码）。
虽然我们数据集中的大多数文件只有一条相关评论，但基于人工检查“错误”预测的个案证据表明，由于上述原因，通常可能有多条最佳实践评论。

鉴于我们的真值数据不完整，我们的精确率和召回率指标有噪声。1https://beam.apache.org/
因此，我们采用下一节描述的补充性评估，以提升对模型整体性能的信心。3.3.2
在完整历史代码评审上评估。为了准确评估真实环境中的潜在评论量，我们使用特定模型检查点和阈值，在一组历史代码评审上评估 AutoCommenter。预测的评论不会追溯发布到代码评审系统中，而是记录到数据库中供分析。这使我们能够估算预期发布频率——包括按文件和按代码评审的粒度。由于开发者会在整个受代码评审的代码变更集上与 AutoCommenter 交互，这一评估是生产部署（deployment）前的重要步骤。额外的好处是，这一步还允许针对不同用户群、编程语言等进行进一步优化并评估发布频率。3.4
推理（inference）基础设施
AutoCommenter 的核心是一个集中式最佳实践分析服务。该服务以一个或多个源文件作为分析输入。

对每个文件，它构建模型输入（3.1 节），将其编码为标准 TensorFlow Example 数据结构，并查询模型。模型本身由模型服务提供，该服务使用 TensorFlow 的 Example 数据结构作为与领域无关的输入输出格式。最后，最佳实践分析服务执行一系列过滤步骤（第 4 节），抑制低质量预测，并返回其余预测。3.5
IDE 与代码评审集成
开发者通过两种方式与 AutoCommenter 的分析服务交互——直接通过 IDE 插件，或间接通过代码评审系统。Google 的所有开发者都使用代码评审系统，而几乎所有人都使用 IDE。AutoCommenter 的评论以诊断信息形式出现在 IDE 中，用蓝色波浪下划线标出，覆盖相关代码片段。将鼠标悬停在下划线代码上会显示完整评论，其中包含最佳实践的简要总结，以及指向相关最佳实践文档的可点击链接。这种嵌入式信息消除了开发者在不熟悉最佳实践时需要在 IDE 和网页浏览器之间切换的需要，从而简化了工作流（workflow）。

由于 IDE 中的评论需要实时生成，我们的目标是以亚秒级延迟（latency）生成评论。在代码评审系统中，AutoCommenter 在每次更新后运行（即针对每个新的代码评审快照），如果检测到任何违规，就自动发布评论。自动化工具生成的评论在视觉上与人工评论相似，但背景颜色不同。图 3 展示了 AutoCommenter 在代码评审系统中生成并发布的一条示例评论。请注意右侧的点赞和点踩按钮，作者和评审者如果觉得某条评论特别有用或没用，可以点击它们。另请注意左侧的“Please fix”按钮，评审者可以看到它。如果点击它，就会生成一条新评论，表明评审者认为该评论很重要，必须在代码合并（merge）到代码库（codebase）之前处理。这些反馈按钮是代码评审系统中的标准功能，会出现在自动化工具生成的所有评论上（例如 [7, 13]），并为工具的用户接受度提供信号。IDE 也提供类似的反馈机制。

现代代码评审中编码实践的 AI 辅助评估
AIware ’24，2024 年 7 月 15–16 日，巴西 Porto de Galinhas
图 3：AutoCommenter 发布的示例评论。4
部署
我们在 2022 年 7 月至 2023 年 10 月期间，分阶段将 AutoCommenter 部署给 Google 的所有开发者：
• 截至 2022 年 7 月——团队试用：本文作者。
• 2022 年 7 月——早期采用者：约 3000 名志愿者。
• 2023 年 7 月——A/B 实验：约半数开发者。
• 自 2023 年 10 月起——正式发布：所有开发者。
请注意，出于工业保密原因，我们无法披露代码评审、开发者、文件、评论的绝对数量，或代码评审时长的分布。我们会在适当之处报告相对指标和相关趋势。我们采用迭代优化方法，持续评估并改进 AutoCommenter 的性能：
• 在历史数据上评估（3.3 节），以获取模型在该任务上表现如何的方向性洞察，并定义阈值和选择解码策略。
• 通过反馈按钮和问题报告，监控并分析用户交互和直接反馈。

• 基于其他评估步骤中观察到的模式，进行有针对性的人工评估。
图 4 展示了随时间变化的、针对已发布代码评审评论和 IDE 诊断信息的开发者正面与负面反馈之比。虚线表示开发者每月提供的反馈点击总数。正如预期，该计数在早期采用者阶段低得多。此外，由于我们在这一阶段积极优化 AutoCommenter，波动性更高。回想一下代码评审系统中的三个反馈按钮（图 3），它们允许开发者对已发布的评论表达正面或负面情感倾向。我们将带有点赞或“Please fix”的评论视为正面，将带有点踩的评论视为负面；我们将有用率定义为正面评论与所有带反馈评论之比。本节其余部分描述了我们在部署期间做出的具体观察和相应改进。4.1
选择阈值和解码策略
4.1.1
阈值。在初始部署期间，我们希望谨慎管理开发者对 AutoCommenter 的信任，因此从 𝑡= 0.98 的高置信度阈值开始。

我们人工抽样了数百个结果（图 4：部署期间的开发者反馈），并观察到阈值以下的预测中约 80% 仍然是正确的——也就是说，在 𝑡= 0.98 时假阴性率非常高。此外，我们观察到 Python 中的预测显示出显著不同的置信度分数分布，且受阈值化影响不成比例。我们推测，训练数据集构成（不同 URL 的数量和 URL 频率）以及最佳实践文档的具体程度是原因，但将更深入的调查留待未来工作。尝试部署按语言划分的阈值被证明无效，因为每种语言使用单一阈值仍无法充分捕捉模型正确预测数百种不同最佳实践的能力。这导致预测 URL 缺乏多样性，因为无论正确与否，模型往往会对某些 URL 给出比另一些更高的分数。这些观察促成了对 AutoCommenter 的第一项重大更改：基于验证数据集上的内在评估来计算按 URL 划分的阈值。4.1.2
解码。

使用按 URL 划分的阈值和贪心解码，在完整历史代码评审上进行评估，发现 AutoCommenter 在 6% 的所有已变更文件中检测到违规。然而，80% 的评论本会发布在作者未修改的代码行上。开发者通常不会对未更改的代码采取行动。因此，AutoCommenter 会过滤掉生成在未更改代码行上的评论，将已变更文件中的评论比例降至 1.3%。为了提高这一比例，我们尝试了不同的解码策略：贪心（默认）、束搜索、top-k 和 top-p 采样。我们最终选择了束搜索（生成 𝑛= 4 个潜在响应），这将发布频率提高到三倍，达到 3.9%。它还带来了显著更高的 URL 多样性：发布最频繁的 10 个 URL 占所有评论的 41%，而贪心搜索为 80%。延迟是选择部署解码策略时的另一个重要方面。虽然束搜索提高了发布频率和多样性，但推理明显变慢（中位延迟为 2 秒）。

鉴于这种延迟对于 IDE 中的交互式使用来说过高，我们最终决定在代码评审系统中使用束搜索，在 IDE 中使用贪心搜索。

AIware ’24，2024 年 7 月 15–16 日，巴西 Porto de Galinhas
Manushree Vijayvergiya 等 4.2
抑制过时最佳实践
在向约 3000 名自愿的早期采用者推出 AutoCommenter 后，我们注意到用户在几天内提交了大量问题。其中许多都对应同一个 URL2，该 URL 描述了与 Python 导入相关的最佳实践。然而，某些类型名称的规范来源已在 Python 3.9 中发生变化，最佳实践也在 2022 年初发生了变化。由于我们的训练数据延伸到 2022 年之前，其中包含许多不再适用的最佳实践评论。我们意识到这是一个反复出现的模式：随着语言演进或新库引入，最佳实践也会演进。缓解该问题的一种方式是过滤掉此类数据（每当规则变化时），并重新训练模型。然而，这既耗时又耗费资源：它需要完整的数据重新生成、模型训练、评估和推出。在此期间，“过时”模型要么需要被关闭，导致系统停机，要么需要抑制受影响的预测。

否则，系统可能很快失去开发者的信任。我们选择使用条件过滤（在源代码上匹配正则表达式）来抑制特定的最佳实践预测，原因有两个。第一，它可以动态部署并立即应用。第二，它允许对预测进行细粒度过滤。4.3
对选定评论的独立评分
在早期使用几个月后，我们观察到有用率停滞在约 54%。为了理解原因、确定改进领域并为更广泛的部署做准备，我们在 2023 年 4 月进行了一项独立人工评分研究，分析了约 370 条在早期采用者部署期间收到开发者反馈的已发布评论样本。为了收集关于评论有用性的多元视角，我们招募了 15 名评分者——来自合作团队的开发者。我们要求他们对收到明确用户反馈的 AutoCommenter 评论进行评分。我们没有向评分者展示原始用户反馈，以避免使他们的评估产生偏差。评分者根据链接的最佳实践和周边代码来评估每条评论的有用性。

我们指示他们关注评论的正确性，但也要关注该评论作为作者对他们是否可操作（例如，他们是否会处理一条技术上正确但在特定情况下似乎不值得处理的评论）。我们鼓励他们对每条评论提供自由形式的反馈。评分者评估得出的有用率为 60%，略高于同一批评论上开发者反馈的 54%，但远低于我们为更广泛部署设定的 80% 目标。这项研究最有趣的发现是，存在明显的不有用评论模式。以下是一些例子：
多个主题或复杂主题：例如，一个 URL 指向一节内容，其中描述了与 Python linter 交互的多条指南，包括它经常触发的情况以及抑制它的方法。作者可能难以理解已发布的评论具体指向哪条指南，以及如何解决它。同样，关于在 C++ 中编写良好函数文档的指导是一整页密集文本。

评分员经常指出，最佳实践（以及 AutoCommenter 的简洁摘要）与实际代码之间存在脱节，即使代码中确实包含相关违规。2https://github.com/google/styleguide/blob/gh-pages/pyguide.md#22-imports
高质量摘要的重要性：评分员常常发现，AutoCommenter 的摘要——它通过抓取文档源生成，有时还会缺失——未能充分说明所引用的准则与评论/代码之间的关联。主观且可能引发争议的话题：一个例子是避免在库代码中使用标志（flag）。在库中使用标志可能引发问题，但有些库正是为通过标志配置大量功能而设计的。此外，遗留代码可能并不遵循该准则，评审者也不会强制执行。模型没有学到这些细微差别，有时会在作者为已有库新增标志时预测出违规。某些准则上的系统性模型错误：一个有趣的例子是某条准则提倡对 C++ vector 优先使用成员函数 push_back 而非 emplace_back，而这两个函数在参数相同时可以实现相同效果。

模型已经学会预测这一点，但在 emplace_back 更合适的情况下，以及当某个无关类型拥有名为 push_back 的成员函数时，它也会做出同样的预测。正确但价值低的评论：代码注释中句末缺少句号往往为人工评审者所容许。虽然这在技术上没错，但要求作者回到 IDE 去修复该问题，净价值可能为负。评分员研究得出的洞见促成了对 AutoCommenter 的两项改动。第一，评分员研究识别出 17 个不可操作的 URL，将其屏蔽后，基于开发者反馈的历史有用比例从 54% 提升到 66%，基于评分员反馈的比例从 60% 提升到 74%。我们又分析了与类似但未评级的 URL 相关联的评论，并额外屏蔽了 5 个。第二，我们审查并手动更新了所有高频发布的 URL 的摘要。这些改动合在一起，足以让我们达到下一阶段部署所设定的 80% 有用比例目标。4.4
A/B 实验
2023 年 7 月，我们在 A/B 实验中把 AutoCommenter 部署给了约一半的开发者。

我们将开发者随机分配到实验组（启用 AutoCommenter）和对照组（禁用 AutoCommenter）。随机化依据是开发者电子邮箱地址 SHA256 哈希值的最后几位数字，并且我们验证了两组在规模和构成上没有差异，包括任职年限、职级、编程语言和业务部门的分布。我们还确认，实验开始前，实验中测量的各项变量在对照组与实验组之间均无差异。实验期间的评论发布频率符合预期（4.1 节）。我们未在以下任何一项上检测到具有统计显著性的变化：代码评审的总时长、开发者在代码评审上实际投入的时间、作者与评审者之间的评论—回复迭代次数。不过，我们确实检测到编码速度略有提升。我们推测，这归因于转向查阅文档的上下文切换减少所带来的正面效果。更深入的探究留待未来工作。

基于这些结果，我们得出结论：不存在不利影响，并于 2023 年 10 月将 AutoCommenter 部署给了所有开发者。

现代代码评审中编码实践的 AI 辅助评估
AIware ’24，2024 年 7 月 15–16 日，巴西加林哈斯港
图 5：生产环境中 AutoCommenter 生成的自动评论与训练数据中人工评论的每 URL 评论数累积分布。5
评估
基于有用比例和自 2023 年 3 月以来收集的用户反馈，我们得出结论：开发者总体上对 AutoCommenter 生成的评论感到满意。我们通过分析用户反馈，持续改进数据集准备、阈值、URL 屏蔽和摘要生成，以确保 AutoCommenter 对开发者工作流产生高度的正面影响。除了开发者满意度之外，在向整个 Google 广泛发布数月后，我们还评估了 AutoCommenter 性能的另外三个方面：
(1) 评论解决率：开发者多久会修改代码以解决 AutoCommenter 发布的评论？(2) AutoCommenter 与人工评论对比：AutoCommenter 的评论在多大程度上覆盖了人工评审者在评论中引用的最佳实践文档？(3) AutoCommenter 与

代码检查工具（linter）对比：AutoCommenter 的输出在多大程度上超越了传统静态分析工具的能力？5.1
评论解决率
开发者很少通过点击代码评审系统中的点赞/点踩按钮以及 IDE，和代码评审系统中的「请修复」按钮，对 AutoCommenter 的评论给出明确反馈（图 3）：代码评审系统中约 10% 的自动评论、IDE 中 2% 的诊断收到了明确反馈，这与 Google 其他自动化分析的情形相当。与此同时，开发者会悬停在 AutoCommenter 约 50% 的 IDE 诊断上，而此前的工作表明，开发者常常在没有明确反馈的情况下解决自动评论 [18]。为评估开发者解决 AutoCommenter 评论的频率，我们进行了一项离线分析，估算通过后续代码变更解决的评论比例。为分析评论解决情况，我们提取了针对 AutoCommenter 自动评论所在文件的历史变更。对每一项变更，我们提取了评论发布时的初始快照以及开发者最终合并进代码库的快照。

每条评论都跨越特定的行范围。我们在这些快照之间使用了自动化的基于 AST 的行映射方法 [18]，以识别模型原本
代码惯用法
文档
格式
语言
命名
0
5
10
不同 URL 的数量
代码检查工具
是
否/部分
图 6：按类型划分的预测频率最高的前 50 个 URL。代码检查工具表示检测相应违规的 linter 是已存在还是可以轻松构建。在第一个快照上预测到、但在合并后的快照上没有预测到的评论。这类快照对表明评论可能已被解决，但仍有可能是不相关的代码变更导致某条评论不再被预测。对 6000 对快照的自动分析显示，在 50% 的情况下，评论在其最初发布的行上已从提交的快照中消失。我们人工抽查了 40 对这类快照的随机样本。我们发现，在 80% 的情况下，作者所做的变更直接解决了所发布评论中描述的问题。

因此，我们估计评论解决率约为 40%，显著高于有明确正面反馈的评论占全部评论的比例。5.2
AutoCommenter 与人工评论对比
图 5 比较了生产环境中 AutoCommenter 生成的自动评论与训练数据中人工评论（按每个唯一 URL 对应一条最佳实践文档）的累积分布。x 轴是 URL 的排名，排名依据是所有曾在自动评论中出现过的 URL 按频率排序。例如，最常使用的 URL 排名第 1，占所有自动评论的 9.9%。同一个 URL 出现在训练数据中 4.3% 的人工评论里。总体而言，AutoCommenter 为 330 个不同的 URL 生成了评论。AutoCommenter 使用的 URL 集合覆盖了历史上 68% 带最佳实践 URL 的人工评论。这是个不错的结果：它表明 AutoCommenter 并未聚焦于评审者很少引用的冷门最佳实践。另一方面，尽管使用了束搜索，URL 的多样性仍然相对较低。前 85 个 URL 占了 AutoCommenter 所生成评论的 90%。

同一组 URL 覆盖了 35% 带最佳实践 URL 的人工评论。在保持准确率和低延迟的同时，提升 URL 的多样性以及自动评论对最佳实践的覆盖度，是我们的首要任务之一。5.3
AutoCommenter 与代码检查工具对比
为理解 AutoCommenter 在多大程度上提供了超越代码检查工具（这些工具能够高效、精确地检查某些最佳实践）的价值，我们抽样了预测频率最高的前 50 个违规——即图 5 中的前 50 个 URL。对每个抽样的

AIware ’24，2024 年 7 月 15–16 日，巴西加林哈斯港
Manushree Vijayvergiya 等 URL，我们查阅了其最佳实践文档，并确定 (1) 最佳实践类型（第 1 节），以及 (2) 检测相应违规的 linter 是已存在还是可以轻松构建。具体而言，三位作者（每人都有超过 10 年构建静态分析工具的经验）阅读了文档并独立对 URL 进行分类。在最佳实践类型上没有分歧，但对于约 15% 的 URL 是否可以轻松构建 linter 存在分歧。三位作者通过多数表决和讨论解决了这些分歧。分歧源于最佳实践含义模糊，以及某些最佳实践包含多条准则。例如，检查代码文档是否存在相对直接，但推断合理的例外情况和内容的清晰度则未必。图 6 展示了 50 个抽样 URL 的分布，按类型以及违规能否被 linter 检测来划分。在这 50 条最佳实践中，有 33 条（66%）的违规检测超出了传统静态分析的范围。

6
经验教训
基于我们开发和部署 AutoCommenter 的经验，我们总结出几条关键经验：
• 对传统分析的补充：AutoCommenter 由 LLM 支持的方法为人工评审者频繁引用的 68% 的最佳实践生成了评论。其中许多超出了传统静态分析的范围。• 内在评估与真实世界表现：内在评估与真实世界表现可能大相径庭：我们的内在评估使用真实世界人工评论数据集，结合当时最先进的模型架构和训练流程，显示模型前景良好，但我们的外在评估和系统改进对于成功部署至关重要。• 监测用户接受度至关重要：即便只有少数负面用户体验，也可能侵蚀对自动化系统的信任。持续监测和分析真实世界反馈，对于发现此类情况并找出补救措施至关重要。就 AutoCommenter 而言，一个简单的屏蔽机制就足以将用户接受度大幅提升到 80% 以上，而无需在效果上做出重大牺牲。

7
相关工作
Johnson [15] 于 1977 年、也就是近 50 年前引入了 C linter。在这 50 年间，产生了大量关于自动化静态分析的研究：Heckman 和 Williams [10] 最近的一篇文献综述识别出 17,571 篇论文。许多研究探讨开发者如何与静态分析交互。Johnson 等人 [14] 探讨了开发者在使用静态分析时面临的挑战。其研究结果凸显了良好集成到现有开发者工作流中的重要性，以及建立并维持对工具的信任的重要性。Vassallo 等人 [27] 探讨了开发者在不同场景（包括编码和代码评审）中如何与静态分析交互。他们同样发现，集成到现有工作流中对开发者是否愿意使用这些工具起着重要作用，而高质量的结果极为重要。Beller 等人 [6] 研究了大量开源项目中静态代码分析的使用情况。除其他发现外，他们强调自动化分析的使用方式和应有方式会因编程语言而异。

相比之下，将机器学习用于代码分析仍是一个相对较新、理解尚不充分的领域。近期有多篇论文（例如 Hong 等 [11]、Li 等 [16]、Li 等 [17]、Thongtanunam 等 [24]、Tufano 等 [25] 以及 Tufano 等 [26]）报告了模型评测结果，并提出了自动代码评审工具。这些模型以及评审意见生成任务与本文提出的模型非常相似，但其评测大多只基于历史数据集。如第 3.3.1 节所述，仅针对历史评审意见开展的内在评测有一定局限，有时无法预测真实场景中的表现。Frömmgen 等 [9] 的另一篇近期论文展示了对在线系统的评测，但针对的是相反的任务：根据评审意见生成代码，而非根据代码生成评审意见。8
结论
验证代码是否符合最佳实践，是现代代码评审流程中的一项常见任务。虽然部分最佳实践可以用 linter 等传统工具自动验证，但许多实践需要经验丰富的开发者运用知识与判断，这需要投入时间和精力。

本文报告了我们开发、部署和评测 AutoCommenter 这一由 LLM 支持的代码评审助手系统的经验。具体而言，文章完整呈现了从任务与模型设计，到内在评测与系统校准，再到分阶段上线与最终用户评测的全过程。评测结果表明，构建一个能力远超传统工具的端到端系统，并同时获得较高的最终用户接受度，是可行的。这些结果是将复杂的代码评审助手与自动化代码评审推向部署的一个有希望的开端。我们的首要目标是通过将 AutoCommenter 设计为具有极高的精确率，来确保良好的开发者体验。虽然召回率并非主要关注点，但我们认识到它的重要性，并计划探索模型与系统架构上的哪些改变能够提升召回率。例如，我们在 2022 年使用的模型在当时是最先进的，但它的上下文窗口只有 2048 个词元，仅够容纳约 200 行代码。

当前最先进的模型在训练时上下文窗口已达数万词元，推理时更是超过一百万词元。这一飞跃为开发新功能、并显著改进现有功能带来了机会。9
致谢
本工作是 Google 核心系统团队与 Google DeepMind 团队多年合作的成果。我们感谢所有团队成员与领导的支持和建议，包括 Alberto Elizondo、Alexander Frömmgen、Ballie Sandhu、Chandu Thekkath、Chris Gorgolewski、David Tattersall、Ilya Cherny、Jacob Austin、Katja Grünwedel、Kristóf Molnár、Lera Kharatyan、Luka Rimanić、Madhura Dudhgaonkar、Marc Brockschmidt、Marcus Revaj、Maxim Tabachnyk、Nina Chen、Niranjan Tulpule、Nitya Ramani、Paige Bailey、Pavel Sychev、Pierre-Antoine Manzagol、Quinn Madison、Roger Fleig、Satish Chandra、Savinee Dancs、Stoyan Nikolov、Subhodeep Moitra 和 Vaibhav Tulsyan。

现代代码评审中编码实践的 AI 辅助评估
AIware '24，2024 年 7 月 15–16 日，巴西 Porto de Galinhas
参考文献
[1] 2024. Google Style Guides. https://google.github.io/styleguide/. 访问日期：2024-03-15. [2] 2024. Linux kernel coding style. https://www.kernel.org/doc/html/v4.10/process/coding-style.html. 访问日期：2024-03-15. [3] 2024. PEP 8 – Python 代码风格指南. https://peps.python.org/pep-0008/. 访问日期：2024-03-15. [4] 2024. Rust Style Guide. https://doc.rust-lang.org/nightly/style-guide/. 访问日期：2024-03-15. [5] Alberto Bacchelli 和 Christian Bird. 2013. 现代代码评审的期望、结果与挑战. In 2013 35th International Conference on Software Engineering (ICSE). 712–721. https://doi.org/10.1109/ICSE.2013.6606617
[6] Moritz Beller、Radjino Bholanath、Shane McIntosh 和 Andy Zaidman. 2016. 静态分析现状分析：一项开源软件中的大规模评测. In 2016 IEEE 23rd International Conference on Software Analysis, Evolution, and Reengineering (SANER), Vol. 1. IEEE, 470–481. [7] Zimin Chen、Małgorzata Salawa、Manushree Vijayvergiya、Goran Petrović、Marko Ivanković 和 René Just. 2023.

MuRS：基于标识符模板的变异体排序与抑制. In Proceedings of the Symposium on the Foundations of Software Engineering (FSE). 1798–1808. [8] M. E. Fagan. 1976. 通过设计与代码检查减少程序开发中的错误. IBM Systems Journal 15, 3 (1976), 182–211. https://doi.org/10.1147/sj.153.0182
[9] Alexander Frömmgen、Jacob Austin、Peter Choy、Nimesh Ghelani、Lera Kharatyan、Gabriela Surita、Elena Khrapko、Pascal Lamblin、Pierre-Antoine Manzagol、Marcus Revaj、Maxim Tabachnyk、Daniel Tarlow、Kevin Villela、Daniel Zheng、Satish Chandra 和 Petros Maniatis. 2024. 用机器学习解决代码评审意见. In International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP). [10] Sarah Heckman 和 Laurie Williams. 2011. 面向自动化静态代码分析的可操作告警识别技术：系统性文献综述. Information and Software Technology 53, 4 (2011), 363–387. https://doi.org/10.1016/j.infsof.2010.12.007 特刊：第 24 届应用计算年度研讨会软件工程方向. [11] Yang Hong、Chakkrit Tantithamthavorn、Patanamon Thongtanunam 和 Aldeida Aleti.

2022. Commentfinder：一种更简单、更快速、更准确的代码评审意见推荐方法. In Proceedings of the Joint Meeting of the European Software Engineering Conference and the Symposium on the Foundations of Software Engineering (ESEC/FSE). 507–519. [12] Marko Ivanković、Goran Petrović、René Just 和 Gordon Fraser. 2019. Google 的代码覆盖率. In Proceedings of the Joint Meeting of the European Software Engineering Conference and the Symposium on the Foundations of Software Engineering (ESEC/FSE). 955–963. [13] Marko Ivanković、Goran Petrović、Yana Kulizhskaya、Mateusz Lewko、Luka Kalinovčić、René Just 和 Gordon Fraser. 2024. 有效覆盖率：提升代码覆盖率的可操作性. In International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP). [14] Brittany Johnson、Yoonki Song、Emerson Murphy-Hill 和 Robert Bowdidge. 2013. 软件开发者为何不使用静态分析工具来发现缺陷？. In 2013 35th International Conference on Software Engineering (ICSE). IEEE, 672–681. [15] Stephen C Johnson. 1977. Lint，一个 C 程序检查器. Bell Telephone Laboratories Murray Hill.

[16] Lingwei Li、Li Yang、Huaxi Jiang、Jun Yan、Tiejian Luo、Zihan Hua、Geng Liang 和 Chun Zuo. 2022. Auger：用预训练模型自动生成评审意见. In Proceedings of the Joint Meeting of the European Software Engineering Conference and the Symposium on the Foundations of Software Engineering (ESEC/FSE). 1009–1021. [17] Zhiyu Li、Shuai Lu、Daya Guo、Nan Duan、Shailesh Jannu、Grant Jenks、Deep Majumder、Jared Green、Alexey Svyatkovskiy、Shengyu Fu 和 Neel Sundaresan. 2022. 通过大规模预训练实现代码评审活动自动化. In Proceedings of the 30th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (<conf-loc>, <city>Singapore</city>, <country>Singapore</country>, </conf-loc>) (ESEC/FSE 2022). Association for Computing Machinery, New York, NY, USA, 1035–1047. https://doi.org/10.1145/3540250.3549081
[18] Goran Petrović、Marko Ivanković、Gordon Fraser 和 René Just. 2023. 请修复这个变异体：开发者如何处理代码评审中暴露出的变异体？. In International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP). 150–161.

[19] Rachel Potvin 和 Josh Levenberg. 2016. Google 为何将数十亿行代码存放在单一仓库中. Communications of the ACM (CACM) 59 (2016), 78–87. http://dl.acm.org/citation.cfm?id=2854146
[20] Peter Rigby、Brendan Cleary、Frederic Painchaud、Margaret-Anne Storey 和 Daniel German. 2012. 实践中的当代同行评审：来自开源开发的启示. IEEE Software 29, 6 (2012), 56–61. https://doi.org/10.1109/MS.2012.24
[21] Peter C. Rigby 和 Christian Bird. 2013. 趋同的当代软件同行评审实践. In Proceedings of the 2013 9th Joint Meeting on Foundations of Software Engineering (Saint Petersburg, Russia) (ESEC/FSE 2013). Association for Computing Machinery, New York, NY, USA, 202–212. https://doi.org/10.1145/2491411.2491444
[22] Adam Roberts、Hyung Won Chung、Gaurav Mishra、Anselm Levskaya、James Bradbury、Daniel Andor、Sharan Narang、Brian Lester、Colin Gaffney、Afroz Mohiuddin 等. 2023. 用 t5x 和 seqio 扩展模型与数据. Journal of Machine Learning Research 24, 377 (2023), 1–8. [23] Caitlin Sadowski、Emma Söderberg、Luke Church、Michal Sipko 和 Alberto Bacchelli. 2018.

现代代码评审：Google 的案例研究. In International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP). 181–190. [24] Patanamon Thongtanunam、Chanathip Pornprasit 和 Chakkrit Tantithamthavorn. 2022. Autotransform：支持现代代码评审流程的自动化代码转换. In Proceedings of the International Conference on Software Engineering (ICSE). 237–248. [25] Rosalia Tufano、Ozren Dabić、Antonio Mastropaolo、Matteo Ciniselli 和 Gabriele Bavota. 2024. 代码评审自动化：现有技术的优势与不足. IEEE Transactions on Software Engineering (TSE) (2024). [26] Rosalia Tufano、Simone Masiero、Antonio Mastropaolo、Luca Pascarella、Denys Poshyvanyk 和 Gabriele Bavota. 2022. 利用预训练模型推动代码评审自动化. In Proceedings of the International Conference on Software Engineering (ICSE). 2291–2302. [27] Carmine Vassallo、Sebastiano Panichella、Fabio Palomba、Sebastian Proksch、Harald C Gall 和 Andy Zaidman. 2020. 开发者在不同情境下如何使用静态分析工具. Empirical Software Engineering 25 (2020), 1419–1457. [28] T. Winters、T. Manshreck 和 H.

Wright. 2020. Google 的软件工程：从长期编程实践中获得的经验. O'Reilly Media. https://books.google.ch/books?id=TyIrywEACAAJ
收稿日期 2024-04-05；录用日期 2024-05-04

