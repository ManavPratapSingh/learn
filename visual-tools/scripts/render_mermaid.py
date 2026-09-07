#!/usr/bin/env python3
import sys
import os
import subprocess

def render_mermaid(mmd_path: str, out_png_path: str) -> bool:
    mmd_path = os.path.abspath(mmd_path)
    out_png_path = os.path.abspath(out_png_path)
    out_dir = os.path.dirname(out_png_path)

    if not os.path.exists(mmd_path):
        print(f"Error: Mermaid file not found: {mmd_path}", file=sys.stderr)
        return False

    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # 1. Try mmdc CLI
    try:
        res = subprocess.run(["mmdc", "-i", mmd_path, "-o", out_png_path, "-b", "transparent"], capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(out_png_path):
            print(f"Rendered Mermaid via mmdc -> {out_png_path}")
            return True
    except FileNotFoundError:
        pass

    # 2. Try npx @mermaid-js/mermaid-cli
    try:
        res = subprocess.run(["npx", "-p", "@mermaid-js/mermaid-cli", "mmdc", "-i", mmd_path, "-o", out_png_path, "-b", "transparent"], capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(out_png_path):
            print(f"Rendered Mermaid via npx mmdc -> {out_png_path}")
            return True
    except FileNotFoundError:
        pass

    print("Warning: mmdc or npx @mermaid-js/mermaid-cli not available.", file=sys.stderr)
    return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 render_mermaid.py <input.mmd> <output.png>")
        sys.exit(1)
    ok = render_mermaid(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)
