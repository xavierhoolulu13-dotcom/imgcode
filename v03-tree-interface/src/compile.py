#!/usr/bin/env python3
"""Governor checks on a composed tree + deterministic build spec emitter.
Stdlib only. Checks: missing dependencies, odd ordering, approval gates,
release risks. Fail-closed: flags block the Factory handoff until cleared.
"""
import json
from datetime import date

BOOKING_WORDS = ("reserv", "booking", "order", "pay", "checkout")
BUILD_WORDS = ("website", "build", "audit", "setup")
MAINTAIN_WORDS = ("maintain", "monitor", "care")


def _children(tree, node_id):
    return [n for n in tree["nodes"] if n["parent"] == node_id]


def _labels(tree):
    return " ".join(n["label"].lower() for n in tree["nodes"])


def check_missing_dependencies(tree):
    flags = []
    by_id = {n["id"]: n for n in tree["nodes"]}
    root_id = tree["root"]["id"]
    for n in tree["nodes"]:
        # pages must descend from a system
        if n["kind"] == "page":
            anc, cur = False, n
            while cur["parent"] != root_id:
                cur = by_id.get(cur["parent"])
                if cur is None:
                    break
                if cur["kind"] == "system":
                    anc = True
                    break
            if not anc:
                flags.append(f"page {n['id']!r} has no system ancestor")
        # booking/payment functions need a contact or payment node somewhere
        lab = n["label"].lower()
        if n["kind"] == "function" and any(w in lab for w in BOOKING_WORDS):
            blob = _labels(tree)
            if "contact" not in blob and "payment" not in blob:
                flags.append(f"function {n['id']!r} looks transactional but no contact/payment node exists")
    if not any(n["kind"] == "offer" for n in tree["nodes"]):
        flags.append("no 'offer' node: MARKET MATCH stage will stall (nothing to sell)")
    return flags


def check_ordering(tree):
    flags = []
    root_id = tree["root"]["id"]
    top = [n for n in tree["nodes"] if n["parent"] == root_id]
    top.sort(key=lambda n: n.get("order", 0))
    labels = [n["label"].lower() for n in top]
    first_maintain = next((i for i, l in enumerate(labels)
                           if any(w in l for w in MAINTAIN_WORDS)), None)
    first_build = next((i for i, l in enumerate(labels)
                        if any(w in l for w in BUILD_WORDS)), None)
    if first_maintain is not None and first_build is not None \
            and first_maintain < first_build:
        flags.append("odd ordering: maintenance/monitoring is sequenced before build/audit work")
    return flags


def approval_gates(tree):
    return [
        "Xavier taps 'done' on the composed tree (this already happened to reach compile)",
        "Governor checks above must show zero blocking flags before Factory handoff",
        "Xavier approves the sales package before any outreach (808 gate)",
        "Xavier approves pricing, contracts, and payments (standing rule)",
    ]


def check_risks(tree):
    risks = []
    count = len(tree["nodes"])
    if count > 20:
        risks.append(f"scope: {count} nodes is a big first build — consider pruning")
    depth = 0
    by_id = {n["id"]: n for n in tree["nodes"]}
    root_id = tree["root"]["id"]
    for n in tree["nodes"]:
        d, cur = 0, n
        while cur["parent"] != root_id:
            d += 1
            cur = by_id.get(cur["parent"])
            if cur is None:
                break
        depth = max(depth, d)
    if depth > 4:
        risks.append(f"nesting depth {depth}: deep trees are harder to sell simply")
    if "contact" not in _labels(tree):
        risks.append("no contact path in tree: customers can't reach the business")
    return risks


def compile_tree(tree):
    dep_flags = check_missing_dependencies(tree)
    order_flags = check_ordering(tree)
    risks = check_risks(tree)
    blocking = dep_flags + order_flags
    spec = {
        "spec_id": f"{tree['tree_id']}-spec",
        "ir_version": "0.3",
        "compiled": str(date.today()),
        "node_count": len(tree["nodes"]),
        "governor": {
            "missing_dependencies": dep_flags,
            "ordering": order_flags,
            "risks": risks,
            "blocking_flags": len(blocking),
            "verdict": "GO" if not blocking else "BLOCKED — clear flags first",
        },
        "approval_gates": approval_gates(tree),
        "factory_handoff": {
            "status": "ready" if not blocking else "held",
            "note": "Hand the composed tree + this spec to the Hoolulu Factory.",
        },
    }
    return spec


def handoff_markdown(tree, spec):
    g = spec["governor"]
    lines = [
        f"# Build handoff — {tree['tree_id']}",
        f"Compiled {spec['compiled']} · {spec['node_count']} nodes · verdict: **{g['verdict']}**",
        "",
        "## Governor checks",
        f"- Missing dependencies: {len(g['missing_dependencies'])}",
        f"- Ordering: {len(g['ordering'])}",
        f"- Risks: {len(g['risks'])}",
        "",
    ]
    for f in g["missing_dependencies"] + g["ordering"]:
        lines.append(f"- BLOCKING: {f}")
    for r in g["risks"]:
        lines.append(f"- RISK: {r}")
    lines += ["", "## Approval gates"]
    for gate in spec["approval_gates"]:
        lines.append(f"- [ ] {gate}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    import sys
    from validate import load_tree
    tree = load_tree(sys.argv[1])
    spec = compile_tree(tree)
    print(json.dumps(spec, indent=2))
