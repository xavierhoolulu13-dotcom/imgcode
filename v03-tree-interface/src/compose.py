#!/usr/bin/env python3
"""Tap-compose: apply Xavier's ops (prune / reorder / annotate) to a tree.
Stdlib only. Ops look like:
  {"op": "prune", "id": "proof.testimonials"}
  {"op": "annotate", "id": "audit.ai-answers", "note": "..."}
  {"op": "move", "id": "offer", "position": 0}   # reorder among siblings
"""
import copy


def descendants(tree, node_id):
    kids = [n["id"] for n in tree["nodes"] if n["parent"] == node_id]
    out = list(kids)
    for k in kids:
        out += descendants(tree, k)
    return out


def apply_ops(tree, ops):
    tree = copy.deepcopy(tree)
    log = []
    for op in ops:
        kind = op["op"]
        if kind == "prune":
            doomed = {op["id"]} | set(descendants(tree, op["id"]))
            before = len(tree["nodes"])
            tree["nodes"] = [n for n in tree["nodes"] if n["id"] not in doomed]
            log.append(f"pruned {op['id']} ({before - len(tree['nodes'])} nodes removed)")
        elif kind == "annotate":
            for n in tree["nodes"]:
                if n["id"] == op["id"]:
                    n["note"] = op["note"]
                    log.append(f"annotated {op['id']}")
        elif kind == "move":
            parent = _parent_of(tree, op["id"])
            sibs = [n for n in tree["nodes"]
                    if n["parent"] == parent and n["id"] != op["id"]]
            target = next(n for n in tree["nodes"] if n["id"] == op["id"])
            sibs.insert(max(0, min(op["position"], len(sibs))), target)
            for i, s in enumerate(sibs):
                s["order"] = i
            log.append(f"moved {op['id']} to position {op['position']}")
        else:
            log.append(f"unknown op ignored: {kind}")
    return tree, log


def _parent_of(tree, node_id):
    return next(n["parent"] for n in tree["nodes"] if n["id"] == node_id)
