#!/usr/bin/env python3
"""Validate a Tree IR document. Stdlib only. Returns (ok, errors).

Reconciled with HOOLULU/IMGCODE CANON v1.0 §5. The canon's Tree IR fields
(version, name, purpose, domain, edges, dependencies, inputs, outputs,
approval_points, constraints, metadata; per-node type/purpose/requires/
produces/status/human_approval) are accepted as optional. v0.3 trees that
don't use them remain valid — one language, no breakage.

Alias rule (canon §21 — no competing representations): `type` is the canon
word for `kind`, `purpose` for `note`. If both are present they must agree.
"""
import json

KINDS = {"business", "system", "page", "channel", "function", "offer"}

CANON_TOPLEVEL_OPTIONAL = {
    "version": str, "name": str, "purpose": str, "domain": str,
    "edges": list, "dependencies": list, "inputs": list, "outputs": list,
    "approval_points": list, "constraints": list, "metadata": dict,
}


def load_tree(path):
    with open(path) as f:
        return json.load(f)


def _canon_node(n):
    """Merge canon aliases into the working shape. Returns (node, errors)."""
    errors = []
    n = dict(n)
    if "type" in n:
        if "kind" in n and n["type"] != n["kind"]:
            errors.append(
                f"node {n.get('id')!r}: type {n['type']!r} conflicts with kind {n['kind']!r}")
        n["kind"] = n["type"]
    if "purpose" in n:
        if "note" in n and n["purpose"] != n["note"]:
            errors.append(f"node {n.get('id')!r}: purpose conflicts with note")
        n["note"] = n["purpose"]
    n.setdefault("requires", [])
    n.setdefault("produces", [])
    n.setdefault("status", "planned")
    n.setdefault("human_approval", False)
    return n, errors


def validate(tree):
    errors = []
    for key in ("tree_id", "ir_version", "root", "nodes", "meta"):
        if key not in tree:
            errors.append(f"missing top-level key: {key}")
    if errors:
        return False, errors
    if tree["ir_version"] != "0.3":
        errors.append(f"ir_version must be '0.3', got {tree['ir_version']!r}")
    for key, typ in CANON_TOPLEVEL_OPTIONAL.items():
        if key in tree and not isinstance(tree[key], typ):
            errors.append(f"top-level {key!r} must be {typ.__name__}")
    root = tree["root"]
    if root.get("kind") != "business":
        errors.append("root.kind must be 'business'")
    nodes = []
    for n in tree["nodes"]:
        nn, errs = _canon_node(n)
        errors.extend(errs)
        nodes.append(nn)
    ids = [n.get("id") for n in nodes]
    if len(ids) != len(set(ids)):
        errors.append("duplicate node ids")
    by_id = {n["id"]: n for n in nodes}
    for n in nodes:
        if n.get("kind") not in KINDS:
            errors.append(f"node {n.get('id')!r}: bad kind {n.get('kind')!r}")
        if not n.get("label"):
            errors.append(f"node {n.get('id')!r}: missing label")
        parent = n.get("parent")
        if parent != root["id"] and parent not in by_id:
            errors.append(f"node {n.get('id')!r}: parent {parent!r} does not exist")
        for req in n.get("requires", []):
            if req not in by_id and req != root["id"]:
                errors.append(f"node {n.get('id')!r}: requires unknown node {req!r}")
        if not isinstance(n.get("human_approval"), bool):
            errors.append(f"node {n.get('id')!r}: human_approval must be true/false")
    # cycle check: parent chains
    for n in nodes:
        seen, cur = set(), n
        while cur["parent"] != root["id"]:
            if cur["id"] in seen:
                errors.append(f"cycle detected at {cur['id']!r}")
                break
            seen.add(cur["id"])
            cur = by_id.get(cur["parent"])
            if cur is None:
                break
    # cycle check: requires graph
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {i: WHITE for i in by_id}

    def visit(u, stack):
        color[u] = GRAY
        for v in by_id[u].get("requires", []):
            if v == root["id"] or v not in by_id:
                continue
            if color[v] == GRAY:
                errors.append(f"requires cycle: {' -> '.join(stack + [u, v])}")
            elif color[v] == WHITE:
                visit(v, stack + [u])
        color[u] = BLACK

    for i in by_id:
        if color[i] == WHITE:
            visit(i, [])
    # edges, if present: endpoints must exist
    for e in tree.get("edges", []):
        for end in (e.get("from"), e.get("to")):
            if end != root["id"] and end not in by_id:
                errors.append(f"edge {e!r}: unknown endpoint {end!r}")
    return (len(errors) == 0), errors


def approval_points(tree):
    """Canon §5 approval points: flagged nodes + the standing 808 sales gate."""
    pts = [n["id"] for n in tree["nodes"] if n.get("human_approval")]
    pts.append("sales-package: Xavier approves before any outreach (808 gate)")
    return pts


def canon_view(tree):
    """Project any valid tree into the canon §5 shape.

    Derivation, not a second store: parent links become edges, requires
    become dependencies, human_approval flags become approval_points.
    """
    nodes, edges, deps = [], [], []
    root_id = tree["root"]["id"]
    for n in tree["nodes"]:
        nn, _ = _canon_node(n)
        nodes.append({
            "id": nn["id"],
            "type": nn["kind"],
            "label": nn["label"],
            "purpose": nn.get("note", ""),
            "requires": list(nn.get("requires", [])),
            "produces": list(nn.get("produces", [])),
            "status": nn.get("status", "planned"),
            "human_approval": bool(nn.get("human_approval", False)),
        })
        edges.append({"from": nn["parent"], "to": nn["id"]})
        for r in nn.get("requires", []):
            deps.append([r, nn["id"]])
            edges.append({"from": r, "to": nn["id"], "kind": "requires"})
    for e in tree.get("edges", []):
        if e not in edges:
            edges.append(e)
    return {
        "tree_id": tree["tree_id"],
        "version": tree.get("version", tree["ir_version"]),
        "name": tree.get("name", tree["root"]["label"]),
        "purpose": tree.get("purpose", ""),
        "domain": tree.get("domain", tree["meta"].get("niche", "")),
        "nodes": nodes,
        "edges": edges,
        "dependencies": deps,
        "inputs": tree.get("inputs", []),
        "outputs": tree.get("outputs", []),
        "approval_points": approval_points(tree),
        "constraints": tree.get("constraints", []),
        "metadata": {**tree.get("metadata", {}),
                     "ir_version": tree["ir_version"],
                     "niche": tree["meta"].get("niche", "")},
    }


if __name__ == "__main__":
    import sys
    ok, errors = validate(load_tree(sys.argv[1]))
    print("VALID" if ok else "INVALID")
    for e in errors:
        print(" -", e)
    sys.exit(0 if ok else 1)
