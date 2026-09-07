# ask_user_question MCP Server (`ask-user-question-mcp`)

A Model Context Protocol (MCP) server port of `./extensions/ask-user-question.ts` for soliciting user feedback, preferences, decisions, or free-text answers.

---

## 🛠 Features

- **Supports 3 Question Modes**:
  1. `text`: Free-form text response (when options are omitted/empty).
  2. `single-select`: Single-choice option selection.
  3. `multi-select`: Multi-choice option selection.
- **Automatic "Other" Write-in Support**: Users can always write custom input under "Other" when options are present.
- **Structured Formatting**: Formats questions and selections for model context.

---

## 📦 Tools

### 1. `ask_user_question`
Asks a single clarifying question, preference question, or decision question.

### 2. `process_question_answer`
Helper tool to format user responses into standard structured context.

---

## 🚀 Usage in Antigravity

Add the server to `.agents/mcp_config.json`:

```json
{
  "mcpServers": {
    "ask-user-question": {
      "command": "python3",
      "args": ["/home/manav/learn/mcp/ask-user-question-mcp/server.py"]
    }
  }
}
```
