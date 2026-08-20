# AI 图像与视频生成模型规格库

一个持续维护、机器可读的 AI 图像/视频生成模型数据库——分辨率、宽高比、片段时长、原生音频、水印策略、商用条款、API 可用性与开源权重状态，一处查齐。

**[在线对比表 →](https://Ninglz.github.io/ai-image-video-model-specs/)**

[English](README.md)

## 为什么做这个

选生成模型时，往往要翻八个定价页、三个 Discord 和一篇过时的博客。最基础的事实——*支不支持 9:16？一段最长几秒？免费版有没有水印？能不能商用？*——零散又常变。

这个仓库把这些事实放进两个 JSON 文件，可以直接阅读、写脚本调用，或在文章里引用：

- [`data/video-models.json`](data/video-models.json) — 16 个视频生成模型
- [`data/image-models.json`](data/image-models.json) — 12 个图像生成模型

每条记录都带 `last_verified`（最近核实日期）和官方来源链接。发现过期信息欢迎[提 issue](../../issues/new/choose) 或直接 PR。

## 内容速览

- **视频模型**：Sora 2、Veo 3.1、可灵 2.5、Runway Gen-4、Luma Ray2、海螺 02、万相 Wan 2.5/2.2、Seedance、Vidu、PixVerse、Pika、LTX-2、混元、Mochi、Firefly
- **图像模型**：Nano Banana 2、GPT Image 1、Midjourney v7、FLUX.2、Ideogram 3、SD 3.5、Imagen 4、Recraft V3、Seedream 4、Qwen-Image、HiDream、Firefly

完整字段（宽高比、水印、商用条款、价格档位、备注）见 JSON 文件和[在线站点](https://Ninglz.github.io/ai-image-video-model-specs/)。

## 实用指南（英文）

- [如何选图生视频模型](guides/choosing-an-image-to-video-model.md)
- [宽高比与分辨率速查表](guides/aspect-ratio-cheatsheet.md)
- [水印、内容溯源与商用须知](guides/watermarks-and-commercial-use.md)

## 数据使用

JSON 结构稳定且有版本号（`schema_version`），可直接 raw 拉取。欢迎在文章、应用、研究中使用，遵循 CC BY 4.0 署名即可。

## 参与贡献

**纠错比新增更有价值。** 入库标准和更新方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可

数据与文档采用 [CC BY 4.0](LICENSE)，站点代码 MIT。

---

由 [InkFox](https://inkfox.app) 团队维护——一个可以并排使用其中多款图像/视频模型的创作工作台。本数据库保持中立：模型收录与规格记录不受其是否上架 InkFox 影响。
