# System atlas

Every architectural plate is supplied as editable SVG and PNG. Mermaid source under `diagrams/` expresses the same responsibility/state boundaries in a text-editable form. The visual generator is `scripts/render_diagrams.py` (requires Pillow and CairoSVG). Raster screenshots come from the actual offline HTML explorer, not a fabricated cloud console.

| Plate | What it explains | Assets |
|---|---|---|
| 01 — System atlas | Client boundary, shared nodes, evidence, storage and optional cloud target | [PNG](../assets/01-system-atlas.png) · [SVG](../assets/01-system-atlas.svg) |
| 02 — Runtime | Bounded loop, termination, review interruption and final authority | [PNG](../assets/02-runtime-statechart.png) · [SVG](../assets/02-runtime-statechart.svg) |
| 03 — Witness gate | Mechanism and actual synthetic result comparison | [PNG](../assets/03-witness-gate.png) · [SVG](../assets/03-witness-gate.svg) |
| 04 — AWS | Private service target and narrower supplied foundation | [PNG](../assets/04-aws-reference.png) · [SVG](../assets/04-aws-reference.svg) |
| 05 — Azure | Equivalent responsibility mapping, explicitly design-only | [PNG](../assets/05-azure-reference.png) · [SVG](../assets/05-azure-reference.svg) |
| 06 — Trust | Principal, planner, oracle, evaluator and approval boundaries | [PNG](../assets/06-trust-boundaries.png) · [SVG](../assets/06-trust-boundaries.svg) |
| 07 — FDE | Discovery through acceptance and operational ownership | [PNG](../assets/07-fde-delivery-loop.png) · [SVG](../assets/07-fde-delivery-loop.svg) |
| 08 — Evidence | Entity shapes, data flow and digest-bound review | [PNG](../assets/08-evidence-model.png) · [SVG](../assets/08-evidence-model.svg) |

Legend: solid nodes generally represent local implementation; purple/dashed nodes are optional integrations; gold/dashed nodes are unimplemented deployment targets. Captions take precedence over color. The generated hero is branding, not a source of implementation claims. No vendor logo or certification badge is used to imply affiliation.
