#!/usr/bin/env python3
"""Keep-or-discard loop over a generator config, autoresearch style, with the recipe frozen.

One probe = (1) generate a fixed-size batch from `gen_config.yaml`, (2) train under the frozen recipe for fixed steps,
(3) score the DEV split, (4) keep the config if the paired bootstrap CI of (probe - incumbent) on the gap cells excludes zero,
else discard. The three commands are pluggable so any paper folder can reuse the loop. The test set is never touched here.

Example:
    python3 -m paperkit.autoresearch.loop --paper papers/p01-spatial-vqa \
        --generate "python3 generate/run.py --config {config} --out {batch}" \
        --train    "python3 train/run.py --data {batch} --out {ckpt}" \
        --score    "python3 eval/dev.py --ckpt {ckpt} --out {scores}"
"""
import argparse, json, random, shutil, subprocess, time
from pathlib import Path


def paired_ci(a, b, iters=2000, seed=0):
    """95% bootstrap CI of mean(a - b) over paired per-item scores."""
    rng = random.Random(seed); d = [x - y for x, y in zip(a, b)]; n = len(d)
    if n == 0:
        return (0.0, 0.0)
    means = sorted(sum(rng.choice(d) for _ in range(n)) / n for _ in range(iters))
    return (means[int(0.025 * iters)], means[int(0.975 * iters)])


def run(cmd, **kw):
    cmd = cmd.format(**kw); t = time.time()
    r = subprocess.run(cmd, shell=True)
    return r.returncode, time.time() - t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", required=True)
    ap.add_argument("--generate", required=True); ap.add_argument("--train", required=True); ap.add_argument("--score", required=True)
    ap.add_argument("--config", default="generate/gen_config.yaml")
    ap.add_argument("--probe-id", default=time.strftime("p%Y%m%d_%H%M"))
    a = ap.parse_args()
    paper = Path(a.paper); res = paper / "results" / "autoresearch"; res.mkdir(parents=True, exist_ok=True)
    batch, ckpt, scores = res / f"{a.probe_id}_batch", res / f"{a.probe_id}_ckpt", res / f"{a.probe_id}_scores.json"
    inc = res / "incumbent_scores.json"
    for name, cmd, kw in (("generate", a.generate, dict(config=paper / a.config, batch=batch)),
                          ("train", a.train, dict(batch=batch, ckpt=ckpt)),
                          ("score", a.score, dict(ckpt=ckpt, scores=scores))):
        rc, secs = run(cmd, **kw)
        if rc:
            (res / "log.jsonl").open("a").write(json.dumps({"probe": a.probe_id, "stage": name, "rc": rc, "secs": round(secs)}) + "\n")
            raise SystemExit(f"{name} failed with rc={rc}")
    probe = json.loads(scores.read_text())          # {"items": [{"id":..., "score":...}], "gap_cells": [...]}
    verdict, lo, hi = "keep (first incumbent)", 0.0, 0.0
    if inc.exists():
        base = {x["id"]: x["score"] for x in json.loads(inc.read_text())["items"]}
        pairs = [(x["score"], base[x["id"]]) for x in probe["items"] if x["id"] in base]
        lo, hi = paired_ci([p for p, _ in pairs], [q for _, q in pairs])
        verdict = "keep" if lo > 0 else "discard"
    if verdict.startswith("keep"):
        shutil.copy(scores, inc); shutil.copy(paper / a.config, res / "incumbent_gen_config.yaml")
    row = {"probe": a.probe_id, "verdict": verdict, "ci": [round(lo, 4), round(hi, 4)], "n_items": len(probe["items"])}
    (res / "log.jsonl").open("a").write(json.dumps(row) + "\n")
    print(row)


if __name__ == "__main__":
    main()
