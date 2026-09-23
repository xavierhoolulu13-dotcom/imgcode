#!/usr/bin/env python3
"""IMGCODE v0.3 — offline cockpit dashboard for Termux.

Serves a tap-friendly control page on localhost: pick a tree, run the
loop, read the sales package, approve or hold. Nothing leaves the phone.

Stdlib only. Binds 127.0.0.1 (this device, no network exposure).

Usage:
  python3 dashboard.py [port]
Then open http://127.0.0.1:8080 in the phone's browser.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from approve import chain_hash, last_hash, LOG  # reuse the gate's chain logic

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html(self):
        with open(os.path.join(HERE, "dashboard.html"), "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            self._html()
        elif path == "/api/trees":
            trees = []
            d = os.path.join(HERE, "tree-ir")
            for fn in sorted(os.listdir(d)):
                if fn.endswith(".json") and fn != "schema.json":
                    try:
                        t = json.load(open(os.path.join(d, fn)))
                        if not t.get("tree_id"):
                            continue
                        trees.append({
                            "file": "tree-ir/" + fn,
                            "tree_id": t.get("tree_id"),
                            "label": (t.get("root") or {}).get("label"),
                            "nodes": len(t.get("nodes", [])),
                        })
                    except Exception:
                        pass
            self._json(trees)
        elif path == "/api/package":
            p = os.path.join(HERE, "sales-package.json")
            self._json(json.load(open(p)) if os.path.exists(p) else {})
        elif path == "/api/log":
            lines = []
            if os.path.exists(LOG):
                for line in open(LOG):
                    line = line.strip()
                    if line:
                        lines.append(json.loads(line))
            self._json(lines)
        else:
            self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            data = {}

        if path == "/api/run":
            tree = data.get("tree") or "tree-ir/visibility-audit-tree.json"
            tree = os.path.basename(tree)
            if not tree.startswith("tree-ir/"):
                tree = "tree-ir/" + tree
            proc = subprocess.run(
                [sys.executable, os.path.join(HERE, "run_loop.py"), tree],
                capture_output=True, text=True, cwd=HERE, timeout=120)
            out = proc.stdout + proc.stderr
            facts = {"ok": proc.returncode == 0}
            for line in out.splitlines():
                s = line.strip()
                if s.startswith("valid:"):
                    facts["valid"] = s
                elif s.startswith("verdict:"):
                    facts["verdict"] = s
            self._json(facts)
        elif path == "/api/decision":
            decision = str(data.get("decision", "HOLD")).upper()
            if decision not in ("APPROVE", "HOLD"):
                decision = "HOLD"
            p = os.path.join(HERE, "sales-package.json")
            package = json.load(open(p)) if os.path.exists(p) else {}
            prev = last_hash()
            record = {
                "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "decision": decision,
                "package": "sales-package.json",
                "tree_id": package.get("tree_id"),
                "business": package.get("business"),
                "proposed_offer": package.get("proposed_offer"),
                "note": str(data.get("note", "")),
                "by": "Xavier",
            }
            record["prev_hash"] = prev
            record["hash"] = chain_hash(record)
            with open(LOG, "a") as f:
                f.write(json.dumps(record) + "\n")
            self._json({"ok": True, "decision": decision})
        else:
            self.send_error(404)

    def log_message(self, *args):  # keep the terminal quiet
        pass


if __name__ == "__main__":
    srv = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"IMGCODE cockpit: http://127.0.0.1:{PORT}  (offline, Ctrl-C to stop)")
    srv.serve_forever()
