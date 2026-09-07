# Rule: Workspace Hygiene & Zero File Pollution for Learning Sessions

Whenever starting, running, or managing learning sessions and tool executions:

1. **NO WORKSPACE POLLUTION**:
   - NEVER create temporary test scripts, scratch python files, or transient runners inside the project workspace directory (e.g. `/home/manav/learn/`).
   - All session helper execution MUST be performed in-memory (`python3 -c "..."`) or stored in the dedicated conversation scratch folder (`<appDataDir>/brain/<conversation-id>/scratch/`).

2. **SESSION FILE MANAGEMENT**:
   - Maintained dedicated tools/MCP servers live in clean folders (`mcp/`, `.agents/`).
   - Rendered visual assets (PNG diagrams, flowcharts) belong in `./viz/`.
   - Never scatter one-off `.py` or `.tmp` files across the workspace.

3. **TEACHING SESSION ENTRY POINT & FRONTEND MIRRORING**:
   - Always run **Phase 0 (Setup)**: Ask for the absolute path to the user's frontend Obsidian note.
   - Link `md-log-mcp` to that note.
   - Every prompt, explanation, LaTeX equation, question, research finding, and diagram MUST be mirrored live to the Obsidian note.
