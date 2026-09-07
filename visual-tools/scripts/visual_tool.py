#!/usr/bin/env python3
import sys
import os
import shutil
import argparse
from render_svg import render_svg
from render_mermaid import render_mermaid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIZ_DIR = os.path.join(os.path.dirname(BASE_DIR), "viz")

MERMAID_FILE = os.path.join(BASE_DIR, "diagram.mmd")
SVG_FILE = os.path.join(BASE_DIR, "diagram.svg")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def write_file(target_path, content):
    ensure_dir(os.path.dirname(target_path))
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    lines = len(content.strip().split("\n"))
    print(f"Wrote {lines} lines to {target_path}")

def edit_file(target_path, old_text, new_text):
    if not os.path.exists(target_path):
        print(f"Error: Target file {target_path} does not exist. Write source first.", file=sys.stderr)
        sys.exit(1)

    with open(target_path, "r", encoding="utf-8") as f:
        content = f.read()

    count = content.count(old_text)
    if count == 0:
        print(f"Error: `old_text` not found in {target_path}", file=sys.stderr)
        sys.exit(1)
    elif count > 1:
        print(f"Error: `old_text` matched {count} times in {target_path}. Must match exactly once.", file=sys.stderr)
        sys.exit(1)

    updated = content.replace(old_text, new_text)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(updated)
    print(f"Successfully edited {target_path}")

def render_and_publish(source_type, save_as=None):
    ensure_dir(VIZ_DIR)
    
    if source_type == "mermaid":
        src = MERMAID_FILE
        filename = save_as or "mermaid_diagram.png"
        out_png = os.path.join(VIZ_DIR, filename)
        ok = render_mermaid(src, out_png)
    elif source_type == "svg":
        src = SVG_FILE
        filename = save_as or "svg_graphic.png"
        out_png = os.path.join(VIZ_DIR, filename)
        ok = render_svg(src, out_png)
    else:
        print(f"Unknown source type: {source_type}", file=sys.stderr)
        sys.exit(1)

    if ok and os.path.exists(out_png):
        print(f"Published visual asset -> {out_png}")
    else:
        print(f"Notice: Source file saved at {src}. (PNG rasterizer skipped/unavailable)")

def main():
    parser = argparse.ArgumentParser(description="Visual Tools CLI for Mermaid and SVG authoring loop.")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # Write command
    write_parser = subparsers.add_parser("write", help="Write source code")
    write_parser.add_argument("type", choices=["mermaid", "svg"])
    write_parser.add_argument("source", help="Source code string")

    # Edit command
    edit_parser = subparsers.add_parser("edit", help="Edit source code (exact match replacement)")
    edit_parser.add_argument("type", choices=["mermaid", "svg"])
    edit_parser.add_argument("old_text", help="Exact string to replace")
    edit_parser.add_argument("new_text", help="Replacement string")

    # Render command
    render_parser = subparsers.add_parser("render", help="Render source to PNG")
    render_parser.add_argument("type", choices=["mermaid", "svg"])
    render_parser.add_argument("--save-as", help="Filename to publish inside ./viz/")

    args = parser.parse_args()

    if args.action == "write":
        target = MERMAID_FILE if args.type == "mermaid" else SVG_FILE
        write_file(target, args.source)
    elif args.action == "edit":
        target = MERMAID_FILE if args.type == "mermaid" else SVG_FILE
        edit_file(target, args.old_text, args.new_text)
    elif args.action == "render":
        render_and_publish(args.type, args.save_as)

if __name__ == "__main__":
    main()
