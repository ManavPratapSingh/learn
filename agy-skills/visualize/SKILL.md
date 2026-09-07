---
name: visualize
description: >-
  Add a correct, minimal visual to a lesson — a diagram or geometric picture — that renders inline in the session log or markdown artifact.
  Use when an idea is genuinely clearer as a picture: a dependency graph, system/flow, sequence, state machine, tree, comparison, or a spatial/geometric thing.
---

# Visualize (AGY Adaptation)

A picture earns its place only when it shows something words can't — shape, structure, direction, relationship, geometry. This skill produces ONE such picture, guarantees it is **correct** (the renderer verifies it before returning), and drops it into the lesson so it renders inline in the log or artifact.

You are the **creative director**. You decide the exact idea and distill it to its fewest carrying elements. A **visual-tool runner** or **subagent** does the authoring, rendering, visual verification, and saving, then returns a published file path. You embed that file in your reply.

---

## When to visualize (and when not to)

This teaching system builds a **dependency graph in the learner's head** — axioms at the root, derived facts hanging off them. A visual is powerful exactly when it makes that structure (or a geometry) visible. Reach for one when:

- The idea is a **structure or relationship**: dependencies, a system with parts and arrows, a flow/pipeline, a sequence of exchanges, a state machine, a tree/hierarchy, a comparison, a containment (what's inside vs outside).
- The idea is **spatial or geometric**: coordinate geometry, a number line, vectors, a function's shape, a physical arrangement.

Do NOT visualize when prose or a single equation already carries it. A decorative diagram that just restates the sentence next to it adds noise and a chance to be wrong. When in doubt, don't — a missing visual is cheaper than a false one.

---

## Choose the tool category

Two categories, supported via `./visual-tools/`:

- **Mermaid (`graph TD`, `sequenceDiagram`, etc.)** — structural/relational visuals: dependency graphs, flowcharts, sequence/state/ER/class diagrams, trees, mindmaps, timelines. This is the default and fits the dependency-graph pedagogy directly.
- **SVG (`<svg ...>`)** — spatial/geometric visuals Mermaid can't lay out: exact coordinates, geometry figures, number lines, vectors, plots, custom shapes.

Rule of thumb: if it's *nodes-and-edges / relationships*, use Mermaid. If it's *positions-and-shapes / geometry*, use SVG.

---

## Briefing: one idea, fewest elements

The most common failure is **cramming** — every extra label makes the picture harder to read AND harder to lay out correctly. Before briefing, prune to the fewest elements that carry the idea, and for each ask: *"if I delete this, is the idea still clear?"* If yes, delete it.

Give the subagent or visual runner the concept AND the concrete elements you want — not a vague topic, and not a long checklist.

- BAD: "make a diagram about how TCP works"
- GOOD: "graph TD: a node 'packet' at the top; arrows down to 'ordering' and 'retransmit on loss'; both arrows down into 'reliable stream'. No title. Show that reliability is built FROM packets, not alongside them."

Keep the idea intact. If your brief lists more than ~5–7 elements, cut it first.

---

## Invocation in Antigravity (AGY)

In Antigravity, you can dispatch the task to a subagent using `invoke_subagent`:

```json
{
  "Subagents": [
    {
      "TypeName": "self",
      "Role": "Mermaid Visual Creator",
      "Prompt": "Execute: python3 ./visual-tools/scripts/visual_tool.py write mermaid '...' && python3 ./visual-tools/scripts/visual_tool.py render mermaid --save-as viz-tcp-flow.png"
    }
  ]
}
```

Or execute the visual pipeline directly via terminal commands:

```bash
# 1. Write the source
python3 ./visual-tools/scripts/visual_tool.py write mermaid "graph TD\n  A[Packets] --> B[Ordering]\n  A --> C[Retransmit]\n  B --> D[Reliable Stream]\n  C --> D"

# 2. Render and publish to ./viz/
python3 ./visual-tools/scripts/visual_tool.py render mermaid --save-as viz-tcp-flow.png
```

The tool publishes the PNG image into `./viz/` and returns:

```text
Published visual asset -> /home/manav/learn/viz/viz-tcp-flow.png
```

---

## Embed it in the lesson

Embed the rendered PNG directly in your teaching response or Markdown artifact using GitHub-style image Markdown syntax:

```markdown
![TCP Reliability Flowchart](/home/manav/learn/viz/viz-tcp-flow.png)
```

Introduce the visual in a sentence, then let it carry the idea — don't narrate every element back in prose.

---

## Why this is reliable in AGY

- **Process-isolated rendering**: Visual assets are created and rendered into deterministic PNG files inside `./viz/`.
- **Pixel-identical rendering**: PNG embeds mean what was verified is pixel-identical to what the learner sees in Obsidian or the Antigravity preview.
- **Unique filenames**: Avoids caching conflicts across multiple teaching sessions.
