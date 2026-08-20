# AI Image & Video Model Specs

A maintained, machine-readable database of AI image and video generation models — resolutions, aspect ratios, clip durations, audio support, watermark policies, commercial-use terms, API availability and open-weights status.

**[Browse the live comparison tables →](https://Ninglz.github.io/ai-image-video-model-specs/)**

[简体中文](README.zh-CN.md)

## Why this exists

Picking a generation model usually means opening eight pricing pages, three Discord servers and a half-outdated blog post. The basic facts — *can it do 9:16? how long can a clip be? does the free tier watermark my output? can I use this commercially?* — are scattered and change every few months.

This repo keeps those facts in two JSON files you can read, script against, or cite:

- [`data/video-models.json`](data/video-models.json) — 16 video generation models
- [`data/image-models.json`](data/image-models.json) — 12 image generation models

Every entry carries a `last_verified` date and a link to the official source. If something is stale, [open an issue](../../issues/new/choose) or send a PR.

## Video models at a glance

| Model | Developer | Max res | Max clip | Native audio | API | Open weights |
|---|---|---|---|---|---|---|
| Sora 2 | OpenAI | 1080p | 12s | ✅ | ✅ | — |
| Veo 3.1 | Google DeepMind | 1080p | 8s | ✅ | ✅ | — |
| Kling 2.5 Turbo | Kuaishou | 1080p | 10s | — | ✅ | — |
| Runway Gen-4 Turbo | Runway | 720p (4K upscale) | 10s | — | ✅ | — |
| Luma Ray2 | Luma AI | 1080p (4K upscale) | 9s | — | ✅ | — |
| Hailuo 02 | MiniMax | 1080p | 10s | — | ✅ | — |
| Wan 2.5 | Alibaba | 1080p | 10s | ✅ | ✅ | — |
| Wan 2.2 | Alibaba | 720p | 5s | — | ✅ | ✅ |
| Seedance 1.0 Pro | ByteDance | 1080p | 10s | — | ✅ | — |
| Vidu Q1 | Shengshu | 1080p | 5s | — | ✅ | — |
| PixVerse V5 | AISphere | 1080p | 8s | — | ✅ | — |
| Pika 2.2 | Pika Labs | 1080p | 10s | — | ✅ | — |
| LTX-2 | Lightricks | 4K / 50fps | 10s | ✅ | ✅ | — |
| HunyuanVideo | Tencent | 720p | 5s | — | ✅ | ✅ |
| Mochi 1 | Genmo | 480p | 5s | — | — | ✅ |
| Firefly Video | Adobe | 1080p | 5s | — | ✅ | — |

## Image models at a glance

| Model | Developer | Max res | Text rendering | API | Open weights |
|---|---|---|---|---|---|
| Nano Banana 2 | Google DeepMind | 4K | excellent | ✅ | — |
| GPT Image 1 | OpenAI | 1536px | excellent | ✅ | — |
| Midjourney v7 | Midjourney | ~2048px | fair | — | — |
| FLUX.2 | Black Forest Labs | 4MP | good | ✅ | ✅ (dev) |
| Ideogram 3.0 | Ideogram | 2048px | excellent | ✅ | — |
| SD 3.5 Large | Stability AI | 1MP | fair | ✅ | ✅ |
| Imagen 4 | Google DeepMind | 2K | good | ✅ | — |
| Recraft V3 | Recraft | 2048px + SVG | excellent | ✅ | — |
| Seedream 4.0 | ByteDance | 4K | excellent | ✅ | — |
| Qwen-Image | Alibaba | ~1.5MP | excellent (CJK) | ✅ | ✅ |
| HiDream-I1 | HiDream | 1MP | good | ✅ | ✅ |
| Firefly Image 4 | Adobe | 2K | good | ✅ | — |

Full details (aspect ratios, watermark policy, commercial-use terms, pricing tier, notes) live in the JSON files and on the [live site](https://Ninglz.github.io/ai-image-video-model-specs/).

## Guides

Practical, model-agnostic write-ups that answer the questions people actually have:

- [Choosing an image-to-video model](guides/choosing-an-image-to-video-model.md) — decision factors and recommendations by use case
- [Aspect ratio & resolution cheatsheet](guides/aspect-ratio-cheatsheet.md) — what every platform wants, and which models can deliver it natively
- [Watermarks, provenance & commercial use](guides/watermarks-and-commercial-use.md) — visible marks, SynthID, C2PA, and what to check before shipping AI media in a paid project

## Using the data

The JSON is stable and versioned (`schema_version`). Fetch it raw:

```bash
curl -s https://raw.githubusercontent.com/Ninglz/ai-image-video-model-specs/main/data/video-models.json | jq '.models[] | select(.native_audio == true) | .name'
```

You're welcome to use it in articles, apps and research — attribution to this repo appreciated (CC BY 4.0).

## Contributing

Corrections beat additions. If a spec is wrong or stale, that's the most valuable PR you can send. See [CONTRIBUTING.md](CONTRIBUTING.md) for the entry criteria and how to update `last_verified`.

## License

Data and docs are released under [CC BY 4.0](LICENSE). The website code in this repo is MIT.

---

Maintained by the team at [InkFox](https://inkfox.app) — a workspace where you can run many of these image and video models side by side. The database stays neutral: entries and specs are independent of whether a model is available on InkFox.
