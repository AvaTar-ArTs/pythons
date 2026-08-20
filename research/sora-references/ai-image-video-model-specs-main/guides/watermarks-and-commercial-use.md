# Watermarks, provenance & commercial use

Last updated: 2026-06. This is practical orientation, **not legal advice** — terms change and jurisdictions differ. The `watermark` and `commercial_use` fields in [the dataset](../data/) link to each model's official terms.

## The three kinds of "watermark"

People use one word for three different things, and the difference matters:

### 1. Visible watermarks

A logo or text overlay burned into the pixels — usually on free tiers (Kling, Hailuo, PixVerse, Ideogram free plans), removed when you pay. Sora's consumer app adds a moving visible watermark to exports regardless.

What to know: a visible watermark on a draft is fine; shipping one in client work is not. Removing a provider's watermark yourself (cropping, inpainting) typically violates the terms you generated under — pay for the clean export instead.

### 2. Invisible watermarks (e.g. SynthID)

A signal embedded in the pixels themselves, designed to survive compression, resizing and screenshots. Google stamps **SynthID** on everything from Veo, Imagen and the Gemini image models. You can't see it, and you can't reliably remove it.

What to know: assume anything you generate with Google models is permanently identifiable as AI-generated. That's not a problem for legitimate work — but don't promise a client "undetectable" output, because you can't deliver it.

### 3. Provenance metadata (C2PA / Content Credentials)

A signed manifest attached to the file saying how it was made. OpenAI and Adobe attach **C2PA** metadata to generations. Unlike invisible watermarks, metadata is fragile — it's stripped by most social platforms, screenshots and re-encodes.

What to know: C2PA is increasingly *expected* in professional contexts (news, stock, some ad networks scan for it). Stripping it deliberately to hide AI origin is a bad idea and, in some contexts, becoming a legal one.

## Commercial use: the questions to actually check

"Can I use this commercially?" is usually the wrong granularity. Work through these instead, against the *current* terms of the model you used:

1. **Does my plan tier allow commercial use?** Free tiers often don't. Midjourney famously requires the paid plan, with extra conditions for companies above a revenue threshold.
2. **Who owns the output?** Most providers assign you their rights in the output — but in many jurisdictions (including the US), purely AI-generated work may not be copyrightable by *anyone*. You can use it; you may not be able to stop others from using something identical.
3. **What about the input?** If you animated a photo, your rights in the photo carry over — and so do other people's. An input image you didn't have rights to doesn't become yours by running it through a model. Faces add publicity/privacy rights on top.
4. **Open weights ≠ do anything.** Apache 2.0 (Wan 2.2, Mochi, Qwen-Image) is genuinely permissive. "Community" licenses (HunyuanVideo, SD 3.5) carry revenue caps or company-size restrictions. FLUX dev weights are non-commercial by default — the commercial license is separate. Read the actual license, not the README badge.
5. **Does my distribution channel have AI rules?** App stores, stock sites, ad networks and some marketplaces have their own disclosure or rejection policies, independent of what the model's terms allow.

## A pre-shipping checklist

Before AI-generated media goes into anything paid or public-facing:

- [ ] Generated on a plan tier whose terms permit commercial use
- [ ] No provider watermark in the deliverable (paid export, not manual removal)
- [ ] Rights to all input images confirmed (especially faces and brands)
- [ ] Client/stakeholder knows it's AI-generated, if disclosure matters in your context
- [ ] If using open weights: license actually read, revenue/size caps checked
- [ ] Output reviewed for accidental trademarks, logos, celebrity likeness, legible nonsense text

Ten minutes of this is cheaper than one takedown.

---

*Part of [ai-image-video-model-specs](../README.md), maintained by the team at [InkFox](https://inkfox.app). InkFox resolves the watermark question server-side per plan — one of the reasons this table exists is that we had to research all of it anyway.*
