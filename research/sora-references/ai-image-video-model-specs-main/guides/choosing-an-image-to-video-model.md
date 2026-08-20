# Choosing an image-to-video model

Last updated: 2026-06. Specs referenced here come from [`data/video-models.json`](../data/video-models.json) — check `last_verified` dates before relying on exact numbers.

There is no "best" image-to-video model. There's a best model *for a given clip*, and the ranking changes depending on what you're animating. This guide covers the questions that actually decide the choice.

## The six questions that matter

### 1. Do you need audio in the same generation?

Only a few models generate synchronized audio natively: **Sora 2**, **Veo 3.1**, **Wan 2.5** and **LTX-2**. Everything else gives you a silent clip, and you add sound in post.

If your output is dialogue or anything where lip sync matters, this question alone eliminates most of the field. If you're scoring with music anyway (most short-form content), ignore audio support and choose on motion quality.

### 2. How long does the clip need to be?

Most models top out at 5–10 seconds per generation. "Longer" videos are made by extending (generating a continuation from the last frame) or by cutting separate clips together.

Practical implication: don't pick a model for its max duration. Pick it for how well it extends — character and lighting drift on extension varies a lot between models. For multi-shot sequences from a single prompt, **Seedance 1.0 Pro** is currently the notable option.

### 3. How faithful must it stay to your input image?

Image-to-video models sit on a spectrum between *"animate exactly this"* and *"use this as loose inspiration."*

- Product shots, brand characters, real people: you want high input fidelity. **Kling** and **Runway Gen-4** are known for staying close to the source.
- Mood pieces and abstract motion: fidelity matters less, so cheaper/faster models (**PixVerse**, **Hailuo**) become attractive.

Test with your hardest image, not your prettiest one. A model that keeps a human face stable will handle a landscape; the reverse is not true.

### 4. What does failure cost you?

Generation is probabilistic — budget for retries. A model with $0.30/clip and a 50% keeper rate costs more than a $0.45 model with an 80% keeper rate, and wastes your time besides.

This is why the `pricing_tier` field in the dataset is deliberately coarse. Per-clip price lists go stale in weeks, and the sticker price is the wrong number anyway. Estimate *cost per usable clip* from your own tests.

### 5. Do you need an API or a UI?

Almost everything has an API now (see `api_available`), but ergonomics differ: some are first-party, some only exist through aggregator platforms, and rate limits vary wildly. If you're building a product, also check webhook support and queue times under load — none of which appear on pricing pages.

If you're a creator rather than a developer, the calculus flips: UI quality, preset libraries and editing tools matter more than raw model quality, because they determine your iteration speed.

### 6. Does it have to run on your hardware?

If data can't leave your infrastructure, or you need unlimited generations at fixed cost, the open-weights column is your shortlist: **Wan 2.2**, **HunyuanVideo**, **Mochi 1**. Expect a real quality and resolution gap versus the closed frontier — currently roughly a year behind — and check the license: "open weights" ranges from Apache 2.0 (do anything) to community licenses with revenue caps.

## Quick recommendations by use case

| Use case | Start with | Why |
|---|---|---|
| Talking character / dialogue | Sora 2, Veo 3.1 | Native synced audio |
| Product animation for ads | Kling 2.5, Runway Gen-4 | Input fidelity, motion control |
| High-volume social content | PixVerse V5, Hailuo 02 | Cost per usable clip |
| Cinematic / film look | Veo 3.1, Luma Ray2 | Lighting, camera behavior |
| Multi-shot story in one go | Seedance 1.0 Pro | Native multi-shot generation |
| Self-hosted / private | Wan 2.2 | Apache 2.0, runs on consumer GPUs |
| Brand-safe for client work | Firefly Video | Licensed training data |

## A sane evaluation workflow

1. Pick 3 candidate models from the table above.
2. Take **three of your own images**: an easy one, a typical one, and your hardest (faces, hands, text, fine patterns).
3. Run the same short motion prompt on all three models. Note keeper rate, not just best-case output.
4. Re-run the winner with your real aspect ratio and target duration — some models degrade noticeably at 9:16 or on extension.

An hour of this beats any leaderboard, including this repo's tables.

---

*Maintained as part of [ai-image-video-model-specs](../README.md). The team behind this database builds [InkFox](https://inkfox.app), where you can run several of these models side by side on the same input image — which is also the fastest way to do step 3 above.*
