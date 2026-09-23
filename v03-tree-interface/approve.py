#!/usr/bin/env python3
"""APPROVAL GATE — Xavier's decision, recorded.

The loop runs itself. This is the one step that needs a human.
Nothing downstream moves without an --approve record. Fail-closed.

Usage:
  python3 approve.py sales-package.json --approve [--note "go, they fit the niche"]
  python3 approve.py sales-package.json --hold [--note "waiting on pricing"]

Decisions append to approvals.log.jsonl — timestamped, hash-chained,
append-only. Editing a line breaks the chain.

Stdlib only. Works offline.
"""
import json
import sys
import os
import hashlib
from datetime import datetime, timezone

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "approvals.log.jsonl")


def chain_hash(prev_hash, record):
    body = prev_hash + json.dumps(record, sort_keys=True)
    return hashlib.sha256(body.encode()).hexdigest()


def last_hash():
    if not os.path.exists(LOG):
        return "GENESIS"
    h = "GENESIS"
    with open(LOG) as f:
        for line in f:
            line = line.strip()
            if line:
                h = json.loads(line)["hash"]
    return h


def main():
    if len(sys.argv) < 3 or sys.argv[2] not in ("--approve", "--hold"):
        print(__doc__)
        sys.exit(2)

    package_path, decision = sys.argv[1], sys.argv[2][2:].upper()
    note = ""
    if "--note" in sys.argv:
        note = sys.argv[sys.argv.index("--note") + 1]

    with open(package_path) as f:
        package = json.load(f)

    prev = last_hash()
    record = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "decision": decision,
        "package": os.path.basename(package_path),
        "tree_id": package.get("tree_id"),
        "business": package.get("business"),
        "proposed_offer": package.get("proposed_offer"),
        "note": note,
        "by": "Xavier",
    }
    record["prev_hash"] = prev
    record["hash"] = chain_hash(prev, record)

    with open(LOG, "a") as f:
        f.write(json.dumps(record) + "\n")

    print("=" * 55)
    print(f" DECISION RECORDED: {decision}")
    print("=" * 55)
    print(f"  business: {record['business']}")
    print(f"  offer:    {record['proposed_offer']}")
    if note:
        print(f"  note:     {note}")
    print(f"  logged:   approvals.log.jsonl")
    if decision == "APPROVE":
        print("  -> released. Next: outreach / GPT808 (manual until wired).")
    else:
        print("  -> held. Nothing moves. Re-run approve.py to release later.")


if __name__ == "__main__":
    main()
