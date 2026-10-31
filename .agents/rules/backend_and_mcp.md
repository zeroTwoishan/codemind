# Backend Architecture & MCP Tool Directives

## Architecture Patterns
- **Django REST Framework**: Standardized viewsets, explicit serializers, permission validation (`IsAuthenticated`, owner checks), structured error envelopes.
- **Real-Time Collaboration**: Django Channels + Redis Pub/Sub for WebSockets. Real-time document diff synchronization, cursor presence broadcasting, and collision resolution.
- **AI Pipelines**: Google GenAI SDK (Gemini) with Pydantic / serializer output validation, Monaco Diff integration, and token efficiency.
- **Security & Integrity**: JWT auth headers, database transactions (`transaction.atomic()`), OWASP input validation.

## MCP Server & Tool Orchestration (Zero Restraint)
- **StitchMCP**: Generate screens, create variants, and scaffold components directly (`generate_screen_from_text`, `create_project`, `create_design_system`, `generate_variants`).
- **Figma MCP**: Extract design tokens, components, and layout files (`figma_build`, `figma_file`).
- **Sequential Thinking**: Call `sequentialthinking` via lazy MCP tool invocation for complex architectural planning, state synchronization algorithms, or distributed coordination.
- **Browser Automation**: Use browser subagents for visual inspection, responsive testing, and end-to-end user flow verification.
