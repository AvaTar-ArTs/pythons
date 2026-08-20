# UI Design Strategy: Taste-Skill Integration

This document outlines the implementation of high-agency design principles for the `~/python` repository, inspired by the Leonxlnx 'taste-skill' framework.

## 1. Core Layout Principles
- **Grid-First Density:** All interfaces must use a strict, gapless bento-grid structure. 
- **Asymmetry:** Standard 3-card equal rows are banned. Adopt zig-zag, 2:1, or 1:3 layout ratios for dashboard components.
- **Max-Width Containment:** All content is constrained to a 1400px centered layout to maintain editorial focus.

## 2. Typographic Hierarchy
- **Primary Headers:** Geist Mono, Bold, Tight-tracking.
- **Body:** Satoshi Regular, 16px, relaxed line-height (1.6).
- **Interface/Label:** Geist Mono, Medium, 12px.
- **Prohibitions:** No default system sans-serifs. Serif fonts are reserved exclusively for editorial flourishes.

## 3. Motion Engine (GSAP-Inspired)
- **Spring Physics:** All interactive elements must utilize spring physics (stiffness: 120, damping: 20).
- **Staggered Reveals:** Lists and grids must use a 50ms cascade delay between elements.
- **Perpetual Micro-Interaction:** Active dashboard widgets require a subtle, infinite 0.5% scale pulse.

## 4. Visual Assets & Reference Boards
- Use `imagegen-frontend-web` and `brandkit` skills to generate UI reference boards before coding implementation.
- All reference boards must be section-specific and maintain a unified, high-contrast palette.

## 5. Implementation Workflow
1. **Design Board:** Generate UI reference imagery (using `brandkit`).
2. **Analysis:** Review image boards against these design rules.
3. **Draft:** Implement using CSS Grid (no percentage-based `calc` hacks).
4. **Motion:** Layer in spring-based interactions via `framer-motion` or GSAP.
