<!-- source: pages/how-warp-uses-warp.html -->
<!-- status: upstream-unavailable -->

# How Warp Uses Warp（上游不可获取，非译文）

> **状态说明**：本文正文**未能获取**，此文件是缺口说明，**不包含译文**，也未做任何推测性翻译。

- **源文件**：`pages/how-warp-uses-warp.html`（离线镜像内正文仅 148 字符）
- **原始站点**：Notion 公开页面
- **不可获取原因**：Notion 页面依赖 **JavaScript 客户端渲染**，静态抓取只能拿到空壳，唯一可见文本是「必须启用 JavaScript 才能使用 Notion」；正文从未出现在镜像里。
- **影响面**：以可翻译正文字符计，本文约 148 字符，占全量 591,975 字符的 **0.025%**。
- **如何补上**：在浏览器中打开原页面并另存为完整 HTML（含渲染后 DOM），或改用带渲染的抓取方式存入
  `pages/how-warp-uses-warp.html`，再重跑 `tools/02_extract.py` → `03_segment.py` → `04_translate.py` → `05_assemble.py` → `08_verify.py`，流水线会自动补译。

更多上下文：见 [`../来源清单.md`](../来源清单.md) 第三节「上游不可获取的 4 篇」与 [`../README.md`](../README.md) 第六节「已知缺口」。
