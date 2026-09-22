# IMGCODE

**Code you tap, not type.** The visual architecture layer that sits *before* AI builders.

```text
Human idea
    ↓
IMGCODE — visual architecture (tap bricks, arrange sequence)
    ↓
Generated system specification
    ↓
AI / build team
    ↓
Tests / approval
    ↓
Deployment
```

## The three-repo loop

IMGCODE is the middle of a full-cycle loop:

```text
FROZEN CORE  →  IMGCODE  →  PUBLISHING
 (governor)      (plan)       (build / deploy / maintain)
     ↑                                        │
     └────────────── feedback ────────────────┘
```

- **hoolulu-factory-FROZEN-CORE** — the governor. Immutable rules, contracts, the GPT808 spine. Nothing bypasses it.
- **imgcode** (this repo) — the visual planning layer. Tap bricks, arrange sequences, compile to buildable specs.
- **publishing** — takes compiled specs to production: build, deploy, maintain, monitor.

How the loop runs:

1. **Govern** — every sequence is validated against the pinned Frozen Core contract before anything builds.
2. **Plan** — IMGCODE compiles tap-arranged bricks into a system spec + build checklist + handoff pack.
3. **Publish** — the handoff pack lands in the publishing repo; Actions build and deploy it.
4. **Feedback** — deploy health and monitor signals loop back; the governor re-validates, IMGCODE iterates.

## Status

- v0.2 "Dependency-Aware Sequence Compiler" — building
- Public beta: https://muse.ai/s/imgcode-xnxm6kakxufdxrt
