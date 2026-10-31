# Frontend & Anti-Slop Design Directives

## Typography & Pairing
- Primary: Modern sans-serif (Geist, Satoshi, Cabinet Grotesk).
- Monospace: JetBrains Mono or Geist Mono for code blocks and Monaco editor integration.
- Banned defaults: System Arial, uncustomized Inter on dark slate.

## Visual Hierarchy & Component Aesthetics
- **Double-Bezel (Doppelrand) Architecture**:
  - Outer: `bg-white/5` or `bg-black/5` with thin border ring.
  - Inner: concentric radius with inset top highlight `shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`.
- **Button-in-Button CTAs**: Pill container with nested trailing action icon badge flush inside right padding.
- **Card Grids**: Varied bento layouts with high visual contrast. Banned: repetitive 3-box equal grids across sections.
- **Surfaces**: Calibrated dark mode with deep OLED charcoal/black (`#0A0A0B`, `#121214`), subtle border dividers (`border-white/10`), and a single electric accent color.

## Motion Guidelines (Emil Kowalski + Jakub Krehel)
- Micro-interactions: 150-250ms duration, spring physics with zero jitter.
- Utility actions: Instant feel, no excessive blur or sluggish bounce on functional elements.
- Page entrances: Staggered reveal for hero elements (`motion/react` or GSAP ScrollTrigger).
