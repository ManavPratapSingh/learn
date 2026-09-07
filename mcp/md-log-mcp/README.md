# md-log MCP Server (`md-log-mcp`)

A Model Context Protocol (MCP) server that mirrors session conversations, prompts, responses, quiz/QA callouts, and custom notes to a target Markdown file.

Designed for long teaching/learning sessions where session logs are read in rendered Markdown previewers (like Obsidian, VS Code Markdown Preview, etc.).

---

## 🛠 Features

- **Callout Rendering**: Automatically formats logged events into GitHub/Obsidian style Markdown callouts (`> [!quote] YOU`, `> [!abstract] ASSISTANT`, `> [!question] Question`, `> [!success] Quiz — correct ✓`, etc.).
- **Skill Block Cleaning**: Strips out raw `<skill>...</skill>` prompt context blocks, leaving clean high-signal notes.
- **Thread Safety**: Appends logs with queue serialization to avoid concurrency file conflicts.
- **Protocol Support**: Works with standard MCP over `stdio` transport.

---

## 📦 Exposed MCP Tools

| Tool Name | Description | Key Arguments |
| :--- | :--- | :--- |
| `set_log_file` | Set the active target `.md` file path | `filepath` (string), `create_if_missing` (boolean) |
| `stop_logging` | Stop logging to active markdown file | none |
| `get_log_status` | Return current logging status and file path | none |
| `log_user_message` | Log user prompt callout (`> [!quote] YOU`) | `text` (string) |
| `log_assistant_message` | Log assistant message (`> [!abstract] ASSISTANT`) | `text` (string), `sender_name` (optional string) |
| `log_question` | Log question/quiz callout (`> [!question]`) | `question` (string), `options` (array), `context` (string) |
| `log_quiz_answer` | Log quiz feedback (`> [!success]` / `> [!failure]`) | `correct` (bool), `answers` (array), `explanation` (string) |
| `log_ask_answer` | Log user question response (`> [!example]`) | `answers` (array), `status` (string) |
| `log_custom_entry` | Log custom callout (`note`, `tip`, `warning`, etc.) | `text` (string), `callout_type` (string), `title` (string) |

---

## 🚀 How to Use in Antigravity

Add the following to your workspace `.agents/mcp_config.json` or global `~/.gemini/config/mcp_config.json`:

```json
{
  "mcpServers": {
    "md-log": {
      "command": "node",
      "args": ["/absolute/path/to/learn/md-log-mcp/dist/index.js"]
    }
  }
}
```

Or run via `tsx`:

```json
{
  "mcpServers": {
    "md-log": {
      "command": "npx",
      "args": ["tsx", "/absolute/path/to/learn/md-log-mcp/src/index.ts"]
    }
  }
}
```
