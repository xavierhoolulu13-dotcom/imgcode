#!/usr/bin/env python3
"""Validate a Tree IR document. Stdlib only. Returns (ok, errors)."""
import json

KINDS = {"business", "system", "page", "channel", "function", "offer"}


def load_tree(path):
    with open(path) as f:
        return json.load(f)


def validate(tree):
    errors = []
    for key in ("tree_id", "ir_version", "root", "nodes", "meta"):
        if key not in tree:
            errors.append(f"missing top-level key: {key}")
    if errors:
        return False, errors
    if tree["ir_version"] != "0.3":
        errors.append(f"ir_version must be '0.3', got {tree['ir_version']!r}")
    root = tree["root"]
    if root.get("kind") != "business":
        errors.append("root.kind must be 'business'")
    nodes = tree["nodes"]
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
    # cycle check: walk each node's parent chain
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
    return (len(errors) == 0), errors


if __name__ == "__main__":
    import sys
    ok, errors = validate(load_tree(sys.argv[1]))
    print("VALID" if ok else "INVALID")
    for e in errors:
        print(" -", e)
    sys.exit(0 if ok else 1)
