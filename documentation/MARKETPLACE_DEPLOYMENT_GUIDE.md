# 🚀 Python Automation Product — Marketplace Deployment Guide

> **Scope:** Best practices for deploying Python scripts and automation tools across 8 marketplaces
> **Current Inventory:** 755+ Python scripts, 7 Gumroad bundles, 10 CodeCanyon products, 72 listings ready
> **Last Updated:** April 12, 2026

---

## Platform Comparison Matrix

| Platform | Product Type | Price Range | File Format | Review Time | Commission | Revenue Model |
|----------|-------------|-------------|-------------|-------------|------------|---------------|
| **Gumroad** | Bundles | $97-$197 | ZIP | None (instant) | 10% + $0.30 | One-time, subscription, PWYW |
| **CodeCanyon** | Individual scripts | $49-$99 | ZIP | 3-10 days | 12.5-55% | One-time (Regular/Extended) |
| **Codester** | Developer tools | $29-$79 | ZIP | 1-2 days | 50-80% | One-time |
| **Payhip** | Digital products | $37-$67 | ZIP | None (instant) | 5% (+ payment) | One-time, subscription, tiers |
| **Sellfy** | Subscriptions | $29-$99/mo | ZIP | None (instant) | 0% (flat fee) | Subscription only |
| **Etsy** | Digital downloads | $7-$49 | ZIP/PDF | None (instant) | 6.5% + $0.20 | One-time |
| **n8n** | Workflow templates | $29-$299 | JSON | Up to 7 days | N/A (self-hosted) | Template sales, services, SaaS |
| **Apify** | Automation actors | Pay-per-event | Docker | 3-7 days | 20% | PPE, free, legacy rental |

---

## 1. Gumroad (Bundles, $97-$197)

### File Format
- **Primary:** `.zip` archive containing all bundle contents
- **Accepted formats inside ZIP:** `.py`, `.json`, `.yaml`, `.md`, `.txt`, `.toml`, `.cfg`
- **Max file size:** 5GB per product (generous for code bundles)
- **Delivery structure:** Use tiered delivery — different ZIP files per purchase tier (Basic/Pro/Enterprise)

### Required Documentation
- **README.md** inside each script directory with:
  - System requirements (Python 3.8+, OS compatibility)
  - Installation steps (pip install, venv setup)
  - Quick-start guide (3-step minimum)
  - Configuration (`.env.example` template)
  - Usage examples with expected output
- **LICENSE file** (commercial vs. personal use clearly stated)
- **Version numbering** (v1.0, v1.1) with CHANGELOG.md
- **Support contact** (email, Discord, or GitHub issues link)

### Optimal Pricing Strategy
- **Sweet spot:** $47-$97 for bundles (data shows highest revenue in this range)
- **Bundle pricing:** 45-55% off individual total (perceived value)
- **Use Purchasing Power Parity (PPP)** — Gumroad auto-adjusts for global markets
- **Tier strategy:**
  - Basic ($47-67): Single product or small bundle
  - Pro ($97-147): Full bundle + documentation
  - Enterprise ($197+): Bundle + support + customization
- **Enable "Pay What You Want"** for lead-magnet products to build email list

### Approval/Review Process
- **No per-product approval** — instant publishing
- **Account review triggered** after 3-4 sales totaling $10+ (takes 1-3 weeks)
- **Funds held 7 days** before release; weekly payouts on Friday (UTC)
- **$10 minimum** payout threshold

### Marketing Assets Needed
- **Cover image:** 1280×720px (16:9), PNG
- **Product screenshots:** 3-5 images showing product in action
- **Demo video:** 60-90 seconds showing setup → usage → result
- **Product description:** 300-500 words with feature list, target audience, results
- **Free preview/sample:** Include 1 free script or preview PDF
- **Affiliate program:** Enable 30-50% commission to drive organic promotion

### Current Assets Ready
- ✅ 7 bundles prepared in `/10-gumroad-bundles/`
- ✅ Product descriptions, marketing emails, pricing calculators
- ✅ Bundle contents mapped with individual valuations

---

## 2. CodeCanyon (Individual Scripts, $49-$99)

### File Format
- **Main file:** `.zip` archive with this structure:
```
product-name-v1.0/
├── src/                    # All Python source files
├── docs/
│   ├── README.md           # Main documentation
│   ├── INSTALLATION.md     # Step-by-step setup guide
│   └── CHANGELOG.md        # Version history
├── requirements.txt        # Dependencies
├── .env.example            # Configuration template
├── LICENSE                 # CodeCanyon Regular License
├── setup.py or pyproject.toml
└── tests/                  # Test suite (highly recommended)
```
- **Additional upload:** Separate `.zip` with screenshots (3-8 images)
- **Code must be well-commented** — inline docstrings for all functions/classes
- **No hardcoded secrets** — use environment variable patterns

### Required Documentation
- **Comprehensive README.md** with:
  - Feature list with screenshots
  - Installation guide (step-by-step)
  - Configuration reference
  - API documentation (if applicable)
  - Troubleshooting / FAQ section
  - Support contact information
- **Inline code comments** — every function must have a docstring
- **Well-organized file structure** — logical module separation
- **Live demo URL** (highly recommended — missing demos cause rejection)

### Optimal Pricing Strategy
- **Individual scripts:** $19-$49
- **Full toolkits/suites:** $49-$99
- **Extended license:** 2-3x Regular License price
- **Commission:** Authors earn 45-87.5% (scales with sales volume)
- **Pricing factors:** uniqueness, development time, target audience (business > hobbyist)

### Approval/Review Process
- **Review time:** 3-10 business days
- **Strict quality standards** — items must be premium quality
- **Common rejection reasons:**
  - Insufficient documentation
  - Poorly organized code structure
  - Lack of live demo
  - Code quality issues (no error handling, no comments)
  - Market saturation (too many similar items)
  - Hardcoded credentials or paths
  - No version control / changelog
- **Soft rejection:** Fix and resubmit
- **Hard rejection:** Item deemed unsuitable (saturation, not premium enough)
- **⚠️ 2026 Reality:** Approval increasingly difficult for newcomers; sales volume has declined. Consider as secondary channel.

### Marketing Assets Needed
- **Preview image:** 590×300px (thumbnail)
- **Screenshots:** 3-8 images, 1500px+ width, showing actual functionality
- **Live demo URL** (strongly recommended)
- **Product video** (optional but helps)
- **Short description:** ≤130 characters with keywords
- **Full description:** ≥300 characters, feature list, technical requirements
- **Tags:** `python, automation, developer-tools, ai-tools, api, scraping`

### Current Assets Ready
- ✅ 10 CodeCanyon products in `/04-codecanyon-products/`
- ✅ Each has `src/`, `docs/`, `LICENSE`, `README.md`, `requirements.txt`
- ⚠️ Need live demo URLs for each product
- ⚠️ Need screenshot packages (800×400px preview + 200×200px icon for Codester)

---

## 3. Codester (Developer Tools, $29-$79)

### File Format
- **Main item file:** `.zip` (must include documentation)
- **Screenshots folder:** Separate `.zip` with screenshot images
- **Image requirements:** `.png` or `.jpg`
- **Preview image:** Exactly 800×400px
- **Icon image:** Exactly 200×200px

### Required Documentation
- **MUST include documentation in main ZIP** — items without docs are rejected
- **Required content:**
  - Installation/setup instructions
  - Step-by-step usage guides for all features
  - Support/contact information
  - Author details
- **Well-commented source code**
- **Highly organized file structure**

### Optimal Pricing Strategy
- **Individual scripts:** $19-$49
- **Developer toolkits:** $29-$79
- **Commission:** Authors earn 50-80% depending on exclusivity
- **Review time:** 1-2 business days (much faster than CodeCanyon)
- **Outcomes:** Approval, Soft Rejection (fix & resubmit), Hard Rejection

### Approval/Review Process
- **Fast:** 1-2 business days
- **Soft rejection:** Item needs adjustments — fix and resubmit
- **Hard rejection:** Unsuitable for market (saturation, not premium, free alternatives exist)
- **Key to approval:** Easy installation, well-commented code, organized structure, live demo

### Marketing Assets Needed
- **Preview image:** 800×400px (exact dimensions)
- **Icon:** 200×200px (exact dimensions)
- **Screenshots:** 3-9 images, professionally cropped
- **Short description:** ≤130 characters with keywords
- **Full description:** ≥300 characters, feature list, technical requirements
- **Demo site URL:** Highly recommended (can cause rejection if missing for scripts)
- **Product video (optional):** Max 90 seconds, light background music

---

## 4. Payhip (Digital Products, $37-$67)

### File Format
- **Primary:** `.zip` archive
- **Accepted:** PDF, MP3, MP4, ZIP, and most common file types
- **No strict file size limits** for most plans
- **Can deliver multiple files** per product listing

### Required Documentation
- **README.md** with installation and usage instructions
- **License terms** clearly stated on product page
- **Version history** maintained
- **Support contact** information

### Optimal Pricing Strategy
- **Sweet spot:** $37-$67 for comprehensive guides/toolkits
- **Pricing tiers:** Under 10 pages/scripts: $7-$17; 10-30 pages/scripts: $27-$47; Comprehensive: $47-$97
- **Commission:** 5% + payment processing (PayPal/Stripe)
- **Free plan available** (5% transaction fee, limited features)
- **Plus plan:** $29/mo (2% fee); Pro plan: $99/mo (0% fee)
- **Enable coupons** and affiliate programs
- **Cross-sell bundles** to increase AOV

### Approval/Review Process
- **No approval process** — instant publishing
- **Identity verification** required for payouts
- **Instant delivery** to buyers after purchase

### Marketing Assets Needed
- **Product image:** 1200×630px recommended
- **Product description:** Clear feature list, target audience, results
- **Preview/sample:** Free version or demo to build trust
- **Email marketing:** Built-in email list builder
- **Affiliate program:** Set commission rates (20-50%)
- **Upsell/cross-sell:** Configure post-purchase offers

---

## 5. Sellfy (Subscriptions, $29-$99/mo)

### File Format
- **Primary:** `.zip` archive
- **Accepted:** Digital files, print-on-demand products
- **Unlimited products** on all plans
- **Annual revenue limits:** Starter $10K, Business $50K

### Required Documentation
- **README.md** with installation instructions
- **Update schedule** clearly communicated (since subscription model)
- **Version changelog** for each release
- **Support commitment** (subscription buyers expect ongoing support)

### Optimal Pricing Strategy
- **Subscription model:** $29-$99/month for ongoing tool access
- **Platform cost:** Starter $29/mo, Business $79/mo (2026 pricing)
- **Best for:** Products with regular updates, new scripts monthly, community access
- **Positioning:** "Automation-as-a-Service" — new scripts/tools added monthly
- **Tier strategy:**
  - Basic ($29/mo): Access to current + 1 new script/month
  - Pro ($59/mo): All scripts + priority support
  - Enterprise ($99/mo): Custom requests + white-label rights

### Approval/Review Process
- **No approval** — instant publishing
- **Monthly subscription billing** managed by Sellfy
- **0% transaction fees** (you pay platform subscription instead)

### Marketing Assets Needed
- **Product image:** 1280×720px recommended
- **Product description:** Emphasize ongoing value, update schedule
- **Email marketing:** Built-in tools
- **Social media integration:** Direct Instagram/Facebook/TikTok links
- **Embeddable Buy Button:** For your own website

---

## 6. Etsy (Digital Downloads, $7-$49)

### File Format
- **Primary:** `.zip` archive (Etsy supports ZIP for digital downloads)
- **Alternative:** `.pdf` with download links (common workaround for code)
- **Max file size:** 20MB per file (Etsy limit) — use ZIP compression
- **Max files per listing:** 5 files
- **Workaround for larger products:** PDF with Gumroad/Payhip link for full download

### Required Documentation
- **README.md** inside ZIP
- **PDF quick-start guide** (Etsy buyers expect visual guides)
- **License terms** (personal vs. commercial use)
- **Installation guide** with screenshots
- **Beginner-friendly** language (Etsy audience is less technical)

### Optimal Pricing Strategy
- **Individual scripts:** $7-$19
- **Script packs (5-10):** $19-$39
- **Complete bundles (50+):** $39-$97
- **Commission:** 6.5% transaction fee + $0.20 listing fee
- **Etsy audience:** Less technical, beginner-friendly positioning works best
- **Bundle with ebooks:** "Python Automation + Beginner Guide PDF" at premium price
- **Use Etsy Ads:** $1-5/day budget for initial visibility

### Approval/Review Process
- **No approval** — instant publishing
- **Listing fee:** $0.20 per listing (valid 4 months)
- **Star Seller program:** Boosts visibility for top-rated shops
- **Digital downloads are auto-delivered** after purchase

### Marketing Assets Needed
- **Listing images:** 2000×2000px minimum (1:1 square), JPG/PNG
- **10 images per listing** maximum — use all slots
- **Image strategy:**
  - Image 1: Hero shot (clean design, product title, price badge)
  - Image 2: What's included (file list, visual)
  - Image 3: Before/after comparison
  - Image 4: Step-by-step preview
  - Image 5: Results/benefits
- **Listing title:** 140 characters max, keyword-optimized
- **Tags:** 13 tags per listing, use long-tail keywords
- **SEO:** Include "Python," "automation," "scripts," "digital download" in title/tags

---

## 7. n8n (Workflow Automation, $29-$299)

### File Format
- **Primary:** `.json` (n8n native workflow export format)
- **Packaging:** Bundle related workflows into ZIP with documentation
- **Include:** `.json` workflow files + README + setup guide + credential templates

### Required Documentation
- **Step-by-step customization guide** for each workflow
- **Credential setup instructions** (API keys, OAuth flows)
- **Expected inputs/outputs** documented
- **Dependency requirements** (n8n version, required nodes/credentials)
- **Troubleshooting/FAQ** section
- **Video walkthrough** (highly recommended for complex workflows)

### Optimal Pricing Strategy
- **Simple workflows:** $29-$49
- **Complex/industry-specific:** $99-$299
- **Bundles (5-10 workflows):** $199-$499
- **Tiered offerings:**
  - Basic ($29-49): JSON file only
  - Standard ($99-149): JSON + customization guide
  - Premium ($199-299): JSON + guide + implementation support
- **Services:** $1,000-$10,000+ for custom workflow development
- **Retainers:** $200-$1,000/month for maintenance
- **Sell via:** Gumroad, own website, or n8n community

### Approval/Review Process
- **n8n Library submissions:** Up to 7 days review (can be longer during high volume)
- **New submission form** and AI-assisted review pipeline in development
- **If >10 business days:** Email community@n8n.io to follow up
- **Community marketplace:** Self-published, no formal review

### Marketing Assets Needed
- **Workflow diagram/screenshot** showing node structure
- **Before/after comparison** (manual process vs. automated)
- **Video demo** (2-5 minutes)
- **Industry-specific positioning** (real estate, e-commerce, agencies)
- **Case study** showing time/money saved
- **GitHub repo** with template source for credibility

### Current Assets
- ✅ n8n workflow templates in existing product inventory
- ✅ Marketplace assets (descriptions, tags, images) in `/12-marketplace-assets/`

---

## 8. Apify (Automation Actors, Pay-per-Event)

### File Format
- **Standard:** Docker container (all Actors run as Dockerized images)
- **Python packaging:** Code must be in Dockerfile with Python base image
- **Actor configuration:** `actor.json` manifest in project root
- **Apify CLI** used for building and deploying (`apify push`)

### Required Documentation
- **README.md** with:
  - One-paragraph description (no marketing buzzwords)
  - **Input table:** Data types, defaults, limits
  - **Output schema** with sample JSON response
  - **Cost guidance:** `"typical run = N events × price + platform CU"`
  - **Worked pricing example** showing input, expected events, estimated cost
  - **Known limitations:** Geo-blocks, login walls, CAPTCHAs, rate limits
  - Screenshots or sample datasets
- **Input validation** with actionable error messages
- **Versioned builds** with migration notes for breaking changes

### Optimal Pricing Strategy
- **Pay Per Event (PPE):** Preferred model — bill per defined action
- **Free tier:** $0 runtime cost (buyer pays compute) — great for adoption
- **Pay Per Result (PPR):** Legacy, being deprecated — avoid new pricing
- **Rental (subscription):** Being sunset in 2026 — avoid
- **Revenue share:** 80% to developer, 20% to Apify
- **Minimum payout:** $100 bank transfer, $20 PayPal
- **Growth strategy:** Launch free → gather reviews → switch to PPE
- **Calculate PPE price:** (proxy cost + compute time) / expected events + margin

### Approval/Review Process
- **Requirements for approval:**
  - Complete listing (README, categories, images)
  - Stable success rates on example URLs
  - Tight input validation
  - Clear limitation disclosures
- **Common rejection fixes:**
  - Add screenshots/sample datasets
  - Disclose geo/login/CAPTCHA limits
  - Tighten input validation
  - Prove reliability on test URLs
- **Post-launch:** Monthly payout reconciliation (~3 days around 11th)
- **Pricing changes:** ~14-day notice required, limited frequency

### Marketing Assets Needed
- **Actor Store listing:** Title, description, categories, images
- **Screenshots:** Output samples, terminal output, data previews
- **Sample datasets:** JSON output examples proving functionality
- **SEO title:** Specific (e.g., "LinkedIn Jobs Scraper" not "Web Scraper")
- **Cross-sell portfolio:** Build multiple related Actors for discovery

---

## 📋 Universal Packaging Checklist

Use this checklist for EVERY marketplace upload:

### Code Quality
- [ ] All functions have docstrings
- [ ] No hardcoded secrets (use `.env`)
- [ ] Error handling implemented (try/except blocks)
- [ ] Input validation on all user-facing parameters
- [ ] Type hints on public functions
- [ ] PEP 8 compliant (run `black` + `isort`)

### Documentation
- [ ] `README.md` with installation, usage, configuration
- [ ] `.env.example` template included
- [ ] `requirements.txt` or `pyproject.toml` with pinned versions
- [ ] `LICENSE` file with clear usage terms
- [ ] `CHANGELOG.md` with version history
- [ ] Troubleshooting/FAQ section

### Packaging
- [ ] Clean ZIP with logical folder structure
- [ ] No `.git/`, `__pycache__/`, `.DS_Store`, `.env` files
- [ ] Version number in ZIP filename (`product-v1.0.zip`)
- [ ] Test ZIP extraction and installation from scratch

### Marketing
- [ ] Cover image at platform-specific dimensions
- [ ] 3-8 screenshots showing actual functionality
- [ ] Product description (platform-optimized length)
- [ ] 13 SEO tags/keywords
- [ ] Short description ≤130 chars (for CodeCanyon/Codester)
- [ ] Full description ≥300 chars with feature list
- [ ] Demo URL (if platform supports)

---

## 🎯 Platform Priority Ranking

Based on research and current ecosystem assets:

| Priority | Platform | Rationale |
|----------|----------|-----------|
| **1** | Gumroad | Instant publish, bundle-friendly, $97-197 sweet spot, 7 bundles ready |
| **2** | Etsy | High traffic, beginner-friendly audience, $7-49 impulse buys |
| **3** | Payhip | Instant publish, low fees, good for individual scripts |
| **4** | Codester | Fast review (1-2 days), 50-80% commission, dev audience |
| **5** | n8n | Growing ecosystem, high-value workflow templates ($99-299) |
| **6** | Apify | 80% revenue share, strong for scraping/data actors |
| **7** | CodeCanyon | Declining platform, strict review, but still has traffic |
| **8** | Sellfy | Best for subscription model, requires ongoing content commitment |

---

## 📦 Recommended Product-to-Platform Mapping

Based on existing inventory:

| Product | Primary Platform | Secondary | Tertiary |
|---------|-----------------|-----------|----------|
| Code Quality Bundle ($97) | Gumroad | Payhip | — |
| MCP Forge ($149) | Gumroad | CodeCanyon | — |
| Plugin Dev Toolkit ($79) | Gumroad | Codester | — |
| Python Automation (50 scripts) | Etsy (beginner pack) | Gumroad | CodeCanyon |
| Agent Templates | Gumroad | n8n (as workflows) | — |
| File Organizer | CodeCanyon | Codester | Etsy |
| Messaging Bots | CodeCanyon | Apify | — |
| Sora Automation | Apify | Gumroad | CodeCanyon |
| ToolUniverse API | Apify | Gumroad | — |
| SEO Repo Optimizer | Etsy | CodeCanyon | n8n |
| n8n Workflow Templates | n8n (community) | Gumroad (bundle) | — |
| Scrapy/Scraping Actors | Apify | CodeCanyon | — |

---

## ⚠️ Important Notes

1. **CodeCanyon in 2026:** Platform is experiencing declining sales and increasingly difficult approval for newcomers. Treat as secondary channel, not primary revenue driver.

2. **Etsy positioning:** Etsy buyers are less technical. Frame Python scripts as "automation tools" or "productivity templates" rather than developer tools. Include beginner-friendly PDF guides.

3. **Apify PPE calculation:** Always calculate `(proxy_cost + compute_time_cost) / events + margin`. Underpricing means you lose money on every run.

4. **n8n monetization:** The n8n Library itself is free. Monetize by selling template bundles on Gumroad/Payhip and referencing the free n8n community templates as demos.

5. **Sellfy commitment:** Only use Sellfy if you can commit to monthly content updates. Subscription buyers churn fast without perceived ongoing value.

6. **Cross-platform consistency:** Maintain version parity across platforms. When you update a script, update the ZIP everywhere and note it in CHANGELOG.md.

---

*This document should be reviewed and updated quarterly as platform policies and market dynamics evolve.*
