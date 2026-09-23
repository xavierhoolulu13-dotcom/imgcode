#!/usr/bin/env python3
"""ADAPTER PORTS — where the real systems plug into the v0.3 loop.

The loop owns:  TREE IN -> VALIDATE -> COMPOSE -> COMPILE -> SALES PACKAGE
It does NOT own: Factory execution, GPT808 market-match / approval.
One job per system. No mega-agent.

This file is the contract both sides must speak. A port defines the exact
input/output shapes; the stub implementations below prove the shape but do
no real work. Swapping a stub for the real system = implement the port,
change one import in run_loop.py. Nothing else in the loop moves.

Real systems (recorded 2026-09-23):
  - FactoryPort  -> Hoolulu Factory, lives in Xavier's GitHub (dispatch TBD)
  - GPT808Port   -> GPT808 Sales Factory, Frozen Spine v1.0.0, lives in Teamily
"""

from abc import ABC, abstractmethod


class NotConnectedError(RuntimeError):
    """Raised when a port has no real implementation wired in yet."""


# --------------------------------------------------------------------------
# FactoryPort — Hoolulu Factory (build execution)
# --------------------------------------------------------------------------
class FactoryPort(ABC):
    """Takes the compiler's build spec, builds it, reports back.

    Input:  build-spec.json dict from compile.compile_tree()
            {tree_id, nodes, governor:{verdict,...}, handoff:{...}}
    Output: {"job_id": str, "status": "queued|building|done|failed",
             "artifacts": [paths/urls], "log": [lines]}
    """

    @abstractmethod
    def submit_build(self, build_spec):
        """Queue a build. Returns the job dict. Never raises on queueing."""


class FactoryStub(FactoryPort):
    """[NOT CONNECTED] Honest stand-in. Accepts the spec, builds nothing."""

    def submit_build(self, build_spec):
        return {
            "job_id": "stub-" + build_spec.get("spec_id", "unknown"),
            "status": "queued",
            "artifacts": [],
            "log": ["[STUB] spec accepted; real execution runs in Hoolulu Factory."],
        }


# --------------------------------------------------------------------------
# GPT808Port — GPT808 Sales Factory (market match + approval gate)
# --------------------------------------------------------------------------
# Maps to real GPT808 stages:
#   discover()        -> DISCOVER stage (find the gaps in a real business)
#   request_approval() -> APPROVE stage / 808 Approval Gate
# Gate semantics (Frozen Spine v1.0.0): every action classifies as
#   APPROVED | ESCALATE | DENIED. Unknown action types ESCALATE.
#   Approval is decision-scoped: one amount, one run, then the ceiling resets.
#   Fail-closed: nothing moves without a human decision. binding: false
#   for every advisory layer (Spin Bot 808, Digital Twin).
class GPT808Port(ABC):
    @abstractmethod
    def discover(self, business):
        """DISCOVER: business profile -> {"gaps": [...], "evidence": [...]}

        business: {"name", "biz_type", "has_website", "review_score", "notes"}
        gaps: [{"gap": str, "evidence": str}] — observable facts only,
              no invented data.
        """

    @abstractmethod
    def request_approval(self, action):
        """APPROVE: action -> "APPROVED" | "ESCALATE" | "DENIED"

        action: {"type", "business", "amount_usd", "payload", "run_id"}
        Fail-closed: anything unrecognized -> "ESCALATE".
        The stub always ESCALATES, exactly like the real gate does when
        Xavier hasn't drawn the line yet.
        """


class GPT808Stub(GPT808Port):
    """[NOT CONNECTED] Honest stand-in. Discovers toy gaps, escalates all."""

    def discover(self, business):
        gaps = []
        if not business.get("has_website"):
            gaps.append({"gap": "No website found",
                         "evidence": "has_website=false in profile"})
        if (business.get("review_score") or 5) < 4.0:
            gaps.append({"gap": f"Review score {business.get('review_score')}",
                         "evidence": "below 4.0 trust threshold"})
        return {"gaps": gaps, "evidence": ["stub rules — real DISCOVER in GPT808"]}

    def request_approval(self, action):
        return "ESCALATE"  # fail-closed: Xavier decides, always


# --------------------------------------------------------------------------
# Wiring: one line swaps a stub for the real thing.
# --------------------------------------------------------------------------
try:
    from factory_adapter import FactoryAdapter
    factory = FactoryAdapter()  # real Hoolulu Factory; fail-closed (raises NotConnectedError when unreachable)
except Exception:
    factory = FactoryStub()     # adapter module missing/broken -> honest stub, never fake success
gpt808 = GPT808Stub()        # -> real GPT808 adapter goes here
