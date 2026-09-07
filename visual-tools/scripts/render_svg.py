#!/usr/bin/env python3
import sys
import os
import subprocess

def render_svg(svg_path: str, out_png_path: str) -> bool:
    svg_path = os.path.abspath(svg_path)
    out_png_path = os.path.abspath(out_png_path)
    out_dir = os.path.dirname(out_png_path)

    if not os.path.exists(svg_path):
        print(f"Error: SVG file not found: {svg_path}", file=sys.stderr)
        return False

    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # 1. Try rsvg-convert (librsvg)
    try:
        res = subprocess.run(["rsvg-convert", "-z", "2", svg_path, "-o", out_png_path], capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(out_png_path):
            print(f"Rendered SVG via rsvg-convert -> {out_png_path}")
            return True
    except FileNotFoundError:
        pass

    # 2. Try ImageMagick (magick or convert)
    for cmd in ["magick", "convert"]:
        try:
            res = subprocess.run([cmd, "-density", "192", "-background", "none", svg_path, out_png_path], capture_output=True, text=True)
            if res.returncode == 0 and os.path.exists(out_png_path):
                print(f"Rendered SVG via {cmd} -> {out_png_path}")
                return True
        except FileNotFoundError:
            pass

    # 3. Try cairosvg (python module/cli)
    try:
        res = subprocess.run(["cairosvg", svg_path, "-o", out_png_path], capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(out_png_path):
            print(f"Rendered SVG via cairosvg -> {out_png_path}")
            return True
    except FileNotFoundError:
        pass

    # 4. Try Inkscape
    try:
        res = subprocess.run(["inkscape", svg_path, "--export-type=png", f"--export-filename={out_png_path}"], capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(out_png_path):
            print(f"Rendered SVG via Inkscape -> {out_png_path}")
            return True
    except FileNotFoundError:
        pass

    print("Warning: No native SVG rasterizer (rsvg-convert, magick, cairosvg, inkscape) found.", file=sys.stderr)
    return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 render_svg.py <input.svg> <output.png>")
        sys.exit(1)
    ok = render_svg(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)
