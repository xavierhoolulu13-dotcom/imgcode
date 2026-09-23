#!/usr/bin/env python3
"""MARKET MATCH — [STUB / DEMO].

Real matching runs inside GPT808 DISCOVER. This stub demonstrates the
contract: product tree + business profile -> sales package shape.
It uses toy gap rules so Xavier can SEE the process end to end.

A sales package NEVER sends outreach. Human approval gate stays fail-closed.
"""


def match_business(tree, business):
    """business: dict with name, biz_type, has_website, review_score, notes."""
    gaps = []
    if not business.get("has_website"):
        gaps.append("No website found — invisible on Google")
    if (business.get("review_score") or 5) < 4.0:
        gaps.append(f"Review score {business.get('review_score')} — losing trust clicks")
    if "google" not in (business.get("notes") or "").lower():
        gaps.append("Google Business Profile looks unclaimed or stale")

    offer_nodes = [n for n in tree["nodes"] if n["kind"] == "offer"]
    offer_labels = []
    for o in offer_nodes:
        kids = [n["label"] for n in tree["nodes"] if n["parent"] == o["id"]]
        offer_labels += kids or [o["label"]]

    package = {
        "stage": "SALES PACKAGE",
        "status": "[STUB] demo match — real matching runs in GPT808 DISCOVER",
        "business": business["name"],
        "biz_type": business.get("biz_type"),
        "tree_id": tree["tree_id"],
        "niche_fit": tree["meta"]["niche"],
        "gaps_found": gaps,
        "product_fit": f"{tree['root']['label']} tree covers: "
                       + ", ".join(sorted({n['label'] for n in tree['nodes']
                                            if n['kind'] == 'system'})),
        "proposed_offer": offer_labels,
        "human_approval": "REQUIRED — Xavier must approve before any outreach (808 gate).",
        "verdict": "READY FOR XAVIER'S REVIEW" if gaps else "no gaps found — skip",
    }
    return package


SAMPLE_BUSINESS = {
    "name": "Ala Moana Poke Co. (sample)",
    "biz_type": "restaurant",
    "has_website": False,
    "review_score": 3.6,
    "notes": "Instagram only, no Google profile claimed",
}


if __name__ == "__main__":
    import json, sys
    sys.path.insert(0, "src")
    from validate import load_tree
    tree = load_tree(sys.argv[1]) if len(sys.argv) > 1 else load_tree("tree-ir/visibility-audit-tree.json")
    print(json.dumps(match_business(tree, SAMPLE_BUSINESS), indent=2))
