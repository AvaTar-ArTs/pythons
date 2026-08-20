# Aspect ratio & resolution cheatsheet for AI media

Last updated: 2026-06. Model support data comes from [`data/video-models.json`](../data/video-models.json) and [`data/image-models.json`](../data/image-models.json).

Generating at the wrong aspect ratio is the most common avoidable mistake in AI media work. Cropping a 16:9 generation to 9:16 throws away 65% of your pixels and usually the composition with it. Generate native whenever the model allows.

## What each platform wants

### Video

| Platform / placement | Ratio | Recommended size | Notes |
|---|---|---|---|
| TikTok | 9:16 | 1080×1920 | Keep text inside center ~80%; UI covers edges |
| Instagram Reels | 9:16 | 1080×1920 | Cover image is cropped to 1:1 in grid |
| YouTube Shorts | 9:16 | 1080×1920 | Max 3 minutes |
| YouTube standard | 16:9 | 1920×1080 / 3840×2160 | 4K noticeably improves perceived quality |
| Instagram feed video | 4:5 | 1080×1350 | Tallest allowed in feed; more screen than 1:1 |
| X (Twitter) | 16:9 or 1:1 | 1280×720 / 1080×1080 | 16:9 autoplays cleanly in timeline |
| LinkedIn | 16:9 or 1:1 | 1920×1080 | 1:1 takes more feed space on mobile |
| Stories / WhatsApp status | 9:16 | 1080×1920 | Top/bottom ~250px covered by UI |
| Display ads (landscape) | 16:9 | 1920×1080 | Some networks also want 1:1 and 4:5 cuts |

### Image

| Platform / placement | Ratio | Recommended size |
|---|---|---|
| Instagram feed | 4:5 | 1080×1350 |
| Instagram grid thumbnail | 1:1 | (auto-cropped) |
| Pinterest pin | 2:3 | 1000×1500 |
| X post image | 16:9 | 1600×900 |
| Open Graph (link preview) | 1.91:1 | 1200×630 |
| YouTube thumbnail | 16:9 | 1280×720 |
| Blog hero | 16:9 or 3:2 | ≥1600px wide |
| Print A-series | 1:√2 (≈5:7) | 300 DPI at target size |

## Which video models generate which ratios natively

From the dataset (June 2026):

- **16:9 + 9:16 only**: Sora 2, Veo 3.1
- **16:9 / 9:16 / 1:1**: Kling 2.5, Hailuo 02, Wan 2.5, Vidu Q1, LTX-2, HunyuanVideo, Firefly Video
- **Six or more ratios** (incl. 4:3, 3:4, 21:9): Runway Gen-4, Luma Ray2, Seedance 1.0 Pro, PixVerse V5
- **Image models**: most modern ones (Nano Banana 2, Seedream 4, Ideogram 3, FLUX.2, Midjourney) handle all common ratios; the constraint is almost always the *video* model.

So if your pipeline is image → video, choose the **video** model's supported ratio first, then generate the source image to match.

## Rules of thumb

1. **Generate native, don't crop.** If the model can't do your target ratio, outpaint/extend the source image to the target ratio first, then animate.
2. **One ratio per campaign asset is a myth.** Plan for 9:16 + 16:9 + 1:1/4:5 cuts from the start. Either generate each natively or compose the 16:9 master with a "safe center" that survives a 9:16 crop.
3. **Resolution ≠ quality, but it's not optional either.** 720p output looks fine on a phone feed and soft on a TV. For anything that might be reused (ads, web hero), prefer models with 1080p+ native output or a good upscale path — see `max_resolution` in the dataset.
4. **Mind the UI chrome.** On TikTok/Reels/Shorts, captions, buttons and the progress bar eat the edges. Keep faces and text in the central ~80% vertically.
5. **Upscaling is fine for stills, risky for video.** Image upscalers are mature; video upscaling can shimmer on motion. Test before promising a client 4K.

---

*Part of [ai-image-video-model-specs](../README.md), maintained by the team at [InkFox](https://inkfox.app) — where generating the same shot in three ratios is a dropdown, not a re-prompt.*
