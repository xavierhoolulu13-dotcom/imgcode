# The Loop

Three repos, one full cycle. Order matters.

```text
FROZEN CORE  →  IMGCODE  →  PUBLISHING
 (governor)      (plan)       (build / deploy / maintain)
     ↑                                        │
     └────────────── feedback ────────────────┘
```

## The three repos

1. **hoolulu-factory-FROZEN-CORE** — the governor. Immutable rules, contracts, the GPT808 spine. **Read-only:** nothing writes here except Xavier. Every stage below validates against the pinned core contract.
2. **imgcode** (this repo) — the visual planning layer. Tap bricks, arrange sequences, compile to buildable specs. Outputs: architecture spec, build checklist, handoff pack, Markdown export.
3. **xavierhoolulu13-dotcom.github.io** — publishing. Compiled specs land here; Pages serves them. Build, deploy, maintain, monitor.

## How a cycle runs

1. **Govern** — IMGCODE validates the sequence against the Frozen Core contract before anything builds. Missing dependencies, bad ordering, and approval gates get flagged here, not in production.
2. **Plan** — the compiler produces the handoff pack: what to build, in what order, with what gates.
3. **Publish** — the handoff pack is pushed to the publishing repo (manual today, automated in v0.3). Pages deploys it.
4. **Feedback** — deploy health and monitor signals loop back. The governor re-validates; IMGCODE iterates the plan. The cycle repeats.

## What's manual today / what's next

- Today: the handoff pack moves by hand (export from IMGCODE, push to the publishing repo).
- v0.3: the compiler pushes directly to the publishing repo; Actions build and deploy; monitor signals feed back automatically.
- The frozen-core repo stays read-only through all of it. The governor doesn't get edited by the loop it governs.
