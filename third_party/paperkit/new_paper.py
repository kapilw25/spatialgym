#!/usr/bin/env python3
"""Scaffold a new paper folder under papers/ with the standard layout, a program.md and a README.

Example:
    python3 -m paperkit.new_paper p03-<short-name> "one-line description"
"""
import sys, textwrap
from pathlib import Path

SKEL = ["plans", "generate", "train", "eval", "results/tables", "results/figures", "docs/dashboard", "logs", "scripts"]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    name = sys.argv[1]; desc = sys.argv[2] if len(sys.argv) > 2 else ""
    root = Path(__file__).resolve().parents[2]
    base = root / "papers" / name
    if base.exists():
        sys.exit(f"{base} already exists")
    for d in SKEL:
        (base / d).mkdir(parents=True); (base / d / ".gitkeep").touch()
    (base / "README.md").write_text(f"# {name}\n\n{desc}\n\nStatus: planning. Plans live in [plans/](plans/). Shared tooling comes from [shared/paperkit](../../shared/paperkit/); the public repo is produced by `python3 -m paperkit.export {name}` at submission time.\n")
    tmpl = (root / "papers" / "p01-spatial-vqa" / "program.md").read_text().replace("p01-spatial-vqa", name)
    (base / "program.md").write_text(tmpl)
    print(f"created {base}: {', '.join(SKEL)}, README.md, program.md")


if __name__ == "__main__":
    main()
