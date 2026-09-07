#!/usr/bin/env python3
import sys
import os
import json
import re
import threading

class MdLogger:
    def __init__(self):
        self.log_file = None
        self.lock = threading.Lock()

    def set_log_file(self, filepath: str, create_if_missing: bool = True) -> str:
        resolved = os.path.abspath(filepath)
        dir_name = os.path.dirname(resolved)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        if not os.path.exists(resolved):
            if create_if_missing:
                with open(resolved, "w", encoding="utf-8") as f:
                    pass
            else:
                raise FileNotFoundError(f"File does not exist: {resolved}")

        self.log_file = resolved

        # Auto-update hook state for seamless auto-approval
        try:
            cfg = "/home/manav/learn/.agents/active_frontend_note.json"
            os.makedirs(os.path.dirname(cfg), exist_ok=True)
            with open(cfg, "w", encoding="utf-8") as f:
                json.dump({"filepath": resolved}, f, indent=2)
        except Exception:
            pass

        return resolved

    def stop_logging(self):
        prev = self.log_file
        self.log_file = None
        return prev

    def get_log_file(self):
        return self.log_file

    def _append_to_file(self, text: str):
        if not self.log_file:
            return
        with self.lock:
            try:
                current = ""
                if os.path.exists(self.log_file):
                    with open(self.log_file, "r", encoding="utf-8") as f:
                        current = f.read()
                prefix = "\n\n" if len(current.strip()) > 0 else ""
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(prefix + text + "\n")
            except Exception:
                pass

    def format_callout(self, type_str: str, title: str, body_lines: list) -> str:
        lines = [f"> [!{type_str}] {title}"]
        for line in body_lines:
            lines.append(">" if len(line) == 0 else f"> {line}")
        return "\n".join(lines)

    def strip_skill_blocks(self, text: str) -> str:
        def replace_skill(match):
            attrs = match.group(1)
            name_match = re.search(r'name="([^"]+)"', attrs)
            name = name_match.group(1) if name_match else "(unknown)"
            return f"> [!note] SKILL loaded: {name}"

        return re.sub(r'<skill\b([^>]*)>[\s\S]*?<\/skill>', replace_skill, text)

    def log_user_message(self, text: str) -> bool:
        if not self.log_file:
            return False
        trimmed = self.strip_skill_blocks(text.strip())
        if not trimmed:
            return False
        block = self.format_callout("quote", "YOU", trimmed.split("\n"))
        self._append_to_file(block)
        return True

    def log_assistant_message(self, text: str, sender_name: str = "ASSISTANT") -> bool:
        if not self.log_file:
            return False
        trimmed = text.strip()
        if not trimmed:
            return False
        block = self.format_callout("abstract", sender_name, trimmed.split("\n"))
        self._append_to_file(block)
        return True

    def log_question(self, question: str, options: list = None, context: str = None, label: str = "Question") -> bool:
        if not self.log_file:
            return False
        options = options or []
        body = []
        for line in question.split("\n"):
            body.append(line)
        if context:
            body.append("")
            for line in context.split("\n"):
                body.append(line)
        if options:
            body.append("")
            for i, opt in enumerate(options):
                lbl = opt.get("label", str(opt)) if isinstance(opt, dict) else str(opt)
                body.append(f"{i + 1}. {lbl}")
        block = self.format_callout("question", label, body)
        self._append_to_file(block)
        return True

    def log_quiz_answer(self, details: dict) -> bool:
        if not self.log_file:
            return False
        status = details.get("status")
        if status == "cancelled":
            block = self.format_callout("warning", "Quiz — cancelled", ["(user skipped)"])
        elif status == "unavailable":
            block = self.format_callout("warning", "Quiz — unavailable", [details.get("message", "")])
        else:
            dont_know = details.get("dont_know", False) or details.get("dontKnow", False)
            correct = details.get("correct", False)
            type_str = "question" if dont_know else ("success" if correct else "failure")
            title = "Quiz — I don't know" if dont_know else ("Quiz — correct ✓" if correct else "Quiz — incorrect ✗")
            body = []

            if dont_know:
                body.append("Your answer: I don't know")
            else:
                answers = details.get("answers", [])
                sel = ", ".join([f"{a.get('index')}. {a.get('label')}" for a in answers]) if answers else "(none)"
                body.append(f"Your answer: {sel}")

            correct_indices = details.get("correct_indices", []) or details.get("correctIndices", [])
            if correct_indices:
                correct_str = ", ".join([str(i) for i in correct_indices])
                body.append(f"Correct answer: {correct_str}")

            if details.get("note"):
                body.append("")
                note_lines = str(details.get("note")).split("\n")
                body.append(f"Note: {note_lines[0]}")
                for line in note_lines[1:]:
                    body.append(line)

            if details.get("explanation"):
                body.append("")
                for line in str(details.get("explanation")).split("\n"):
                    body.append(line)

            block = self.format_callout(type_str, title, body)

        self._append_to_file(block)
        return True

    def log_ask_answer(self, details: dict) -> bool:
        if not self.log_file:
            return False
        status = details.get("status")
        if status == "cancelled":
            block = self.format_callout("warning", "Question — cancelled", ["(user skipped)"])
        elif status == "unavailable":
            block = self.format_callout("warning", "Question — unavailable", [details.get("message", "")])
        else:
            answers = details.get("answers", [])
            body = []
            for a in answers:
                if a.get("type") == "other":
                    body.append(f"Other: {a.get('label')}")
                elif a.get("type") == "text":
                    body.append(a.get("label"))
                else:
                    idx_str = f"{a.get('index')}. " if a.get("index") is not None else ""
                    body.append(f"{idx_str}{a.get('label')}")
            if not body:
                body.append("(no answer)")
            block = self.format_callout("example", "Answer", body)

        self._append_to_file(block)
        return True

    def log_custom_entry(self, text: str, callout_type: str = None, title: str = None) -> bool:
        if not self.log_file:
            return False
        if callout_type:
            block = self.format_callout(callout_type, title or callout_type.upper(), text.split("\n"))
        else:
            block = text
        self._append_to_file(block)
        return True

class McpServer:
    def __init__(self):
        self.logger = MdLogger()

    def start(self):
        sys.stderr.write("md-log MCP Server started on stdio (python)\n")
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

    def handle_message(self, msg: dict):
        if not isinstance(msg, dict):
            return

        msg_id = msg.get("id")

        if msg_id is None:
            # Notification
            return

        method = msg.get("method")
        params = msg.get("params", {})

        if method == "initialize":
            self.send_result(msg_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "md-log-mcp", "version": "1.0.0"}
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
                "name": "set_log_file",
                "description": "Set the active Markdown file path to mirror session logs and callouts to.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string", "description": "Path to the markdown file"},
                        "create_if_missing": {"type": "boolean", "default": True}
                    },
                    "required": ["filepath"]
                }
            },
            {
                "name": "stop_logging",
                "description": "Stop mirroring session logs to the active markdown file.",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_log_status",
                "description": "Get current status and active markdown log file path.",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "log_user_message",
                "description": "Append a user prompt callout (> [!quote] YOU) to the markdown log.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"text": {"type": "string", "description": "The user prompt text to log"}},
                    "required": ["text"]
                }
            },
            {
                "name": "log_assistant_message",
                "description": "Append an assistant response callout (> [!abstract]) to the markdown log.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "The assistant text to log"},
                        "sender_name": {"type": "string", "default": "ASSISTANT"}
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "log_question",
                "description": "Append a question or quiz callout (> [!question]) to the markdown log.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "options": {"type": "array", "items": {"type": "string"}},
                        "context": {"type": "string"},
                        "label": {"type": "string", "default": "Question"}
                    },
                    "required": ["question"]
                }
            },
            {
                "name": "log_quiz_answer",
                "description": "Append quiz feedback callout (> [!success] / > [!failure]) to the markdown log.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "dont_know": {"type": "boolean"},
                        "correct": {"type": "boolean"},
                        "answers": {"type": "array", "items": {"type": "object"}},
                        "correct_indices": {"type": "array", "items": {"type": "number"}},
                        "note": {"type": "string"},
                        "explanation": {"type": "string"}
                    }
                }
            },
            {
                "name": "log_ask_answer",
                "description": "Append user answer callout (> [!example] Answer) for a question tool call.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "answers": {"type": "array", "items": {"type": "object"}}
                    }
                }
            },
            {
                "name": "log_custom_entry",
                "description": "Append a custom text or markdown callout (> [!note], > [!tip], > [!warning], etc.) to the log file.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "callout_type": {"type": "string"},
                        "title": {"type": "string"}
                    },
                    "required": ["text"]
                }
            }
        ]

    def handle_tool_call(self, msg_id, name: str, args: dict):
        try:
            res_text = ""
            if name == "set_log_file":
                filepath = args.get("filepath")
                create_if_missing = args.get("create_if_missing", True)
                resolved = self.logger.set_log_file(filepath, create_if_missing)
                res_text = f"Log file set to: {resolved}"
            elif name == "stop_logging":
                prev = self.logger.stop_logging()
                res_text = f"Stopped logging to: {prev}" if prev else "No active log file was set."
            elif name == "get_log_status":
                active = self.logger.get_log_file()
                res_text = f"Logging is ACTIVE -> {active}" if active else "Logging is INACTIVE (no file linked)."
            elif name == "log_user_message":
                ok = self.logger.log_user_message(args.get("text", ""))
                res_text = "User message logged successfully." if ok else "Failed to log user message."
            elif name == "log_assistant_message":
                ok = self.logger.log_assistant_message(args.get("text", ""), args.get("sender_name", "ASSISTANT"))
                res_text = "Assistant message logged successfully." if ok else "Failed to log assistant message."
            elif name == "log_question":
                raw_opts = args.get("options", [])
                opts = [{"label": o} if isinstance(o, str) else o for o in raw_opts]
                ok = self.logger.log_question(args.get("question", ""), opts, args.get("context"), args.get("label", "Question"))
                res_text = "Question logged successfully." if ok else "Failed to log question."
            elif name == "log_quiz_answer":
                ok = self.logger.log_quiz_answer(args)
                res_text = "Quiz answer logged successfully." if ok else "Failed to log quiz answer."
            elif name == "log_ask_answer":
                ok = self.logger.log_ask_answer(args)
                res_text = "Ask answer logged successfully." if ok else "Failed to log ask answer."
            elif name == "log_custom_entry":
                ok = self.logger.log_custom_entry(args.get("text", ""), args.get("callout_type"), args.get("title"))
                res_text = "Custom entry logged successfully." if ok else "Failed to log entry."
            else:
                self.send_error(msg_id, -32601, f"Unknown tool: {name}")
                return

            self.send_result(msg_id, {
                "content": [{"type": "text", "text": res_text}]
            })
        except Exception as e:
            self.send_result(msg_id, {
                "content": [{"type": "text", "text": f"Error executing tool {name}: {str(e)}"}],
                "isError": True
            })

    def send_result(self, msg_id, result: dict):
        resp = {"jsonrpc": "2.0", "id": msg_id, "result": result}
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()

    def send_error(self, msg_id, code: int, message: str, data=None):
        resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message, "data": data}}
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    server = McpServer()
    server.start()
