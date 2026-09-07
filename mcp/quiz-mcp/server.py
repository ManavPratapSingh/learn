#!/usr/bin/env python3
import sys
import os
import json
import random

def normalize_options(options_raw):
    if not options_raw or len(options_raw) < 2:
        raise ValueError("Quiz requires at least two options.")
    seen = set()
    out = []
    for opt in options_raw:
        label = opt.get("label", "").strip()
        val = opt.get("value", "").strip() or label
        desc = opt.get("description", "").strip() or None
        if not label:
            continue
        if val in seen:
            raise ValueError(f'Duplicate option value "{val}"')
        seen.add(val)
        out.append({"label": label, "value": val, "description": desc})
    return out

def coerce_correct_answer(correct_answer):
    if isinstance(correct_answer, list):
        return [str(v) for v in correct_answer]
    trimmed = str(correct_answer).strip()
    if trimmed.startswith("[") and trimmed.endswith("]"):
        try:
            parsed = json.loads(trimmed)
            if isinstance(parsed, list):
                return [str(v) for v in parsed]
        except Exception:
            pass
    return [trimmed]

def resolve_correct(correct_answer, options):
    arr = coerce_correct_answer(correct_answer)
    if not arr:
        raise ValueError("correctAnswer parameter is required.")
    by_value = {o["value"]: i + 1 for i, o in enumerate(options)}
    indices = []
    values = []
    for raw in arr:
        v = str(raw).strip()
        if v not in by_value:
            known = ", ".join([f'"{o["value"]}"' for o in options])
            raise ValueError(f'correctAnswer "{v}" does not match any option value ({known})')
        indices.append(by_value[v])
        values.append(v)
    unique_indices = sorted(list(set(indices)))
    return unique_indices, values

def is_correct(selected_indices, correct_indices):
    return sorted(selected_indices) == sorted(correct_indices)

def grade_quiz(params):
    question = params.get("question", "")
    details = params.get("details")
    explanation = params.get("explanation", "")
    multi_select = params.get("multiSelect", False)
    mode = "multi-select" if multi_select else "single-select"
    shuffle = params.get("shuffle", True)

    options = normalize_options(params.get("options", []))
    if shuffle is not False:
        random.shuffle(options)

    displayed_options = [
        {"index": i + 1, "label": o["label"], "value": o["value"], "description": o.get("description")}
        for i, o in enumerate(options)
    ]

    correct_indices, correct_values = resolve_correct(params.get("correctAnswer"), options)

    dont_know = params.get("dontKnow", False) or params.get("dont_know", False)
    selected_indices = params.get("selectedIndices", [])
    selected_values = params.get("selectedValues", [])

    if not dont_know:
        if selected_indices:
            selected_values = [
                next((o["value"] for o in displayed_options if o["index"] == idx), "")
                for idx in selected_indices
            ]
        elif selected_values:
            selected_indices = [
                next((o["index"] for o in displayed_options if o["value"] == val), 0)
                for val in selected_values
            ]
            selected_indices = [idx for idx in selected_indices if idx > 0]

    correct = False if dont_know else is_correct(selected_indices, correct_indices)

    lines = []
    lines.append(f"Question: {question}")
    if details:
        lines.append(f"Context: {details}")
    lines.append(f"Mode: {mode}")
    lines.append("")
    lines.append("Options:")

    correct_set = set(correct_indices)
    selected_set = set(selected_indices)

    for opt in displayed_options:
        is_sel = opt["index"] in selected_set
        is_key = opt["index"] in correct_set

        if dont_know:
            mark = "✓ " if is_key else "  "
        elif is_sel and is_key:
            mark = "✓ "
        elif is_sel and not is_key:
            mark = "✗ "
        elif not is_sel and is_key:
            mark = "✓ "
        else:
            mark = "  "

        lines.append(f'{mark}{opt["index"]}. {opt["label"]} (value: "{opt["value"]}")')
        if opt.get("description"):
            lines.append(f'   {opt["description"]}')

    lines.append("")
    if dont_know:
        lines.append('User Verdict: Selected "I don\'t know" (genuine knowledge gap)')
    elif correct:
        lines.append("User Verdict: ✓ Correct!")
    else:
        lines.append("User Verdict: ✗ Incorrect.")

    correct_display = ", ".join(
        [f'{idx}. {next((o["label"] for o in displayed_options if o["index"] == idx), "")}' for idx in correct_indices]
    )
    lines.append(f"Correct Answer(s): {correct_display}")

    user_note = params.get("userNote") or params.get("user_note")
    if user_note:
        lines.append(f"User Note: {user_note}")

    lines.append("")
    lines.append(f"Explanation: {explanation}")

    formatted_output = "\n".join(lines)

    return {
        "status": "answered",
        "question": question,
        "context": details,
        "mode": mode,
        "options": displayed_options,
        "correctIndices": correct_indices,
        "selectedIndices": selected_indices,
        "selectedValues": selected_values,
        "correctValues": correct_values,
        "isCorrect": correct,
        "dontKnow": dont_know,
        "explanation": explanation,
        "userNote": user_note,
        "formattedOutput": formatted_output,
    }

class QuizMcpServer:
    def start(self):
        sys.stderr.write("quiz MCP Server started on stdio (python)\n")
        sys.stderr.flush()

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                self.handle_message(msg)
            except Exception as e:
                self.send_error(None, -32700, "Parse error", str(e))

    def handle_message(self, msg):
        if not isinstance(msg, dict):
            return
        msg_id = msg.get("id")
        if msg_id is None:
            return

        method = msg.get("method")
        params = msg.get("params", {})

        if method == "initialize":
            self.send_result(msg_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "quiz-mcp", "version": "1.0.0"}
            })
        elif method == "tools/list":
            self.send_result(msg_id, {"tools": self.get_tool_definitions()})
        elif method == "tools/call":
            self.handle_tool_call(msg_id, params.get("name"), params.get("arguments", {}))
        elif method == "ping":
            self.send_result(msg_id, {})
        else:
            self.send_error(msg_id, -32601, f"Method not found: {method}")

    def get_tool_definitions(self):
        return [
            {
                "name": "quiz",
                "description": "Ask the user a GRADED question with a known correct answer, then instantly grade and give feedback (✓/✗, correct answer, explanation).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string", "description": "The single quiz question to ask."},
                        "details": {"type": "string", "description": "Optional extra context under question."},
                        "options": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "label": {"type": "string"},
                                    "value": {"type": "string"},
                                    "description": {"type": "string"}
                                },
                                "required": ["label"]
                            },
                            "minItems": 2
                        },
                        "multiSelect": {"type": "boolean"},
                        "correctAnswer": {
                            "description": "REQUIRED option value(s). Single-select: string. Multi-select: array of strings.",
                            "anyOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]
                        },
                        "explanation": {"type": "string", "description": "REQUIRED explanation."},
                        "shuffle": {"type": "boolean"},
                        "selectedValues": {"type": "array", "items": {"type": "string"}},
                        "dontKnow": {"type": "boolean"},
                        "userNote": {"type": "string"}
                    },
                    "required": ["question", "options", "correctAnswer", "explanation"]
                }
            },
            {
                "name": "evaluate_quiz_response",
                "description": "Grade a user selection against a quiz question spec.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "options": {"type": "array", "items": {"type": "object"}},
                        "correctAnswer": {"anyOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
                        "selectedValues": {"type": "array", "items": {"type": "string"}},
                        "dontKnow": {"type": "boolean"},
                        "explanation": {"type": "string"}
                    },
                    "required": ["question", "options", "correctAnswer", "explanation"]
                }
            }
        ]

    def handle_tool_call(self, msg_id, name, args):
        try:
            if name in ("quiz", "evaluate_quiz_response"):
                res = grade_quiz(args)
                self.send_result(msg_id, {
                    "content": [{"type": "text", "text": res["formattedOutput"]}],
                    "details": res
                })
                return
            self.send_error(msg_id, -32601, f"Unknown tool: {name}")
        except Exception as e:
            self.send_result(msg_id, {
                "content": [{"type": "text", "text": f"Error executing {name}: {str(e)}"}],
                "isError": True
            })

    def send_result(self, msg_id, result):
        resp = {"jsonrpc": "2.0", "id": msg_id, "result": result}
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()

    def send_error(self, msg_id, code, message, data=None):
        resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message, "data": data}}
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    server = QuizMcpServer()
    server.start()
