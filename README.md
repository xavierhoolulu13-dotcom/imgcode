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

- **hoolulu-factory-FROZEN-CORE** — the governor. Immutable rules, contracts, the GPT808 spine. Nothing bypasses it. Read-only.
- **imgcode** (this repo) — the visual planning layer. Tap bricks, arrange sequences, compile to buildable specs.
- **xavierhoolulu13-dotcom.github.io** (publishing) — takes compiled specs to production: build, deploy, maintain, monitor. Live at https://xavierhoolulu13-dotcom.github.io

See [LOOP.md](LOOP.md) for how a full cycle runs.

## Ecosystem

IMGCODE is the visual planning layer of a four-project ecosystem:

- **x-it** — https://github.com/xavierhoolulu13-dotcom/x-it — Xavier's own AI product and the brain/OS of the system (chat, sandbox execution, tool calling, local Ollama support).
- **TENTCITY** — https://github.com/xavierhoolulu13-dotcom/tentcity (live: https://xavierhoolulu13-dotcom.github.io/tentcity/) — the public mall front door: $5 entry, tool directory, lead funnels.
- **IMGCODE** — https://github.com/xavierhoolulu13-dotcom/imgcode — "code you tap, not type": visual tap-to-build system that compiles tapped specs into shippable systems.
- **Hoolulu Factory** — https://github.com/xavierhoolulu13-dotcom/hoolulu-factory — the backend engine: agents, autopilot loops, client ops.

## Status

- v0.2 "Dependency-Aware Sequence Compiler" — built, pending publish
- Public beta: https://muse.ai/s/imgcode-xnxm6kakxufdxrt
