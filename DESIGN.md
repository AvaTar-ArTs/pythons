# Design System: AI Python Automation Toolkit

## 1. Visual Theme & Atmosphere
A raw, utilitarian, and mechanical interface inspired by high-end engineering documentation. It feels like a declassified blueprint for an AI agent. The atmosphere is dense, structured, and focused on information density without clutter, using asymmetric layouts to guide the eye through complex script configurations.

## 2. Color Palette & Roles
- **System Dark** (#09090B) — Primary background surface
- **Steel Surface** (#18181B) — Container/Card fill
- **Terminal White** (#FAFAFA) — Primary text
- **Muted Gray** (#71717A) — Secondary text/metadata
- **Utility Blue** (#3B82F6) — Primary accent for terminal output/CLI references
- **Border Utility** (rgba(255,255,255,0.1)) — 1px dividers

## 3. Typography Rules
- **Display:** Geist — Tight-tracked, high contrast, authoritative
- **Body:** Satoshi — Relaxed leading, 65ch max, precise readability
- **Mono:** JetBrains Mono — Used for all code, CLI output, and script references
- **Banned:** Inter, standard serif fonts (Georgia/Times), neon-glowing typography.

## 4. Component Stylings
* **Buttons:** Tactile, button-pressed interaction state with 1px border shift. Accent blue for primary actions.
* **Cards:** Rigid structural containers with 4px border radius. Used to delineate separate script configurations or system logs.
* **Inputs:** Monospaced input fields for configuration values. Clear label-above hierarchy.
* **Loaders:** Terminal-style cursor blinking effect during processing.
* **Empty States:** "No assets found" indicated by code block comments rather than text.

## 5. Layout Principles
- Information density is paramount. Dense, rigid grid systems used for configuration dashboards.
- Asymmetric layout for Hero sections: Code preview on right, functionality description on left.
- Mobile-first: Everything must stack to a single-column, full-width terminal view under 768px.
- No arbitrary white space; spacing is determined by functional relationship between script and data.

## 6. Motion & Interaction
- Rigid, precise animations matching terminal performance.
- Staggered script-execution logs cascading in real-time.
- Perpetual micro-shimmer on active automated agents.
- GPU-accelerated code syntax highlighting shifts.

## 7. Anti-Patterns (Banned)
- No emojis
- No "seamless" / "unleash" AI marketing speak
- No rounded cards or gradients
- No neon glows
- No centered layouts for Hero
- No filler UI content like "Scroll to explore"
