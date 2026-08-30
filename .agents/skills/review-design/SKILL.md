---
name: review-design
description: Independently review meaningful user-facing visual changes for product-specific quality, usability, responsiveness, accessibility, and obvious AI-generated design patterns. Use for stakeholder-visible pages, major layout/style changes, or release-critical UI; skip for trivial non-visual edits.
---

# Review Design

Use a fresh context when supported. Start with the Task Packet, rendered screenshots, changed UI paths, and `docs/DESIGN.md` plus approved references only when relevant.

1. Judge the rendered result, not the entire source tree.
2. Check hierarchy, typography, spacing/density, responsive states, accessibility, content authenticity, and consistency with the project's visual system.
3. Check unjustified generic agent defaults such as repetitive card grids, decorative pills, arbitrary gradients/glow/glass, invented metrics/testimonials, or generic marketing copy.
4. Inspect source only when needed to explain/fix a visible issue.
5. Run the configured visual gate when available; keep screenshots/logs as artifacts and return a concise result.
6. Human review, when needed, should answer whether the visible product/brand outcome is acceptable, not inspect CSS details.
