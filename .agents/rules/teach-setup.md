# Rule: Teaching Session Initialization & Obsidian Frontend Mirroring

Whenever the user starts a teaching or learning session:

1. **Auto-Approval**: Tool calls (`md-log-mcp`, `quiz-mcp`, `ask-user-question-mcp`, `research`) and file access to the active frontend note are auto-approved via `.agents/hooks.json` and `.agents/hooks/hooks_auto_allow.py` so interactive popups do not hinder learning.
2. **Phase 0 Setup & Dynamic Permission Granting**:
   - Ask for the absolute file path to the user's frontend Obsidian note.
   - Call `set_log_file` on `md-log-mcp` with that file path. `set_log_file` automatically saves the path to `.agents/active_frontend_note.json`.
   - The hook `.agents/hooks/hooks_auto_allow.py` dynamically auto-approves all read/write operations to the file and its parent Obsidian vault for the entire session without prompting for permission.
3. **Obsidian is the Only Screen**:
   - The user views the lesson ONLY on their Obsidian screen.
   - EVERY explanation, question (including 1a and 1b together), subagent research output, status update, and diagram MUST be logged to `md-log-mcp` before or during the turn response.
4. **No Link Pollution**:
   - NEVER wrap node labels or step tags in square brackets like `[D1]` or `[[D1]]` in titles, text, or Mermaid diagrams.
   - Obsidian parses `[D1]` as Markdown reference / Wiki links, causing it to register phantom note files (`D1`, `D2`, etc.) in the vault graph. Use plain text or parentheses (`D1: ...` or `(D1 → D2)`).
