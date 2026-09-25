#!/usr/bin/env python3
"""Export one paper folder into a standalone public repo directory.

Copies papers/<name>, vendors shared/paperkit and shared/docs_builder at the current commit under third_party/, drops logs and
checkpoints, rewrites links that point outside the paper (into the private lab repo) to plain text, strips third-party figures
that carry no permissive licence from docs/assets/qual (dataset rows stay), rebuilds the docs page with the vendored builder,
runs the PII name gate and the markdown table gate, and writes RELEASE.md with the pinned commit and the list of stripped files.
Nothing is pushed; the owner creates the GitHub repo and pushes.

Example:
    python3 -m paperkit.export p01-spatial-vqa --out ../exports/spatialgym --names "name1,name2"
"""
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path

DROP = {"logs", ".runbook_done", "__pycache__", ".DS_Store"}
PERMISSIVE = ("cc-by", "cc by", "apache", "mit", "openmdw", "cc0", "bsd")
PRIVATE_LINK = re.compile(r"!?\[([^\]]+)\]\((?:\.\./){2,}[^)]*\)")   # two or more ../ leave the paper folder: private lab material


def permissive(licence):
    return bool(licence) and any(k in str(licence).lower() for k in PERMISSIVE)


def is_figure_like(entry, from_figs):
    if from_figs:
        return True
    return entry.get("row_index") == -1 or (entry.get("media") == "image" and not (entry.get("question") or entry.get("instruction")))


def strip_figures(out):
    """Third-party figures without a permissive licence leave the public release; provenance keeps the pointer."""
    stripped = []
    for prov in out.glob("docs/assets/qual/*/provenance_*.json"):
        entries = json.loads(prov.read_text())
        from_figs = prov.name == "provenance_figs.json"
        for e in entries:
            if not e.get("file") or not is_figure_like(e, from_figs) or permissive(e.get("licence")):
                continue
            f = prov.parent / e["file"]
            if f.exists():
                f.unlink()
            stripped.append(f"{prov.parent.name}/{e['file']} (source: {e.get('source_url') or e.get('paper_url')})")
            e["stripped"] = "removed from the public release: no permissive licence recorded; see source_url"
            e["file"] = None
        prov.write_text(json.dumps(entries, indent=1, ensure_ascii=False))
    return stripped


def rewrite_private_links(out):
    """Markdown links into the lab repo become plain text marked private."""
    n = 0
    for md in out.rglob("*.md"):
        text = md.read_text()
        new, k = PRIVATE_LINK.subn(r"\1 (lab notes, private)", text)
        if k:
            md.write_text(new); n += k
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paper")
    ap.add_argument("--out", required=True)
    ap.add_argument("--names", default="", help="comma-separated personal names the PII gate must not find")
    a = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    src, out = root / "papers" / a.paper, Path(a.out).resolve()
    if not src.exists():
        sys.exit(f"no such paper folder: {src}")
    if out.exists():
        sys.exit(f"refusing to overwrite {out}")
    ignore = lambda d, names: [n for n in names if n in DROP or n.endswith(".ckpt") or n.endswith(".safetensors")]
    shutil.copytree(src, out, ignore=ignore)
    shutil.copytree(root / "shared" / "paperkit", out / "third_party" / "paperkit", ignore=ignore)
    shutil.copytree(root / "shared" / "docs_builder", out / "third_party" / "docs_builder", ignore=ignore)
    (out / ".gitignore").write_text("logs/\n__pycache__/\n.DS_Store\n.env\n*.ckpt\n*.safetensors\n")
    sha = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    links = rewrite_private_links(out)
    stripped = strip_figures(out)
    rebuilt = "not rebuilt (node missing)"
    if shutil.which("node") and (out / "docs" / "page_config.json").exists():
        r = subprocess.run(["node", "third_party/docs_builder/build_plan_page.mjs", "docs/page_config.json"], cwd=out, capture_output=True, text=True)
        rebuilt = r.stdout.strip() if r.returncode == 0 else f"rebuild failed: {r.stderr.strip()[:200]}"
    (out / "RELEASE.md").write_text(
        f"# Release\n\nExported from the lab repo at commit `{sha}`; shared tooling vendored under [third_party/paperkit](third_party/paperkit) and "
        f"[third_party/docs_builder](third_party/docs_builder) at the same commit. Rebuild the docs page with:\n\n"
        f"```\nnode third_party/docs_builder/build_plan_page.mjs docs/page_config.json\n```\n\n"
        f"- {links} link(s) into private lab notes were rewritten to plain text.\n"
        f"- Third-party figures without a permissive licence were removed from [docs/assets/qual](docs/assets/qual); their provenance entries keep the "
        f"source pointer. Dataset rows under their own licences stay, with provenance.\n"
        + ("".join(f"  - {s}\n" for s in stripped) if stripped else "  - none\n")
        + f"- Docs page: {rebuilt}\n")
    problems = []
    if a.names:
        rx = re.compile(r"\b(" + "|".join(map(re.escape, a.names.split(","))) + r")\b", re.I)
        for p in out.rglob("*"):
            if p.is_file() and p.suffix in {".md", ".py", ".sh", ".json", ".yaml", ".html", ".txt"}:
                for i, l in enumerate(p.read_text(errors="replace").splitlines(), 1):
                    if rx.search(l):
                        problems.append(f"PII: {p.relative_to(out)}:{i}: {l.strip()[:80]}")
    gate = root / ".claude" / "skills" / "md-tables" / "check_md_tables.py"
    mds = [str(p) for p in out.rglob("*.md") if "third_party" not in p.parts]
    if gate.exists() and mds:
        r = subprocess.run([sys.executable, str(gate), *mds], capture_output=True, text=True, cwd=out)
        if r.returncode:
            problems.extend(l for l in r.stdout.splitlines() if l.startswith("FAIL"))
    for p in problems:
        print(p)
    if problems:
        print(f"export written to {out} but {len(problems)} gate problem(s) above must be fixed before pushing")
        sys.exit(1)
    print(f"export OK: {out} (pinned {sha}); {links} private links rewritten, {len(stripped)} figure(s) stripped, {rebuilt}")
    print("next: create the GitHub repo, then `git init && git add -A && git commit` inside the export and push it yourself")


if __name__ == "__main__":
    main()
