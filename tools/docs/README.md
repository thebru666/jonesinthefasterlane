# Render the Mermaid documentation

This documentation-only tool extracts every Mermaid fenced block under `docs/`, renders SVG and PNG copies, and creates an offline HTML gallery plus a Markdown index. It does not change diagram semantics or contain game application code. Original-game reference diagrams contain analytical summaries, not extracted art/code.

## Dependencies and regeneration

Use Python3, Node.js, Playwright and Chromium/Chrome. Mermaid is pinned to12.2.0, with npm package SHA-512 verification in the download helper. The downloaded third-party renderer/license stay in ignored `work/diagram-renderer/`; no global npm installation is required. Rendered files and original Mermaid fence copies are committed.

From the repository root:

```sh
python3 tools/docs/prepare_mermaid.py
node tools/docs/render-mermaid.mjs \
  --playwright-module /absolute/path/to/playwright/index.mjs \
  --browser /absolute/path/to/chrome
```

On the current Codex host, the bundled runtime provides Node at `/home/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node`, Playwright at `/home/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs`, and Chrome at `/opt/google/chrome/chrome`. Other computers should supply their own absolute dependency paths. The bundle path defaults to `work/diagram-renderer/mermaid.min.js` and can be overridden with `--mermaid-js` (matching package metadata required).

Open [the gallery](../../docs/diagrams/README.md) or `artifacts/diagrams/index.html`. Each source document is labelled by original-reference/current-proposal/earlier-draft status. The manifest records Mermaid source and rendered-file hashes, dimensions and renderer details. Browser fonts/layout can affect output bytes; semantic diagrams remain sourced from the Markdown files.

HTTP requests are blocked while rendering; diagram text stays local. The initial checksum-verified renderer download requires access to the npm registry. The headless documentation browser uses `--no-sandbox` for this container, loads only the local renderer and source strings, and closes after export.
