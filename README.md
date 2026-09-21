# Agentic AI Field Guide (2026 Edition)

A **26-page, print-optimized technical field guide** on designing production-grade agentic systems — published free as a public-edition PDF by **AZ Engineering** (Aamir Zameer).

> Full public edition (PDF): free download behind a simple email gate — see [landing/](landing/).
> Author page in the guide links to consultations, Topmate products, X and LinkedIn.

## What's inside

- **3 technical diagrams** (inline SVG): the request loop, orchestration topology, and hybrid cost-routing tiers
- **Layer-by-layer architecture map** — intake to delivery, with guardrails at every boundary
- **5-question readiness scorecard** + 30-day field checklist
- Separate reading tracks for executives and engineers, plus a plain-language glossary

## Repository structure

| Path | What it is |
|---|---|
| `AZ-Engineering-Agentic-AI-Field-Guide.html` | Single-file HTML (print CSS + WordPress-compatible), the master source |
| `AZ-Engineering-Agentic-AI-Field-Guide.pdf` | Rendered A4 PDF — 26 pages |
| `AZ-Field-Guide-2026-Free-Preview.pdf` | 5-page luring teaser: first 4 pages + poster page with QR |
| `src/` | Build source: `part_a.html` (CSS/cover), `part_b.html` (sections/TOC), fragment files, build scripts |
| `landing/` | Email-gated landing page (deploys to Cloudflare Pages) |

## How it's built

The book is authored as two HTML parts plus fragments; a small script splices fragments, then headless Chrome renders the assembled HTML to PDF:

```bash
python3 src/update_ebook.py          # splice footers / diagrams / author page
cat src/part_a.html src/part_b.html > AZ-Engineering-Agentic-AI-Field-Guide.html
python3 src/toc_sync.py              # re-sync contents page numbers after reflow
google-chrome --headless=new --no-sandbox --no-pdf-header-footer \
  --print-to-pdf=AZ-Engineering-Agentic-AI-Field-Guide.pdf \
  file://$(pwd)/AZ-Engineering-Agentic-AI-Field-Guide.html
```

## License

© 2026 AZ Engineering (Aamir Zameer). The free public-edition PDF may be distributed
as-is. Source, diagrams and copy may **not** be reused commercially or republished
without written permission — a licensed corporate edition is available from the author.
Contact: azengineeringapp@gmail.com

---

Part of [my always-on agent stack](https://github.com/Amz34) · [Awesome Agent Infrastructure](https://github.com/Amz34/awesome-agent-infrastructure) (135 live-checked building blocks).
