# AvatarArts CloudDocs vs AVATARARTS Dupe Du Diff - 2026-07-08

## DU

- CloudDocs `0_AvaTarArTs`: 897M
- `/Users/steven/AVATARARTS`: 9.5G
- `/Users/steven/AVATARARTS/business`: 9.4G
- `/Users/steven/AVATARARTS/docs`: 64M
- `/Users/steven/AVATARARTS/system`: 18M
- `/Users/steven/AVATARARTS/code`: 11M

## Exact Archive-Folder Duplicates By File List
- `Main-Html.zip` == `Main-Html` (125 files)
- `_disco (1).zip` == `disco` (133 files)
- `ai-phi.zip` == `ai-phi` (6 files)
- `card.zip` == `card` (5 files)
- `ChatGPT-Export.zip` == `ChatGPT-Export` (9 files)
- `gallery.zip` == `gallery` (14 files)
- `alchemy.zip` == `alchemy` (5 files)
- `tutorials.zip` == `tutorials` (4 files)
- `tools.zip` == `tools` (4 files)
- `grouped-gallery.zip` == `grouped-gallery` (3 files)
- `chotaku.zip` == `chotaku` (4 files)
- `AvatarArts_AI_Music_Integrations.zip` == `AvatarArts_AI_Music_Integrations` (8 files)

## Near Duplicates: Archive Adds Only Finder Junk
- `city.zip` ~= `city` (archive-only 1 junk entries)
- `follow.zip` ~= `follow` (archive-only 2 junk entries)
- `all.zip` ~= `all` (archive-only 1 junk entries)
- `form.zip` ~= `form` (archive-only 1 junk entries)
- `flow.zip` ~= `flow` (archive-only 1 junk entries)

## Real Archive-Folder Diffs
- `_disco.zip` vs `disco`: archive-only 0, dir-only 4; examples archive=[] dir=['js/main.js', 'js/photoswipe-ui-default.min.js', 'js/photoswipe.min.js']

## No Obvious Target Name Match In /Users/steven/AVATARARTS
- `Main-Html.zip`
- `Main-Html`
- `city.zip`
- `city`
- `_public_html.tar`
- `_public_html.zip`
- `seo`
- `follow`
- `follow.zip`
- `all.zip`
- `all`
- `_public_html (1).tar`
- `simplegallery`
- `ai-phi.zip`
- `ai-phi`
- `card`
- `card.zip`
- `ChatGPT-Export.zip`
- `ChatGPT-Export`
- `Quantum_Computing_Breakthroughs_2026-06-16.pptx`
- `medium`
- `flow.zip`
- `flow`
- `cover`
- `grouped-gallery.zip`
- `chotaku.zip`
- `grouped-gallery`
- `chotaku`
- `AvatarArts_AI_Music_Integrations`
- `blog.zip`
- `buy.zip`
- `AvatarArts_AI_Music_Integrations.zip`
- `AvatarArts_HTML.zip`
- `AvatarArts_Tailwind.zip`
- `AvatarArts_Astro.zip`
- `AvatarArts_NextJS.zip`

## Merge Guidance
- Do not merge exact archive-folder duplicate pairs until deciding whether archive or expanded folder is canonical.
- `Main-Html.zip` and `Main-Html` are exact by file list; this is the biggest duplicate pair and should be resolved first if cleaning CloudDocs.
- `_disco.zip` is older/incomplete relative to `disco`; `_disco (1).zip` matches `disco`.
- Candidate deltas to inspect before merge into AVATARARTS: `alchemy`, `form`, `quantumforgelabs`; earlier rsync dry-runs showed real differences.
- Many CloudDocs artifacts have no obvious shallow name match in AVATARARTS; these should be staged under a review/import area, not copied into the live tree root.
