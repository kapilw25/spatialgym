# program.md for p01-spatial-vqa (owner-edited org code for the improvement loop)

Goal: the pre-registered claims in [plans/](plans/), measured on the DEV split only inside the loop; the test set is scored once per release.

Levers the agent may edit (one file: `generate/gen_config.yaml`): skill mix, camera or scene prior, twin ratio, tolerance bands, difficulty knobs, asset pools, question or task templates.

Frozen: the training recipe (shared with every rival column), the test set, the claims.

Metric: dev accuracy or success on the gap cells, paired bootstrap CI over dev items.

Budget per probe: one generation run of fixed size plus one fixed-step training run.

Verdict: keep only if the CI excludes zero on the gap cells; otherwise discard and run the diagnose loop (research-direction skill) before the next proposal.

Stop rule: OURS beats every rival on the claimed subsets with CI, or two nights keep nothing (then write "dead weight" into the plan).

Log: [results/autoresearch/log.jsonl](results/autoresearch/log.jsonl) and `log.md`, one row per probe.
