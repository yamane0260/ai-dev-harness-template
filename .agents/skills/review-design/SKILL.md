---
name: review-design
description: Independently review meaningful user-facing visual changes for visual hierarchy, brand/product-specific expression, responsiveness, accessibility presentation, and obvious AI-generated design patterns. Use for stakeholder-visible pages or major styling/layout changes. This is visual QA; use review-ux separately for information architecture, interaction appropriateness, settings organization, and task usability.
---

# Review Design

Use a fresh context when supported. Start with the Task Packet, rendered screenshots, changed UI paths, and `docs/DESIGN.md` plus approved references only when relevant.

1. Judge the rendered visual result, not the entire source tree.
2. Check hierarchy, typography, spacing/density, responsive states, visual accessibility, content authenticity, and consistency with the project's visual system.
3. Check unjustified generic agent defaults such as repetitive card grids, decorative pills, arbitrary gradients/glow/glass, invented metrics/testimonials, or generic marketing copy.
4. Keep visual expression project-specific, while leaving familiar interaction conventions to the UX review.
5. Inspect source only when needed to explain/fix a visible issue.
6. Run the configured visual gate when available; keep screenshots/logs as artifacts and return a concise result.
7. Human review, when needed, should answer whether the visible product/brand outcome is acceptable, not inspect CSS details.
