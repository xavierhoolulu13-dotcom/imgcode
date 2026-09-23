# IMGCODE v0.3 — Termux Offline Cheat Sheet

## [1] FIRST TIME (needs internet once)
```
pkg install -y python git
cd ~
git clone https://github.com/xavierhoolulu13-dotcom/imgcode
```

## [2] UPDATE (needs internet)
```
cd ~/imgcode && git pull
```

## [3] RUN THE LOOP (works offline)
```
cd ~/imgcode/v03-tree-interface
python3 run_loop.py ~/my-tree.json
```

## [4] SAMPLE TREES (works offline)
```
python3 run_loop.py tree-ir/visibility-audit-tree.json
python3 run_loop.py tree-ir/restaurant-os-tree.json
python3 run_loop.py tree-ir/eco-cycle-subscription-001.json
```

## [5] READ THE RESULTS (works offline)
```
python3 -m json.tool sales-package.json
cat HANDOFF.md
```

## [6] APPROVE OR HOLD (works offline)
```
python3 approve.py sales-package.json --approve
python3 approve.py sales-package.json --hold --note "waiting on pricing"
cat approvals.log.jsonl
```

## [7] REAL RUN (research needs internet; loop works offline)
```
python3 run_loop.py tree-ir/visibility-audit-tree.json business-profiles/hopohni-honolulu.json
```

## [9] BROWSER DASHBOARD (works offline)
```
cd ~/imgcode/v03-tree-interface
python3 dashboard.py
```
Then open **http://127.0.0.1:8080** in the phone browser.
Tap a tree → RUN → read the package → APPROVE or HOLD.

## [10] DAILY FLOW
```
pull → run → read → approve
```
