---
name: visual-tools
description: >-
  Standardized runbook and tool suite for authoring, editing, rendering, and publishing
  Mermaid architecture diagrams and SVG vector graphics into PNG images. Use this skill when
  the user asks for architecture diagrams, sequence diagrams, flowcharts, or visual vector graphics.
---

# Visual Tools Skill (`visual-tools`)

The **Visual Tools** suite replicates the authoring loop for **Mermaid** diagrams and **SVG** vector graphics. It enables progressive design, exact string editing, rendering to high-res PNG, and publishing output artifacts into `./viz/`.

---

## 📐 Supported Workflows

### 1. Mermaid Diagrams (`.mmd`)
- **Authoring**: Write full Mermaid source (`graph TD`, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`, `classDiagram`, `architecture`).
- **Editing**: Make targeted exact-match string replacements (`old_text` -> `new_text`).
- **Rendering**: Render source to crisp PNG images via `visual_tool.py` or CLI renderers.

### 2. SVG Vector Graphics (`.svg`)
- **Authoring**: Write standalone SVG documents (`<svg ...> ... </svg>`).
- **Editing**: Make targeted string edits to XML elements, styling, colors, or coordinates.
- **Rendering**: Render vector graphics to PNG via `rsvg-convert`, `magick`, or `visual_tool.py`.

---

## 🚀 Quick Execution Commands

All visual tool operations are executed via standard terminal commands:

### Mermaid Workflow
```bash
# 1. Write or update Mermaid source
python3 ./visual-tools/scripts/visual_tool.py write mermaid "graph TD\n  A[Client] --> B[API Server]\n  B --> C[(Database)]"

# 2. Edit existing Mermaid source
python3 ./visual-tools/scripts/visual_tool.py edit mermaid "B[API Server]" "B[API Gateway / Server]"

# 3. Render and publish PNG
python3 ./visual-tools/scripts/visual_tool.py render mermaid --save-as architecture.png
```

### SVG Workflow
```bash
# 1. Write SVG source document
python3 ./visual-tools/scripts/visual_tool.py write svg '<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#1e1e2e"/><text x="50%" y="50%" fill="#cba6f7" font-family="sans-serif" font-size="24" text-anchor="middle" dominant-baseline="middle">Antigravity Visual Tools</text></svg>'

# 2. Edit SVG source
python3 ./visual-tools/scripts/visual_tool.py edit svg '#cba6f7' '#89b4fa'

# 3. Render and publish PNG
python3 ./visual-tools/scripts/visual_tool.py render svg --save-as badge.png
```

---

## 📂 Output & Assets

Published image artifacts are automatically saved into `./viz/`:
- `viz/architecture.png`
- `viz/badge.png`

For templates and syntax guides, refer to:
- [Mermaid Syntax Reference](./references/MERMAID_REFERENCE.md)
- [SVG Syntax & Styling Reference](./references/SVG_REFERENCE.md)
