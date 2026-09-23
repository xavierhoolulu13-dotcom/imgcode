#!/usr/bin/env python3
"""Organism vitals — minimal dashboard seed.

Run from v03-tree-interface/:
    python3 vitals.py

Prints one line per organ: tree validation, factory connectivity.
Stdlib only. Exit 0 = all GO, 1 = something needs Xavier.
"""

import glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from validate import load_tree, validate  # noqa: E402
from adapters import factory  # noqa: E402

try:
    from factory_adapter import FactoryAdapter  # noqa: E402
except Exception:
    FactoryAdapter = None


def main() -> int:
    print("=== ORGANISM VITALS ===")
    bad = 0

    for path in sorted(glob.glob("tree-ir/*.json")):
        name = path.split("/")[-1]
        if name == "schema.json":
            continue
        try:
            ok, _errs = validate(load_tree(path))
        except Exception as exc:  # noqa: BLE001
            print(f"tree     {name:38} ERROR {exc}")
            bad += 1
            continue
        print(f"tree     {name:38} {'GO' if ok else 'BLOCKED'}")
        if not ok:
            bad += 1

    real = FactoryAdapter is not None and isinstance(factory, FactoryAdapter)
    if real:
        status, detail = factory.check_connection()
    else:
        status, detail = "NOT_CONNECTED", "stub wired (no real adapter)"
    print(f"factory  {'FactoryAdapter' if real else 'FactoryStub':38} {status} ({detail})")
    if status != "CONNECTED":
        bad += 1

    print("=======================")
    print("ALL GO" if bad == 0 else f"{bad} ORGAN(S) NEED XAVIER")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
