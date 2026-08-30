---
name: review-design
description: Review user-facing UI for product-specific visual quality, usability, responsiveness, accessibility, and obvious AI-generated design patterns. Use for pages/components that customers or stakeholders will see, especially marketing pages, dashboards, and major layout/style changes before release.
---

# Review Design

1. Read `docs/DESIGN.md`, real brand/content assets, and any approved reference screens before judging aesthetics.
2. Render the actual implementation. Review screenshots at representative viewport sizes; source inspection alone is not visual QA.
3. Check information hierarchy, typography, spacing/rhythm, density, responsive behavior, interaction states, content authenticity, accessibility, and consistency with the project's visual system.
4. Check for generic agent defaults that are not justified by the product: repetitive card grids, decorative pills/badges, arbitrary gradients/glow/glass effects, invented metrics/testimonials, generic marketing copy, or style choices based only on vague adjectives.
5. Prefer project-specific content and layout logic over swapping one fashionable AI default for another.
6. Compare with the chosen reference/source-of-truth where one exists. Fix the largest perceptual discrepancies first.
7. Run the configured `visual` gate if available and record screenshots/evidence.
8. Human review, when needed, should answer "Is this an acceptable product/brand outcome?" rather than inspect CSS implementation details.
