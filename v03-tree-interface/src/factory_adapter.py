#!/usr/bin/env python3
"""FactoryAdapter — the real Hoolulu Factory behind the FactoryPort contract.

Canon: adapters never fake execution. If the factory is unreachable this
adapter reports NOT_CONNECTED and submit_build raises NotConnectedError
with an explicit reason. No silent stubs, no invented builds.

Config (env, never hardcoded hosts):
  FACTORY_BASE_URL  default http://localhost:8000
  FACTORY_TIMEOUT_S  default 600 (covers SSE build stream + poll fallback)

Stdlib only.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

from adapters import FactoryPort, NotConnectedError


DEFAULT_BASE_URL = "http://localhost:8000"
DEFAULT_TIMEOUT_S = 600
MAX_PROMPT_CHARS = 12000  # factory MessageCreate.content limit


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def build_prompt(build_spec: dict) -> str:
    """Turn a compiled build spec into a factory build prompt.

    Kept separate from transport so prompt wording can evolve without
    touching the HTTP layer.
    """
    spec_id = build_spec.get("spec_id", "unknown")
    governor = build_spec.get("governor", {}) or {}
    approval_points = governor.get("approval_points", []) or []
    execution_order = governor.get("execution_order", []) or []
    tree_id = spec_id[:-len("-spec")] if spec_id.endswith("-spec") else spec_id

    lines = [
        f"Build the web project for compiled system '{tree_id}'.",
        f"Nodes: {build_spec.get('node_count', '?')}. Governor verdict: {governor.get('verdict', 'GO')}.",
    ]
    if execution_order:
        lines.append("Execution order: " + " -> ".join(str(x) for x in execution_order))
    if approval_points:
        lines.append("Human approval points in this system:")
        for point in approval_points:
            lines.append(f"- {point}")
    lines += [
        "",
        "Produce a complete, self-contained static web project (index.html plus",
        "assets) implementing this system. Validate before packaging.",
    ]
    prompt = "\n".join(lines)
    if len(prompt) > MAX_PROMPT_CHARS:
        prompt = prompt[: MAX_PROMPT_CHARS - 3] + "..."
    return prompt


class FactoryAdapter(FactoryPort):
    """Real Hoolulu Factory. Fail-closed: no factory, no build, explicit error."""

    def __init__(self, base_url: str | None = None, timeout_s: float | None = None):
        self.base_url = (base_url or os.environ.get("FACTORY_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout_s = float(timeout_s or os.environ.get("FACTORY_TIMEOUT_S") or DEFAULT_TIMEOUT_S)

    # ------------------------------------------------------------------
    # connectivity
    # ------------------------------------------------------------------
    def check_connection(self) -> tuple[str, str]:
        """Returns (status, detail). Status is CONNECTED or NOT_CONNECTED."""
        try:
            health = self._get("/api/health")
        except Exception as exc:  # noqa: BLE001 - detail string is the point
            return "NOT_CONNECTED", f"health check failed: {exc}"
        if not isinstance(health, dict) or health.get("status") != "ok":
            return "NOT_CONNECTED", f"health check unexpected response: {str(health)[:120]}"
        try:
            core = self._get("/api/core")
        except Exception as exc:  # noqa: BLE001
            return "NOT_CONNECTED", f"core check failed: {exc}"
        digest = core.get("digest", "?") if isinstance(core, dict) else "?"
        return "CONNECTED", f"service ok, core digest {str(digest)[:12]}"

    # ------------------------------------------------------------------
    # FactoryPort
    # ------------------------------------------------------------------
    def submit_build(self, build_spec: dict) -> dict:
        log: list[str] = []

        def trace(msg: str) -> None:
            log.append(f"[{_now()}] {msg}")

        spec_id = str(build_spec.get("spec_id", "unknown"))
        trace(f"submit_build spec={spec_id}")

        status, detail = self.check_connection()
        trace(f"connectivity: {status} ({detail})")
        if status != "CONNECTED":
            raise NotConnectedError(f"Factory {status}: {detail}")

        governor = build_spec.get("governor", {}) or {}
        if governor.get("verdict", "GO") != "GO":
            blocking = list(governor.get("missing_dependencies", []) or []) + list(
                governor.get("ordering", []) or []
            )
            trace(f"refused: governor verdict is not GO ({len(blocking)} blocking flags); no HTTP build attempted")
            return {
                "job_id": f"refused-{spec_id}",
                "status": "failed",
                "artifacts": [],
                "log": log + [f"BLOCKED: {b}" for b in blocking],
            }

        prompt = build_prompt(build_spec)
        trace(f"prompt built ({len(prompt)} chars)")

        try:
            conv = self._post("/api/conversations", {"title": spec_id[:80]})
            conversation_id = conv["id"]
            trace(f"conversation {conversation_id}")
        except Exception as exc:  # noqa: BLE001
            trace(f"conversation create failed: {exc}")
            return self._failed(spec_id, log, f"conversation create failed: {exc}")

        try:
            final_build = self._stream_build(conversation_id, prompt, trace)
        except Exception as exc:  # noqa: BLE001
            trace(f"build stream failed: {exc}")
            return self._failed(spec_id, log, f"build stream failed: {exc}")

        build_id = final_build.get("id", "?")
        build_status = str(final_build.get("status", "unknown"))
        trace(f"build {build_id} terminal status: {build_status}")

        port_status = {"completed": "done", "failed": "failed"}.get(build_status, "failed")
        artifacts: list[str] = []
        if port_status == "done":
            artifacts = [
                self.base_url + final_build.get("download_url", f"/api/builds/{build_id}/download"),
                self.base_url + final_build.get("preview_url", f"/api/builds/{build_id}/preview/"),
            ]
            trace(f"artifacts: {artifacts}")

        error = None if port_status == "done" else f"factory reported status={build_status}"
        log.append(self._handoff_record(spec_id, build_id, port_status, artifacts, error))
        return {"job_id": build_id, "status": port_status, "artifacts": artifacts, "log": log}

    # ------------------------------------------------------------------
    # transport
    # ------------------------------------------------------------------
    def _stream_build(self, conversation_id: str, prompt: str, trace) -> dict:
        """POST the build message, consume the SSE stream to its terminal event.

        Returns the final public build dict. Falls back to polling if the
        stream drops before a terminal event.
        """
        url = self.base_url + f"/api/conversations/{conversation_id}/messages"
        body = json.dumps({"content": prompt, "mode": "build"}).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")

        build_id: str | None = None
        final_build: dict | None = None
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                event_name: str | None = None
                data_lines: list[str] = []
                for raw in resp:
                    line = raw.decode("utf-8", "replace").strip()
                    if line.startswith("event:"):
                        event_name = line[6:].strip()
                    elif line.startswith("data:"):
                        data_lines.append(line[5:].strip())
                    elif line == "" and event_name:
                        payload = json.loads("".join(data_lines)) if data_lines else {}
                        data_lines = []
                        name, event_name = event_name, None
                        if name == "build" and isinstance(payload.get("build"), dict):
                            build_id = payload["build"].get("id")
                            trace(f"sse: build started {build_id}")
                        elif name in ("artifact", "build_error", "done"):
                            b = payload.get("build")
                            if isinstance(b, dict):
                                final_build = b
                                trace(f"sse: terminal event '{name}' status={b.get('status')}")
                                if name == "done":
                                    break
                # stream ended without terminal event
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"factory HTTP {exc.code}: {exc.read().decode()[:200]}") from exc

        if final_build is not None:
            return final_build
        if build_id:
            trace("sse: stream ended early, falling back to poll")
            return self._poll_build(build_id, trace)
        raise RuntimeError("build stream ended with no build id and no terminal event")

    def _poll_build(self, build_id: str, trace) -> dict:
        deadline = time.time() + self.timeout_s
        wait = 2.0
        while time.time() < deadline:
            build = self._get(f"/api/builds/{build_id}")
            st = str(build.get("status", "unknown"))
            if st in ("completed", "failed"):
                return build
            trace(f"poll: status={st}, waiting {wait:.0f}s")
            time.sleep(wait)
            wait = min(wait * 1.5, 30.0)
        raise TimeoutError(f"build {build_id} did not finish within {self.timeout_s:.0f}s")

    def _get(self, path: str) -> dict:
        req = urllib.request.Request(self.base_url + path, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"GET {path} -> HTTP {exc.code}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"GET {path} unreachable: {exc.reason}") from exc

    def _post(self, path: str, payload: dict) -> dict:
        body = json.dumps(payload).encode()
        req = urllib.request.Request(
            self.base_url + path, data=body, headers={"Content-Type": "application/json"}, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"POST {path} -> HTTP {exc.code}: {exc.read().decode()[:200]}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"POST {path} unreachable: {exc.reason}") from exc

    # ------------------------------------------------------------------
    # records
    # ------------------------------------------------------------------
    @staticmethod
    def _handoff_record(spec_id: str, build_id: str, status: str, artifacts: list, error) -> str:
        rec = {
            "source": "IMGCODE compiler",
            "target": "Hoolulu Factory API",
            "input": spec_id,
            "output": f"build {build_id} status={status} artifacts={artifacts}",
            "status": "CONNECTED" if status == "done" else "COMPLETED_WITH_ERROR",
            "error": error,
        }
        return "HANDOFF " + json.dumps(rec)

    @staticmethod
    def _failed(spec_id: str, log: list[str], error: str) -> dict:
        log.append(f"[{_now()}] FAILED: {error}")
        return {"job_id": f"error-{spec_id}", "status": "failed", "artifacts": [], "log": log}
