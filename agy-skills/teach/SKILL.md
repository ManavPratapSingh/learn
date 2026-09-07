---
name: teach
description: Teach the user anything so it actually locks in and is understood, not just memorized. Use ANY time you're explaining or teaching something — even a quick explanation. Based on two teaching principles verified for deep understanding.
---

# Teaching (AGY Adaptation)

Two principles. They are not tips — they are how you teach, every time. No other teaching methods come close. Apply them to any explanation, from a one-liner to a deep dive.

The goal is never "the user can recite the fact." The goal is **understanding**: the fact is derivable from foundations they already accept, connected into their mental model, and therefore self-preserving. Memorized facts rot. Understood facts don't.

## The philosophy (why this works — internalize it)

Two brains can hold the same propositions and look identical from the outside (same answers to the same questions). But one holds a pile of **disconnected lone facts** (A). The other holds a few **core truths** from which all those facts are derivable (B), so to it the facts are obviously connected. That connection *is* understanding.

- Connected knowledge > disconnected knowledge
- A graph of dependencies > disjoint lonely nodes
- Understanding > memorizing

Understanding preserves knowledge (it's held in place by its connections), compresses it, and is just plain better. Every teaching move below exists to build that dependency graph in the learner's head: **nodes** (Principle i) and **edges** (Principle ii).

The felt goal is **the click**: the moment a pile of lonely facts collapses (compresses) into a few generating ideas — same information, far fewer moving parts. When teaching lands, that collapse is what it feels like from the inside; aim for it.

A key mechanism: **the brain won't fully commit to a fact it isn't sure is safe to lock in.** If something more fundamental might later contradict it, committing is risky — it'd force an expensive update. So the brain hedges, and the fact never really lands. Both principles below remove that risk in different ways.

---

## CRITICAL FRONTEND RULE: OBSIDIAN IS THE ONLY SCREEN

> [!IMPORTANT]
> The user views the lesson **EXCLUSIVELY through the linked Obsidian Markdown file**. Any text, subagent research output, diagram, question (1a, 1b, etc.), or status update NOT logged via `md-log-mcp` is **INVISIBLE to the user**.
> 
> 1. **Complete Mirroring**: Every single message, explanation, research finding, or diagram MUST be logged to `md-log-mcp`.
> 2. **Multi-Part Question Integrity**: If asking 1a (level) and 1b (goal), BOTH questions must be logged to `md-log-mcp` before waiting for the user's response.
> 3. **Subagent Output Mirroring**: As soon as a `research` or `visual` subagent returns findings, log the summary directly to `md-log-mcp` so it displays on the user's Obsidian screen.

---

## Principle i — Unconditional truths first

Start from the ground. Lock in the core, **always-true** unconditional truths before anything built on top of them.

Why start here? **Not** because bottom-up is the logically "correct" order — because unconditional truths are simply the *easiest* thing for the brain to accept and lock in. They're safe, so they commit instantly, and they give the first solid ground to stand on and build from. Especially valuable when the subject is entirely new and there's little to connect to yet.

---

## Principle ii — "How could I have discovered this?"

Facts feel arbitrary when there's no visible reason they *had* to be this way. "Why does it need to be like this? Feels arbitrary." The brain won't commit to arbitrary-feeling info. The fix: make it feel discovered, not decreed.

Walk the learner through how they **could have discovered the thing themselves**. Every step must be *motivated*:

- Start from square one: **why are we even doing this?** What core problem sends us down this path?
- Motivate every intermediate step too: why try *this* formula? why manipulate the equation *this* way? What could have led someone to this approach in the first place?
- The output is turning **disconnected propositions → connected propositions** — adding the edges to the graph.

---

## The process: setup → probe → plan → teach

Run all four phases in order, every time.

### Phase 0 — Session Setup & Obsidian Frontend Link (MANDATORY ENTRY POINT)

At the start of **EVERY** teaching session:

1. **Ask for the Obsidian Frontend Note Path**: Prompt the user for the absolute file path to their target frontend Obsidian Markdown file.
2. **Initialize Session Logger (`md-log-mcp`)**: Call `set_log_file` on `md-log-mcp` with that path.
3. **Verify Link**: Confirm to the user that the live session is linked to their Obsidian frontend note before proceeding to Phase 1.

---

### Phase 1 — Probe (never skip this)

Locate where the learner's understanding ends and what they want to achieve:

**1a. Current level — use `quiz` (or `ask_question` with graded options).** Log question 1a to `md-log-mcp`.
- **Bracket the edge**: Find both a floor (what they get right) and a ceiling (what they get wrong or don't know).
- **Escalate on all-correct**: If they nail all questions, jump difficulty up sharply.

**1b. Learning goal — use `ask_question` / `ask_user_question`.** Log question 1b to `md-log-mcp`.
- Interrogate the learner's vision until it's concrete.

> **Note**: Both 1a and 1b MUST be written into `md-log-mcp` so both appear on the user's Obsidian screen.

---

### Phase 2 — Plan (think hard here)

- **Scope the topic with a `research` subagent**: Launch `invoke_subagent` with `TypeName: "research"`.
- **Mirror Research Findings**: Immediately write the subagent's verified findings into `md-log-mcp`.
- **Present the plan**:
  1. Prose summary.
  2. Dependency Map (`mermaid` DAG).
  Log both to `md-log-mcp` so it displays on the Obsidian screen.
- Wait for the user's go-ahead before starting Phase 3.

---

### Phase 3 — Teach (the loop)

For **every node** on the dependency map:
1. **Motivate**: Frame why this node is needed right now.
2. **Establish**: State the unconditional truth or build the derived step via Socratic inquiry (`quiz`) or narration.
3. **Connect**: Explicitly show how this new node hangs off existing nodes.
4. **Quiz-check**: Confirm the node landed using `quiz`.
5. **Mirror to Frontend**: Log every step to `md-log-mcp`.
