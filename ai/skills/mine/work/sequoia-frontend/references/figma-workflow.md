# Figma-to-Sequoia workflow

## Source of truth

Use Figma's remote MCP server when available. Figma recommends the remote server, and its design-context workflow is link-based:

- [Figma MCP introduction](https://developers.figma.com/docs/figma-mcp-server/)
- [Remote server installation](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/)
- [Tools and prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
- [What the MCP sends vs. what the agent does](https://developers.figma.com/docs/figma-mcp-server/mcp-vs-agent/)

The MCP server supplies structured design context; the coding agent must adapt it to the real codebase and design system.

## Extraction sequence

1. Validate the supplied URL and identify its file and selected node.
2. Request design context for that exact frame/layer.
3. Request a screenshot for visual comparison.
4. Retrieve variables, styles, component instances, and Code Connect mappings available for the node.
5. Download required raster/vector assets with the Figma asset tool. Preserve provided assets; do not redraw them with CSS or replace them with generic placeholders.
6. Identify variants and nearby frames representing responsive layouts or interaction states.

If a whole-file link contains multiple candidate screens, ask which frame to implement. A precise frame link allows design extraction, but never skip the confirmed implementation contract required by `SKILL.md`.

## Translate, do not paste

- Map Figma component instances to Eureka or existing product components.
- Map Figma variables to semantic Eureka tokens. Do not paste raw hex values when a semantic token exists.
- Convert auto-layout intent into resilient flex/grid behavior rather than absolute positioning.
- Treat exact canvas positions as hints unless the design represents a fixed overlay or diagram.
- Reuse real typography, icons, and assets available in the workspace or Figma export.
- Ignore framework/library choices in generated design context when they conflict with the owning repo.
- Do not add a dependency merely because generated context imports it.

## Fidelity pass

Verify at the Figma viewport first, then at a narrow and wider viewport:

- content hierarchy, spacing, alignment, sizing, wrapping, and overflow;
- token-resolved colors, typography, borders, radii, shadows, and icons;
- hover, focus, pressed, disabled, loading, empty, error, and validation states;
- keyboard navigation, accessible names, focus visibility, and dialog behavior;
- dark/high-contrast/theme variants supported by the target product.

Use the attached DevTools browser, reuse the current tab, and compare the rendered screenshot to Figma. Inspect computed styles for disagreements instead of compensating with unverified arbitrary values.
