# Contributing

Thanks for helping keep this accurate. A few ground rules keep the dataset trustworthy.

## Corrections (most wanted)

If a spec is wrong or stale:

1. Edit the relevant entry in `data/video-models.json` or `data/image-models.json`.
2. Update that entry's `last_verified` to the current `YYYY-MM`.
3. In the PR description, link the **official source** for the new value (docs, pricing page, changelog, announcement). Tweets from the official account count; third-party blogs don't.

Small PRs merge fast. One model per PR is ideal.

## Adding a model

Entry criteria — all must hold:

- **Generally available.** No waitlists, invite-only betas or "coming soon."
- **A creator or developer can actually use it** — public UI or public API.
- **Distinct model, not a wrapper.** Platforms that resell other models (including InkFox itself) don't get entries; the underlying models do.
- For image models: notable on at least one axis (quality, speed, price, license, text rendering, format). We don't list every SD fine-tune.

Copy an existing entry as a template and fill every field. If a field is genuinely unknowable, use `"unknown"` rather than guessing — and say so in `notes`.

## Updating after a model release

When a provider ships a new major version (e.g. Kling 2.5 → 3.0):

- If the old version is still sold/served, keep both entries.
- If the old version is retired, replace the entry and mention the supersession in `notes`.

## What we don't take

- Promotional copy in `notes` — keep it factual and comparative.
- Affiliate or referral links anywhere.
- Quality rankings or scores. This repo records *facts*; "which is better" belongs in benchmarks, not here.

## Schema changes

Open an issue first. Schema bumps (`schema_version`) break downstream users, so they need more discussion than a data fix.
