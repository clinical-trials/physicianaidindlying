#!/usr/bin/env python3
"""Inline data/policy.json into index.html to produce single-file builds.

The repo version fetches its data at runtime, which needs an HTTP server.
These builds do not — useful for emailing a copy, opening from a USB stick,
or publishing somewhere that blocks cross-file requests.

    python3 scripts/build_standalone.py

Outputs:
  dist/standalone.html   full page; opens directly from the filesystem
  dist/artifact.html     same content, wrapper tags stripped for embedding
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
DATA = ROOT / "data" / "policy.json"
DIST = ROOT / "dist"

MARKER = "<script>\n(function(){"


def main():
    if not SRC.exists() or not DATA.exists():
        print(f"✗ missing {SRC if not SRC.exists() else DATA}")
        return 1

    html = SRC.read_text()
    data = json.loads(DATA.read_text())  # parse first so bad JSON fails loudly

    if MARKER not in html:
        print("✗ could not find the main <script> block in index.html")
        return 1

    # </script> inside a script block would terminate it early; JSON can legally
    # contain that sequence inside a string, so neutralise it.
    payload = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    inject = (
        "<script>window.__POLICY_DATA__=" + payload + ";</script>\n" + MARKER
    )
    built = html.replace(MARKER, inject, 1)

    DIST.mkdir(exist_ok=True)
    (DIST / "standalone.html").write_text(built)

    # Artifact/embed variant: strip the document wrapper, keep everything inside.
    frag = built
    frag = re.sub(r"(?is)^.*?<head[^>]*>", "", frag)
    frag = re.sub(r"(?is)</head>\s*<body[^>]*>", "\n", frag)
    frag = re.sub(r"(?is)</body>\s*</html>\s*$", "", frag)
    frag = re.sub(r'(?is)<meta[^>]*charset[^>]*>\s*', "", frag)
    frag = re.sub(r'(?is)<meta[^>]*name="viewport"[^>]*>\s*', "", frag)
    (DIST / "artifact.html").write_text(frag.strip() + "\n")

    def kb(p):
        return f"{p.stat().st_size / 1024:.0f} KB"

    print(f"  · {len(data.get('usAuthorizing', []))} US jurisdictions, "
          f"{len(data.get('international', []))} international regimes inlined")
    print(f"  · dist/standalone.html  {kb(DIST / 'standalone.html')}")
    print(f"  · dist/artifact.html    {kb(DIST / 'artifact.html')}")
    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
