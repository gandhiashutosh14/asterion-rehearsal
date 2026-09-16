"""Start the API under uvicorn exactly as the Dockerfile does, exercise it over HTTP, then stop it.

    python scripts/api_smoke.py [--port 8765]

Requires the `api` extra. Uses throwaway tokens and a temporary state directory; nothing is
exposed beyond 127.0.0.1 and the server is terminated before the script exits.
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
import subprocess
import sys
import tempfile
import time

import httpx


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    base = f"http://127.0.0.1:{args.port}"
    operator, reviewer = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
    tokens = {operator: {"tenant": "smoke", "role": "operator", "actor": "smoke-operator"},
              reviewer: {"tenant": "smoke", "role": "reviewer", "actor": "smoke-reviewer"}}
    checks: list[tuple[str, bool]] = []

    def check(name: str, ok: bool) -> None:
        checks.append((name, ok))
        print(("PASS " if ok else "FAIL ") + name)

    with tempfile.TemporaryDirectory() as state:
        env = {**os.environ, "ASTERION_API_TOKENS": json.dumps(tokens), "ASTERION_STATE_DIR": state}
        command = [sys.executable, "-m", "uvicorn", "asterion.api:create_app", "--factory",
                   "--host", "127.0.0.1", "--port", str(args.port), "--workers", "1", "--no-access-log"]
        server = subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        try:
            with httpx.Client(base_url=base, timeout=30) as client:
                deadline = time.monotonic() + 30
                while True:
                    try:
                        health = client.get("/healthz")
                        break
                    except httpx.TransportError:
                        if time.monotonic() > deadline or server.poll() is not None:
                            raise SystemExit("server did not start")
                        time.sleep(0.2)
                check("GET /healthz -> 200 synthetic-only", health.status_code == 200 and health.json()["mode"] == "synthetic-only")
                check("GET /v1/runs without a token -> 401", client.get("/v1/runs").status_code == 401)
                op = {"Authorization": f"Bearer {operator}", "Idempotency-Key": "smoke-1"}
                created = client.post("/v1/runs", json={}, headers=op)
                run = created.json()
                check("POST /v1/runs -> 201 PENDING_REVIEW", created.status_code == 201 and run["status"] == "PENDING_REVIEW")
                again = client.post("/v1/runs", json={}, headers=op)
                check("same Idempotency-Key -> 200, same run", again.status_code == 200 and again.json()["run_id"] == run["run_id"])
                check("same key, different request -> 409",
                      client.post("/v1/runs", json={"profile": "optimistic"}, headers=op).status_code == 409)
                path = f"/v1/runs/{run['run_id']}"
                events = client.get(path + "/events", headers=op)
                check("GET events -> SSE journal replay",
                      events.status_code == 200 and events.text.count("event: journal") == len(run["events"]))
                review = {"decision": "approve", "expected_digest": run["evidence_digest"], "rationale": "Smoke-test review"}
                check("operator cannot review -> 403", client.post(path + "/review", json=review, headers=op).status_code == 403)
                rv = {"Authorization": f"Bearer {reviewer}"}
                approved = client.post(path + "/review", json=review, headers=rv)
                check("reviewer approves with the exact digest -> APPROVED",
                      approved.status_code == 200 and approved.json()["status"] == "APPROVED")
                check("second review -> 409", client.post(path + "/review", json=review, headers=rv).status_code == 409)
                report = client.get(path + "/report", headers=op)
                check("GET report -> HTML with nosniff",
                      report.status_code == 200 and report.headers.get("x-content-type-options") == "nosniff"
                      and "APPROVED" in report.text)
        finally:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()
    failed = [name for name, ok in checks if not ok]
    print(f"{len(checks) - len(failed)} of {len(checks)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
