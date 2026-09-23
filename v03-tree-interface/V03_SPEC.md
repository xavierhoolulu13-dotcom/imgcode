# IMGCODE v0.3 — "Tree Interface" Evolution Spec

**Date:** 2026-09-22
**Status:** SPEC — not built. Awaiting Xavier's tap before any build.
**Replaces:** earlier v0.3 definition ("auto-publish compiler → repo → Actions").
That automation is parked, not dead — it becomes a deployment detail inside the
Factory stage once the tree loop is proven.

## The call

v0.3 = IMGCODE learns to read **trees**. One job per system, no mega-monster,
no duplicate pipelines. Everything still runs through the Frozen Core governor
and the GPT808 Sales Factory.

```
GROK'S TREE GENERATOR          IMGCODE v0.3              FACTORY            GPT808 SALES
  (external, finishing)    ┌──────────────────┐      ┌──────────────┐    ┌────────────────┐
   "What exists?" ──tree──▶│  "How does it     │─spec─▶│  "BUILD IT"  │    │ "WHO NEEDS IT" │
                           │   connect?"       │      └──────────────┘    └───────┬────────┘
                           │  tap-compose      │                                 │
                           └──────────────────┘                          SALES PACKAGE
                                    ▲                                           │
                                    │                                    HUMAN APPROVAL
                              Xavier taps/prunes                               │
                              reorders, approves                                ▼
                                                                           CUSTOMER → REVENUE
```

## Canonical Tree IR (the common language)

The tree is the intermediate representation between every stage.
Any producer (Grok's generator, hand-built, future importers) emits this shape.
Any consumer (IMGCODE, compiler, Factory) reads only this shape.

```json
{
  "tree_id": "restaurant-os-001",
  "ir_version": "0.3",
  "root": { "id": "root", "label": "Restaurant", "kind": "business" },
  "nodes": [
    { "id": "website",        "parent": "root",       "label": "Website",               "kind": "system"  },
    { "id": "website.home",   "parent": "website",    "label": "Home",                  "kind": "page"    },
    { "id": "website.menu",   "parent": "website",    "label": "Menu",                  "kind": "page"    },
    { "id": "acquire",        "parent": "root",       "label": "Customer Acquisition",  "kind": "system"  },
    { "id": "acquire.google", "parent": "acquire",    "label": "Google presence",       "kind": "channel" },
    { "id": "acquire.reviews","parent": "acquire",    "label": "Reviews",               "kind": "channel" },
    { "id": "ops",            "parent": "root",       "label": "Operations",            "kind": "system"  },
    { "id": "ops.reserve",    "parent": "ops",         "label": "Reservations",         "kind": "function"},
    { "id": "maintain",       "parent": "root",       "label": "Maintenance",           "kind": "system"  },
    { "id": "maintain.vis",   "parent": "maintain",   "label": "Visibility monitoring", "kind": "function"}
  ],
  "meta": {
    "source": "grok-tree-generator | hand-built | importer",
    "niche": "restaurant",
    "created": "2026-09-22"
  }
}
```

Rules:
- `kind` is a closed set: `business | system | page | channel | function | offer`.
- Every node has exactly one parent (a true tree, no DAGs in v0.3).
- IMGCODE never invents nodes; it composes, prunes, reorders, and annotates.

## IMGCODE v0.3 — one job: compose the structure

Input: a Tree IR document (file upload / paste / future generator hook).
Xavier's UX (unchanged System Builder pattern):
1. Tree loads as tappable bricks, nested by parent.
2. He taps to keep/prune, reorders by drag, taps a node to attach notes
   ("this page needs online ordering").
3. He says "done."

Then the v0.2 compiler core runs on the composed tree:
- Missing-dependency detection now walks the tree (e.g. Reservations node
  with no Contact/System parent → flag).
- Impossible ordering, approval gates, release risks — same governor checks,
  tree-aware.
- Output: deterministic build spec + architecture + checklist + handoff pack
  (v0.2 outputs, unchanged shape) → handed to the Factory.

What v0.3 does **not** change: the compiler's fail-closed approval gate, the
Frozen Core contract, the System Builder tap flow.

## Factory handoff (unchanged, existing pipe)

Build spec → Hoolulu Factory executes its normal pipeline
(understand → plan → generate → validate → package, per Frozen Core limits).
No new execution path. No parallel factory.

## GPT808 Sales handoff — the "who needs it" half (defined, not rebuilt)

The product tree's `niche` + `offer` nodes become a MARKET_MATCH request
into the **existing** GPT808 DISCOVER stage:

```
MARKET_MATCH { product_tree_id, niche, offer_summary, geo }
        │
        ▼
GPT808 DISCOVER → finds businesses with gaps matching the tree
        │
        ▼
SALES PACKAGE { business, gaps_found, product_fit, proposed_offer }
        │
        ▼
HUMAN APPROVAL (Xavier — fail-closed, unchanged gate)
        │
        ▼
OUTREACH (existing pipeline only)
```

Nothing here duplicates the sales factory. The tree just gives DISCOVER
something specific to hunt for, instead of a generic audit.

## Capability marketplace (future, not v0.3)

MetaGPT and friends stay **capability sources**, not merged systems.
v0.3 only reserves the contract: a tree node may carry
`"needs_capability": "code-generation"` and the Factory resolves it from a
registry later. No registry is built in v0.3.

## Approval gates (fail-closed, per Frozen Core)

1. Tree schema validation before IMGCODE accepts it.
2. Xavier's "done" before compile.
3. Governor checks before Factory build.
4. Xavier's approval on every sales package before outreach.
5. Xavier's approval on pricing/contracts/payments (unchanged standing rule).

## Non-goals (explicitly out)

- No SUPER_AI_FACTORY mega-agent. One job per system (table in §1).
- No duplicate sales pipeline — GPT808 stays the only one.
- No touching Grok's tree generator build. It finishes on its own; v0.3
  builds the receiving dock (this spec + the IR), not the ship.
- No Roku-channel-store build. Still parked until Xavier says go.
- No auto-publish loop yet (old v0.3). Parked as a Factory deployment detail.

## Open inputs (parked on others)

1. Grok's tree generator: actual output/code, so the IR can be conformance-tested.
2. Xavier: pick the FIRST tree to run the full loop (recommendation below).

## Revenue proof — first loop

Don't boil the ocean. First full Find → Build → Sell loop runs on **one**
product in **one** niche. Recommendation: the AI-visibility audit
(closest to cash, already positioned) as the first tree:

```
Business (Honolulu SMB)
├── Visibility audit (AI answers vs competitors)
├── Gap fix list
├── Offer ($X audit → $Y/mo monitoring)
└── Proof (before/after)
```

Alternative: Restaurant OS. Xavier picks. One loop, real customer, real
revenue — then we talk about the other seven niches.
