"""Safe, portable output. Embedded JSON and HTML are escaped for offline viewing."""
from __future__ import annotations
import html
import json
from pathlib import Path
from hashlib import sha256

STYLE = """body{margin:0;background:#080e1c;color:#e5edf9;font:15px/1.6 system-ui,sans-serif}main{max-width:1120px;margin:48px auto;padding:0 28px}h1{font-size:44px;letter-spacing:-1.5px;margin:0}h2{font-size:22px;margin-top:40px}small,.muted{color:#92a2bc}.tag{color:#6ee7ce;text-transform:uppercase;letter-spacing:3px;font-size:12px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:28px 0}.card{padding:22px;border:1px solid #253650;border-radius:12px;background:#101b2e}.value{font-size:27px;font-weight:650}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:11px;border-bottom:1px solid #253650}th{color:#92a2bc;font-size:12px;text-transform:uppercase}.PASS{color:#6ee7ce}.FAIL,.BLOCKED{color:#ff919e}.MISSING,.HOLD{color:#f8cc80}pre{white-space:pre-wrap;background:#101b2e;border:1px solid #253650;padding:20px;border-radius:10px;overflow-wrap:anywhere}code{font-family:ui-monospace,monospace}footer{margin:48px 0;color:#92a2bc;font-size:12px}.notice{border-left:3px solid #f8cc80;padding:12px 20px;background:#161d2b}@media(max-width:700px){.cards{grid-template-columns:1fr}main{margin:20px auto}h1{font-size:32px}td,th{padding:6px;font-size:12px}}"""

def render_html(state: dict) -> str:
    esc = html.escape
    a = state["assessment"]
    rows = "".join(f'<tr><td>{esc(c["obligation_id"])}</td><td>{esc(c["slice"])}</td><td>{esc(c["owner"])}</td><td class="{c["status"]}">{c["status"]}</td></tr>' for c in a["cells"])
    counters = esc(json.dumps(a["counterexamples"], indent=2))
    timeline = "".join(f'<li><strong>{esc(e["stage"])}</strong> <span class="muted">{esc(e["at"])}</span></li>' for e in state["events"])
    return f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ASTERION | Handoff dossier</title><style>{STYLE}</style><main>
    <div class="tag">ASTERION / Evidence-linked deployment rehearsals</div><h1>The handoff dossier.</h1><p class="muted">Synthetic case study · {esc(state['target_version'])} · {esc(state['request']['engine'])} engine</p>
    <div class="notice">{esc(a['disclaimer'])} Approval exports a rehearsal capsule; it never deploys an application.</div>
    <div class="cards"><div class="card"><small>HANDOFF STATE</small><div class="value">{esc(state['status'])}</div></div><div class="card"><small>REQUIRED-CELL COVERAGE</small><div class="value">{a['coverage']:.0%}</div></div><div class="card"><small>OBSERVED WITNESS PASS RATE</small><div class="value">{a['observed_pass_rate']:.1%}</div></div></div>
    <h2>Witness-Coverage Matrix</h2><p class="muted">A passing normal case cannot discharge an untested failure-mode obligation.</p><table><thead><tr><th>Obligation</th><th>Operational slice</th><th>Owner</th><th>Evidence</th></tr></thead><tbody>{rows}</tbody></table>
    <h2>Counterexamples</h2><pre>{counters}</pre><h2>Execution journal</h2><ol>{timeline}</ol>
    <h2>Evidence binding</h2><pre>Run: {esc(state['run_id'])}\nSHA-256: {esc(state['evidence_digest'])}</pre>
    <footer>Local prototype. Content hashes detect content changes; they are not digital signatures. No customer data. No production writes.</footer></main></html>"""


def markdown_report(state: dict) -> str:
    a = state["assessment"]
    lines = ["# ASTERION — Handoff dossier", "", f"Status: **{state['status']}**", "",
             f"Engine: `{state['request']['engine']}` · Target: `{state['target_version']}`",
             "", a["disclaimer"], "", f"Coverage: {a['coverage']:.1%}; observed witness pass rate: {a['observed_pass_rate']:.1%}.",
             "", "| Obligation | Slice | Status | Owner |", "|---|---|---|---|"]
    lines.extend(f"| {c['obligation_id']} | {c['slice']} | {c['status']} | {c['owner']} |" for c in a["cells"])
    lines += ["", "## Counterexamples", "```json", json.dumps(a["counterexamples"], indent=2), "```", "", "## Evidence digest", f"`{state['evidence_digest']}`"]
    return "\n".join(lines) + "\n"


def export_dossier(state: dict, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    outputs = {"report.json": json.dumps(state, indent=2) + "\n", "report.md": markdown_report(state),
               "report.html": render_html(state),
               "events.jsonl": "".join(json.dumps(e) + "\n" for e in state["events"])}
    # Write the exact bytes that are hashed. Text-mode writes translate "\n" to "\r\n" on Windows,
    # which made every exported dossier fail its own manifest check there.
    encoded = {name: content.encode("utf-8") for name, content in outputs.items()}
    for name, data in encoded.items():
        (directory / name).write_bytes(data)
    manifest = {"kind": "rehearsal-dossier", "production_deployment": False,
                "status": state["status"], "evidence_digest": state["evidence_digest"],
                "files": {name: sha256(data).hexdigest() for name, data in encoded.items()},
                "hash_encoding": "SHA-256 of raw UTF-8 file bytes; not a signature"}
    (directory / "manifest.json").write_bytes((json.dumps(manifest, indent=2) + "\n").encode("utf-8"))
