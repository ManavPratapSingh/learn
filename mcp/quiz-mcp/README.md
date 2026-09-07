# quiz MCP Server (`quiz-mcp`)

A Model Context Protocol (MCP) server port of `./extensions/quiz.ts` for asking **GRADED** questions with instant evaluation, option shuffling, and detailed explanations.

---

## 🛠 Features

- **Graded Evaluation**: Positively verifies user selections against target option `value` identifiers.
- **Option Shuffling**: Automatically randomizes option presentation order unless explicitly disabled.
- **Support for Multi-Select & Single-Select**: Handles single-choice or multi-choice quizzes with exact-set matching.
- **Support for "I don't know"**: Recognizes explicit uncertainty as a distinct knowledge gap rather than an unlucky guess.
- **Detailed Explanations**: Reinforces why the correct answer is right and why distractors are wrong.

---

## 📦 Tools

### 1. `quiz`
Poses and evaluates a graded multiple-choice or multi-select quiz question.

### 2. `evaluate_quiz_response`
Evaluates a specific user answer against a quiz specification.

---

## 🚀 Usage in Antigravity

Add the server to `.agents/mcp_config.json`:

```json
{
  "mcpServers": {
    "quiz": {
      "command": "python3",
      "args": ["/home/manav/learn/quiz-mcp/server.py"]
    }
  }
}
```
