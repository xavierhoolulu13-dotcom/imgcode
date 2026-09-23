#!/usr/bin/env python3
"""IMGCODE v0.3 — full loop test run. Stdlib only.

Walks the whole monster on a sample tree so Xavier can SEE the process:
  TREE IN -> VALIDATE -> COMPOSE (scripted taps) -> COMPILE (governor)
  -> FACTORY [STUB] -> MARKET MATCH [STUB] -> SALES PACKAGE (awaits Xavier)

Usage: python3 run_loop.py [tree] [business-profile.json]
"""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from validate import load_tree, validate
from compose import apply_ops
from compile import compile_tree, handoff_markdown
from market_match import match_business, SAMPLE_BUSINESS

BAR = "=" * 55


def stage(n, total, name):
    print(f"\n[{n}/{total}] {name}")
    print("-" * 55)


def main():
    tree_path = sys.argv[1] if len(sys.argv) > 1 else "tree-ir/visibility-audit-tree.json"
    business = SAMPLE_BUSINESS
    real_profile = False
    if len(sys.argv) > 2:
        with open(sys.argv[2]) as f:
            business = json.load(f)
        real_profile = True
    print(BAR)
    print(" IMGCODE v0.3 — FULL LOOP TEST RUN")
    print(BAR)

    # 1. TREE IN + VALIDATE
    stage(1, 6, "TREE IN — validate the IR")
    tree = load_tree(tree_path)
    ok, errors = validate(tree)
    if not ok:
        print("INVALID TREE — loop halted:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"  valid: {tree['tree_id']} ({len(tree['nodes'])} nodes, "
          f"niche={tree['meta']['niche']})")

    # 2. COMPOSE — Xavier's taps (scripted for the demo run)
    stage(2, 6, "COMPOSE — Xavier's taps")
    taps = [
        {"op": "prune", "id": "proof.testimonials"},
        {"op": "annotate", "id": "audit.ai-answers",
         "note": "Lead with this — it's the hook nobody else sells"},
    ]
    composed, log = apply_ops(tree, taps)
    for entry in log:
        print("  tap:", entry)
    print(f"  composed tree: {len(composed['nodes'])} nodes")

    # 3. COMPILE — governor checks
    stage(3, 6, "COMPILE — governor checks")
    spec = compile_tree(composed)
    g = spec["governor"]
    print(f"  missing dependencies: {len(g['missing_dependencies'])}")
    print(f"  ordering flags:       {len(g['ordering'])}")
    print(f"  risks:                {len(g['risks'])}")
    for f in g["missing_dependencies"] + g["ordering"]:
        print("  BLOCKING:", f)
    for r in g["risks"]:
        print("  RISK:", r)
    print(f"  verdict: {g['verdict']}")
    print(f"  approval points ({len(g['approval_points'])}):")
    for a in g["approval_points"]:
        print("   -", a)
    eo = g["execution_order"]
    if eo["error"]:
        print("  ORDER ERROR:", eo["error"])
    else:
        print(f"  execution levels: {len(eo['levels'])} (each level can run in parallel)")
        for i, lvl in enumerate(eo["levels"], 1):
            print(f"   L{i}: {', '.join(lvl)}")
    if g["blocking_flags"]:
        print("  loop HELD — clear flags, then re-run. (This is the governor doing its job.)")
        sys.exit(2)

    with open("build-spec.json", "w") as f:
        json.dump(spec, f, indent=2)
    with open("HANDOFF.md", "w") as f:
        f.write(handoff_markdown(composed, spec))
    print("  wrote build-spec.json + HANDOFF.md")

    # 4. FACTORY [STUB]
    stage(4, 6, "FACTORY — [STUB]")
    print("  build spec accepted. Real execution happens in the Hoolulu Factory.")
    print("  package: queued (demo)")

    # 5. MARKET MATCH [STUB rules, real data when a profile is given]
    stage(5, 6, "MARKET MATCH — [STUB]")
    package = match_business(composed, business)
    if real_profile:
        package["status"] = ("REAL business profile — observed data, checked "
                             "2026-09-23; stub rules — real matching runs in GPT808 DISCOVER")
    print(f"  business: {package['business']}")
    print(f"  gaps found: {len(package['gaps_found'])}")
    for gap in package["gaps_found"]:
        print("   -", gap)
    print("  proposed offer:", "; ".join(package["proposed_offer"]))

    # 6. SALES PACKAGE — human gate
    stage(6, 6, "SALES PACKAGE — awaiting Xavier")
    print("  " + package["human_approval"])
    print(f"  verdict: {package['verdict']}")
    with open("sales-package.json", "w") as f:
        json.dump(package, f, indent=2)
    print("  wrote sales-package.json")

    print("\n" + BAR)
    print(" LOOP COMPLETE (demo). Stubs: Factory execution, GPT808 DISCOVER.")
    print(" Nothing was sent, built, or charged. Xavier approves next moves.")
    print(BAR)


if __name__ == "__main__":
    main()
