# Visual Tools Suite (`./visual-tools`)

A standardized tool suite and runbook for creating, editing, rendering, and publishing **Mermaid** diagrams and **SVG** vector graphics.

---

## 📂 Directory Layout

```
visual-tools/
├── SKILL.md                 # Antigravity Skill Definition (YAML frontmatter + instructions)
├── README.md                # Overview & Documentation
├── viz/                     # Default output directory for published PNG diagrams
├── scripts/
│   ├── visual_tool.py       # Core CLI runner (write, edit, render, publish)
│   ├── render_mermaid.py    # Dedicated Mermaid renderer (.mmd -> .png)
│   └── render_svg.py        # Dedicated SVG renderer (.svg -> .png)
├── templates/
│   ├── flowchart.mmd        # Sample Mermaid Flowchart
│   ├── sequence.mmd         # Sample Mermaid Sequence Diagram
│   └── badge.svg            # Sample SVG Vector Graphic
└── references/
    ├── MERMAID_REFERENCE.md  # Quick Mermaid diagram reference
    └── SVG_REFERENCE.md      # SVG coding guidelines & styling reference
```

---

## 🛠 Features

- **Managed Files**: Automatically tracks session source files (`diagram.mmd` and `diagram.svg`).
- **Exact-Match Editing**: Safe string replacement (`old_text` -> `new_text`) with single-occurrence validation.
- **Robust Rendering**: Supports multiple rendering backends (`mmdc`, `rsvg-convert`, `magick`, `cairosvg`, `python-pillow`).
- **Publishing Pipeline**: Automatically copies and names rendered outputs inside `./viz/`.
