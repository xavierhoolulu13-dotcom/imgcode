# IMGCODE v0.3 — Tree Interface

**Status:** WORKING CODE. The full loop, wired end to end, testable right now.

```text
TREE IN → VALIDATE → COMPOSE (your taps) → COMPILE (governor) → FACTORY → MARKET MATCH → SALES PACKAGE
```

## What's real vs what's a stand-in

| Stage | Status |
|---|---|
| Tree IR schema + validator | REAL |
| Compose (prune / reorder / annotate) | REAL |
| Compiler governor checks (missing deps, ordering, risks) | REAL |
| Build spec + handoff pack emitter | REAL |
| Factory execution | STUB — accepts the spec, real build runs in the Hoolulu Factory |
| Market match | STUB — shape is real, real matching runs in GPT808 DISCOVER |
| Human approval gates | REAL — fail-closed, nothing passes without Xavier |

Stubs are labeled `[STUB]` in the output. No pretending.

## Test it

```bash
python3 run_loop.py
```

That runs the whole monster on the visibility-audit tree: validate →
your scripted taps → governor checks → spec → factory stub → market-match
stub → sales package awaiting your approval.

Sample trees in `tree-ir/`:
- `visibility-audit-tree.json` — the first product (closest to cash)
- `restaurant-os-tree.json` — second niche sample

## The contract

`tree-ir/schema.json` is the law. Any tree producer (Grok's generator,
hand-built, future importers) emits this shape; every stage reads only this
shape. See `V03_SPEC.md` for the full evolution spec.

## One job per system

Tree Generator → what exists · IMGCODE → how it connects ·
Compiler → build spec · Factory → build it · GPT808 → who needs it ·
Xavier → approves. That's the whole monster. Nothing duplicated.
