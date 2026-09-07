#!/usr/bin/env python3
import sys
import os
import json

def normalize_options(options_raw):
    out = []
    for opt in options_raw or []:
        label = opt.get("label", "").strip()
        val = opt.get("value", "").strip() or label
        desc = opt.get("description", "").strip() or None
        if label:
            out.append({"label": label, "value": val, "description": desc})
    return out

def get_other_label(options):
    if any(o["label"].lower() == "other" for o in options):
        return "Other (custom)"
    return "Other"

def process_question(params):
    question = params.get("question", "")
    details = params.get("details")
    options = normalize_options(params.get("options", []))
    multi_select = params.get("multiSelect", False)

    mode = "text" if len(options) == 0 else ("multi-select" if multi_select else "single-select")

    answers = []

    if mode == "text":
        text_resp = params.get("textResponse") or ""
        if not text_resp and params.get("selectedAnswers"):
            text_resp = params["selectedAnswers"][0].get("text", "")
        trimmed = text_resp.strip()
        answers.append({"type": "text", "label": trimmed, "value": trimmed})
    else:
        other_text = params.get("otherText")
        if other_text and other_text.strip():
            o_trimmed = other_text.strip()
            answers.append({"type": "other", "label": o_trimmed, "value": o_trimmed})

        sel_ans = params.get("selectedAnswers", [])
        for sa in sel_ans:
            sa_type = sa.get("type")
            if sa_type == "other" and sa.get("text"):
                o_txt = sa["text"].strip()
                answers.append({"type": "other", "label": o_txt, "value": o_txt})
            elif sa.get("index") is not None and 1 <= sa["index"] <= len(options):
                opt = options[sa["index"] - 1]
                answers.append({"type": "option", "label": opt["label"], "value": opt["value"], "index": sa["index"]})
            elif sa.get("value"):
                idx = next((i for i, o in enumerate(options) if o["value"] == sa["value"] or o["label"] == sa["value"]), -1)
                if idx != -1:
                    opt = options[idx]
                    answers.append({"type": "option", "label": opt["label"], "value": opt["value"], "index": idx + 1})

    lines = []
    lines.append(f"Question: {question}")
    if details:
        lines.append(f"Context: {details}")
    lines.append(f"Mode: {mode}")
    lines.append("")

    if options:
        lines.append("Available Options:")
        for idx, opt in enumerate(options):
            desc_str = f' ({opt["description"]})' if opt.get("description") else ""
            lines.append(f'  {idx + 1}. {opt["label"]}{desc_str}')
        lines.append(f"  - {get_other_label(options)} (custom text write-in)")
        lines.append("")

    if not answers:
        lines.append("Status: Awaiting user response.")
    else:
        lines.append("User Answers:")
        for ans in answers:
            if ans["type"] == "text":
                lines.append(f'  - Answer: {ans["label"] if ans["label"] else "(empty)"}')
            elif ans["type"] == "other":
                lines.append(f'  - Other (custom): {ans["label"]}')
            else:
                lines.append(f'  - {ans["index"]}. {ans["label"]}')

    formatted_output = "\n".join(lines)

    return {
        "status": "answered",
        "question": question,
        "context": details,
        "mode": mode,
        "options": options,
        "answers": answers,
        "formattedOutput": formatted_output,
    }

class AskUserQuestionMcpServer:
    def start(self):
        sys.stderr.write("ask_user_question MCP Server started on stdio (python)\n")
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
                "serverInfo": {"name": "ask-user-question-mcp", "version": "1.0.0"}
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
                "name": "ask_user_question",
                "description": "Ask the user a single question and pause execution until they answer.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string", "description": "The single question to ask."},
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
                            }
                        },
                        "multiSelect": {"type": "boolean"},
                        "selectedAnswers": {"type": "array", "items": {"type": "object"}},
                        "otherText": {"type": "string"},
                        "textResponse": {"type": "string"}
                    },
                    "required": ["question"]
                }
            },
            {
                "name": "process_question_answer",
                "description": "Process and format user answers for an ask_user_question call.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "options": {"type": "array", "items": {"type": "object"}},
                        "selectedAnswers": {"type": "array", "items": {"type": "object"}},
                        "otherText": {"type": "string"},
                        "textResponse": {"type": "string"}
                    },
                    "required": ["question"]
                }
            }
        ]

    def handle_tool_call(self, msg_id, name, args):
        try:
            if name in ("ask_user_question", "process_question_answer"):
                res = process_question(args)
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
    server = AskUserQuestionMcpServer()
    server.start()
