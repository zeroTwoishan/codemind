# CodeMind Vault — Agent Directives & Operational Rules

## 0. Mandatory MCP Server & Skill Orchestration Rule (Zero Restraint)
- **Mandatory Sequential Thinking**: You MUST proactively, extensively, and routinely execute `sequentialthinking` MCP tool calls for every non-trivial step, architectural decision, full-stack decomposition, state sync design, and complex debugging task. Never bypass or rush through multi-step reasoning.
- **Mandatory StitchMCP Integration**: You MUST proactively use `StitchMCP` (`create_project`, `generate_screen_from_text`, `generate_variants`, `create_design_system`, `edit_screens`, `download_assets`) to scaffold, generate, iterate, and refine UI screens and design tokens.
- **Collaborative Phased Execution & Educational Transparency**: Never perform large multi-step changes silently or alone. Always work strictly **phase-by-phase**, explaining clearly:
  1. **WHAT** was done (concrete changes and files modified).
  2. **HOW** it works (code mechanics, data flow, architecture).
  3. **WHY** it was done (mental model, purpose, architectural necessity).
  Verify each phase before moving to the next.

---

## 1. Zero-Restraint Skill & MCP Execution Policy
- **No Holding Back**: You are instructed to actively, aggressively, and proactively leverage all learned frontend design skills, backend engineering skills, and MCP servers without artificial restraint.
- **Continuous Skill Activation**: Whenever a task touches frontend design, UI components, backend architecture, real-time WebSockets, AI pipelines, or testing, automatically activate the corresponding learned skills and patterns.
- **Proactive MCP Server Integration**:
  - **Sequential Thinking** (`sequentialthinking`): Use for complex multi-step reasoning, architectural decomposition, state synchronization, and algorithmic design.
  - **StitchMCP** (`create_project`, `generate_screen_from_text`, `generate_variants`, `create_design_system`, `edit_screens`, `download_assets`): Proactively use to scaffold, generate, and iterate on UI screens, component variants, and design tokens.
  - **Figma MCP** (`figma_build`, `figma_file`, `figma_design_system`): Use for extracting design specs, asset pipelines, and design system alignment.
  - **Browser Subagents / QA**: Validate UI/UX directly with browser inspection, visual verification, and automated workflows.
  - **Image Generation (`generate_image`)**: Never use placeholder images or fake visual text; generate production-quality visual assets, mockups, and preview thumbnails directly.

---

## 2. Master Frontend Design & Aesthetics Registry
Always integrate and apply these dedicated global design & engineering skills across every visual surface:

### A. Design Intelligence & Anti-Slop Craft
* **`anti-slop-design-mastery`**: Multi-dimensional anti-slop rules, visual density control, zero-clutter surfaces.
* **`ui-ux-pro-max`**: Access to 84 curated UI styles, 192 calibrated palettes, and 74 bespoke typography pairings.
* **`impeccable`**: Elite interface design commands (`craft`, `shape`, `polish`, `critique`).
* **`redesign-existing-projects`**: Upgrading standard MVPs into polished, commercial-grade tools.
* **`make-interfaces-feel-better`**: Tactile micro-details, click responsiveness, cursor state precision.
* **`frontend-design-direction`**: Cohesive dark-theme developer tokens, border alpha rings, and glow calibrations.

### B. Real-World Design Systems & Foundations
* **`75-company-designs`**: Benchmark and borrow patterns from industry leaders (Linear, Vercel, Stripe, Raycast, GitHub, Apple).
* **`design-system`**: Strict token architectures for color, typography, surface elevations, and radii.
* **`ui-styling`**: shadcn/ui + Tailwind v4 component guidelines, accessible primitives, and consistent utility composition.
* **`design-is`**: Adherence to Dieter Rams' Ten Principles of Good Design.

### C. Motion, Micro-Interactions & Spring Physics
* **`design-motion-principles`**: The 3-designer lens (Emil Kowalski, Jakub Krehel, Paco Coursey) for utilitarian vs expressive motion.
* **`motion-foundations`**: Strict spring presets (`stiffness: 400, damping: 30`), layout transitions, and reduced-motion fallbacks.
* **`motion-patterns`**: Polished animations for modals, sidebars, toast banners, tooltips, and tabs.
* **`motion-advanced`**: Drag-and-drop mechanics, gesture responsiveness, and text stagger effects.
* **`motion-ui`**: End-to-end component motion systems in React using `motion/react`.

### D. Accessibility & Frontend Engineering
* **`accessibility` & `frontend-a11y`**: WCAG 2.2 Level AA compliance, semantic ARIA roles, focus visible rings, keyboard navigation traps.
* **`frontend-patterns`**: Modern React 19 state boundaries, TanStack Query cache invalidation, and custom hooks.

### E. Visual QA & Verification
* **`qa` & `browser-qa`**: Automated visual checks, responsive layout audits, and quality scoring (1–5).
* **`ui-demo`**: Recording polished UI walkthroughs and interaction validation.

---

## 3. Strict Visual & Interaction Rules (Anti-Slop Standard)

### Visual Aesthetics
- **Banned AI Tells**: No default Inter-on-slate-900, no generic purple/blue glow mesh gradients, no equal-size 3-card monotony, no fake div screenshots, no repetitive nested card boxes (box-in-a-box).
- **Typography & Hierarchy**:
  - Pair distinctive modern typefaces: **Geist + JetBrains Mono**, **Satoshi + JetBrains Mono**, or **Cabinet Grotesk + Inter Tight**.
  - Maintain crisp line heights and proper descender clearance (`pb-1` for italics).
- **Layout & Structure**:
  - **Hero Viewport Discipline**: Hero fits in the initial viewport (`pt-24` max top padding, max 4 elements in stack, max 2-line headline, max 20-word subtext).
  - **Section Variety**: Never repeat the same layout structure (bento, split, 3-card) twice on a single page.
  - **Doppelrand (Double-Bezel) Cards**: Outer shell (`bg-white/5` or `bg-black/5` with subtle border ring) + Inner card core (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]` with concentric radii).
  - **Button-in-Button CTAs**: Sleek pill buttons with trailing icon badge wrappers flush inside right padding.
- **Color & Surface Calibration**:
  - Dark mode default with calibrated dark surfaces (`#09090B`, `#121215`, `#18181C`).
  - Single saturated accent (e.g., electric emerald, neon cyan, or crisp amber, < 80% saturation) kept strictly consistent page-wide.
  - Strict WCAG AA contrast ratios (4.5:1 body, 3:1 large headers).

### Motion & Interaction Discipline
- Prioritize **speed, crisp spring physics, and subtle utility motion**.
- Micro-interactions: 150–250ms transitions, smooth hover states, deliberate active press feedback, layout animations with `motion/react`.
- No gratuitous blur-on-mount or slow bouncing animations on utilitarian controls.

---

## 4. Backend & Full-Stack Architecture Standards

### Robust Architecture
- **Django REST Framework**: Use clean ViewSets, ModelSerializers, clear permission classes (`IsAuthenticated`, custom object-level permissions), and standard envelope response formats.
- **Real-Time Collaboration**: Django Channels + ASGI (Daphne/Uvicorn) + Redis Channel Layer for room-based WebSocket synchronization, presence tracking, and conflict detection.
- **Authentication**: SimpleJWT with short-lived access tokens, refresh token rotation, and secure header transmission (`Authorization: Bearer <token>`).
- **AI Integrations**: Google GenAI SDK (Gemini) with structured output parsing (Pydantic / DRF serializers), streaming responses, diff computation for Monaco DiffEditor, and rate-limit guardrails.
- **Database & Data Layer**: Strict foreign keys, indexed lookups (slugs, user IDs, room IDs), atomic database transactions (`transaction.atomic()`), and automated Django migrations.

### Engineering Practices
- **Superpowers TDD Workflow**: Spec in digestible chunks, write test cases (pytest / pytest-django / pytest-asyncio), implement cleanly, and verify against quality gates.
- **Full Output Enforcement**: Never truncate code with `// ...` or `// rest of code`. Always provide complete, drop-in implementations.
- **Code Cleanliness**: Avoid boilerplate, keep controllers slim, encapsulate business logic in services/selectors, and heavily comment complex logic for clarity.