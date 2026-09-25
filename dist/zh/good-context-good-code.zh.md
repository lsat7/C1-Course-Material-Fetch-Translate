<!-- source: pages/good-context-good-code.html -->
<!-- status: upstream-unavailable -->

# Good Context, Good Code（上游不可获取，非译文）

> **状态说明**：本文正文**未能获取**，此文件是缺口说明，**不包含译文**，也未做任何推测性翻译。
> 保留它是为了让读者明确知道"这里少了一份资料、为什么少"，而不是以为翻译漏了。

- **源文件**：`pages/good-context-good-code.html`（离线镜像内正文仅 344 字符）
- **原始站点**：StockApp 工程博客（Ghost 托管）
- **不可获取原因**：站点设有**访问码墙**（access code wall），正文被拦在授权层之后；静态镜像只留下站点框架与「输入访问码」提示，没有可翻译正文。
- **影响面**：以可翻译正文字符计，本文约 344 字符，占全量 591,975 字符的 **0.06%**。
- **如何补上**：若你持有该站访问码（或在浏览器里已登录），把带正文的 HTML 放回镜像同名路径
  `pages/good-context-good-code.html`，然后重跑流水线即可自动补译，**无需改任何代码**：

  ```bash
  python tools/02_extract.py      # 重新抽取正文
  python tools/03_segment.py      # 分段 + 术语占位符保护
  python tools/04_translate.py    # 机器翻译（DeepSeek 兼容端点）
  python tools/05_assemble.py     # 回填重组
  python tools/08_verify.py       # Han 占比与占位符校验
  ```

更多上下文：见 [`../来源清单.md`](../来源清单.md) 第三节「上游不可获取的 4 篇」与 [`../README.md`](../README.md) 第六节「已知缺口」。
