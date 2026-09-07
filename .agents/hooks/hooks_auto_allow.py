#!/usr/bin/env python3
import sys
import json
import os

CONFIG_FILE = "/home/manav/learn/.agents/active_frontend_note.json"

def get_active_frontend_path():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("filepath", "").strip()
    except Exception:
        pass
    return ""

def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw else {}
    except Exception:
        data = {}

    tool_name = data.get("tool_name", "")
    args = data.get("tool_args", {}) if isinstance(data.get("tool_args"), dict) else {}

    target_path = (
        args.get("filepath") or
        args.get("TargetFile") or
        args.get("AbsolutePath") or
        args.get("SearchPath") or
        args.get("DirectoryPath") or
        ""
    )

    active_path = get_active_frontend_path()
    active_dir = os.path.dirname(active_path) if active_path else ""

    reason = "Auto-approved for teaching session."

    if active_path and target_path:
        norm_target = os.path.abspath(target_path)
        norm_active = os.path.abspath(active_path)
        norm_dir = os.path.abspath(active_dir) if active_dir else ""

        if norm_target == norm_active:
            reason = f"Auto-approved access to active frontend note: {active_path}"
        elif norm_dir and norm_target.startswith(norm_dir):
            reason = f"Auto-approved access inside active vault directory: {norm_dir}"

    output = {
        "decision": "allow",
        "reason": reason
    }
    sys.stdout.write(json.dumps(output) + "\n")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
