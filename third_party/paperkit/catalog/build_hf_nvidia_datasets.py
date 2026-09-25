#!/usr/bin/env python3
"""Build a single hyperlinked table of every Hugging Face dataset matching the
Hub search "nvidia" (https://huggingface.co/datasets?sort=downloads&search=nvidia).

Sources (all public, no token needed):
  1. Hub API   /api/datasets?search=nvidia&sort=downloads  (metadata, tags, license, sizes)
  2. Hub UI    /datasets?p=N&sort=downloads&search=nvidia  (embedded datasetsServerInfo:
               viewer type + numRows exactly as rendered in the listing, incl. gated repos)

Usage:
  python3 d01/literature/scripts/build_hf_nvidia_datasets.py \
      [--out-md d01/literature/notes_01.md] [--out-csv d01/literature/data/hf_nvidia_datasets_<date>.csv] \
      [--cache-dir DIR] [--no-fetch]   # --no-fetch reuses DIR/api.json + DIR/ui.json
"""
import argparse, csv, datetime as dt, html, json, os, re, sys, time, urllib.parse, urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import regen_map as RM  # noqa: E402  curated simulator / generation-library map
import t1_benchmarks as TB  # noqa: E402  papers + public benchmarks (arXiv) for T1 rows

SEARCH = "nvidia"
API = ("https://huggingface.co/api/datasets?search={q}&sort=downloads&direction=-1&limit=1000"
       "&expand[]=author&expand[]=cardData&expand[]=createdAt&expand[]=description&expand[]=downloads"
       "&expand[]=downloadsAllTime&expand[]=gated&expand[]=lastModified&expand[]=likes&expand[]=mainSize"
       "&expand[]=private&expand[]=tags&expand[]=trendingScore")
UI = "https://huggingface.co/datasets?p={p}&sort=downloads&search={q}"
UA = {"User-Agent": "Mozilla/5.0 (research-notes fetcher)"}


def get(url, tries=4, timeout=60):
    for a in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read().decode("utf-8")
        except Exception as e:  # noqa
            err = e
            time.sleep(2 * (a + 1))
    raise RuntimeError(f"failed {url}: {err}")


def fetch_api(q):
    return json.loads(get(API.format(q=urllib.parse.quote(q))))


def fetch_ui(q, n_items):
    pages = list(range(0, (n_items + 29) // 30 + 1))

    def one(p):
        h = get(UI.format(p=p, q=urllib.parse.quote(q)))
        for blk in re.findall(r'data-props="([^"]+)"', h):
            s = html.unescape(blk)
            if s.startswith('{"initialValues"'):
                return json.loads(s)["initialValues"].get("datasets", [])
        return []

    out = {}
    with ThreadPoolExecutor(8) as ex:
        for ds in ex.map(one, pages):
            for d in ds:
                out.setdefault(d["id"], d)
    return out


# ----------------------------------------------------------------------------- taxonomy
# Curated exact assignments for names whose prefix is not self-explanatory (checked
# against the dataset card description). Applied before the ordered regex rules.
EXACT = {
    "SAGE-10k": "PhysicalAI: 3D Scenes & Sim Assets",
    "SPEED-Bench": "LLM Evaluation Benchmarks",
    "HiLiftAeroML": "Domain Data (Sci/Eng/Med/Fin/Legal)",
    "OCR-Synthetic-Multilingual-v1": "Vision, Video & 3D",
    "SOL-ExecBench": "Code & SWE",
    "Granary": "Speech & Audio",
    "earth2studio-assets": "Domain Data (Sci/Eng/Med/Fin/Legal)",
    "When2Call": "Agents & Tool Use",
    "cvdp-benchmark-dataset": "Code & SWE",
    "ProCUA-SFT": "Agents & Tool Use",
    "Lyra-Testing-Example": "Vision, Video & 3D",
    "ToolScale": "Agents & Tool Use",
    "describe-anything-dataset": "Vision, Video & 3D",
    "DLC-Bench": "Vision, Video & 3D",
    "Anchor-Lab": "PhysicalAI: Robotics",
    "OpenH-RF": "Domain Data (Sci/Eng/Med/Fin/Legal)",
    "srp-staging-controlled": "PhysicalAI: 3D Scenes & Sim Assets",
    "simready-dsx": "PhysicalAI: 3D Scenes & Sim Assets",
    "miracl-vision": "QA, Retrieval & RAG",
    "Puzzle-KD-Nemotron-Post-Training-Dataset-v2": "Nemotron: SFT & Post-training",
    "Harmonizer-Dataset": "Vision, Video & 3D",
    "NitroGen": "PhysicalAI: Robotics",
    "esm2_uniref_pretraining_data": "Science",
    "ffs_stereo4d": "Vision, Video & 3D",
    "GEN3C-Testing-Example": "PhysicalAI: World Models & Cosmos",
    "compute-eval": "Code & SWE",
    "Daring-Anteater": "Instruction Following & Alignment",
    "TechQA-RAG-Eval": "QA, Retrieval & RAG",
    "judges-verdict": "QA, Retrieval & RAG",
    "Kimodo-Motion-Gen-Benchmark": "Vision, Video & 3D",
    "LiveCodeBench-CPP": "Code & SWE",
    "aisim-data": "Misc / Internal",
    "aisimulate-fpm-dataset": "Misc / Internal",
    "QCalEval": "Science",
    "ProfBench": "LLM Evaluation Benchmarks",
    "BFCL-Hi": "LLM Evaluation Benchmarks",
    "ChatRAG-Hi": "LLM Evaluation Benchmarks",
    "GSM8K-Hi": "LLM Evaluation Benchmarks",
    "IFEval-Hi": "LLM Evaluation Benchmarks",
    "MT-Bench-Hi": "LLM Evaluation Benchmarks",
    "dynpose-100k": "Vision, Video & 3D",
    "sft_datablend_v1": "Instruction Following & Alignment",
    "form-hoi": "PhysicalAI: Robotics",
    "Spark-AnomalyGen-USD": "PhysicalAI: 3D Scenes & Sim Assets",
    "FinHeadlineMix": "Domain Data (Sci/Eng/Med/Fin/Legal)",
    "SEED-Timeline-Annotations": "Vision, Video & 3D",
    "Linear-Radiation-Transport": "Domain Data (Sci/Eng/Med/Fin/Legal)",
    "cascade": "PhysicalAI: Autonomous Vehicles",
    "Scoring-Verifiers": "LLM Evaluation Benchmarks",
    "Shopify-product-catalogue-8k": "Misc / Internal",
    "R4D-Bench": "Vision, Video & 3D",
    "ORCA-sim-push-cart-gr00t": "PhysicalAI: Robotics",
    "NuRec-AV-Object-Benchmark": "PhysicalAI: Autonomous Vehicles",
    "dextrah_textures": "PhysicalAI: Robotics",
    "X-Mobility": "PhysicalAI: Robotics",
    "PBench": "PhysicalAI: World Models & Cosmos",
    "heb-clip": "Vision, Video & 3D",
    "video-data-augmentation-demo": "PhysicalAI: Smart Spaces & Spatial AI",
    "APE_dataset": "Misc / Internal",
    "llm-robustness-leaderboard-evals": "LLM Evaluation Benchmarks",
    "nvblox": "PhysicalAI: Robotics",
    "omni-dreams-samples": "PhysicalAI: Autonomous Vehicles",
    "omni-dreams-scenes": "PhysicalAI: Autonomous Vehicles",
    "cosmos_data_latent_480p": "PhysicalAI: World Models & Cosmos",
    "nemotron-research-lgt": "Vision, Video & 3D",
    "Nemotron-Research-GooseReason-0.7M": "Nemotron: RL & Reward",
    "PhysicalAI-NuRec-PPISP": "Vision, Video & 3D",
    "Nemotron-RL-litmus-bench-v0.1": "Science",
    "Nemotron-RL-QA-Abstention-v1": "QA, Retrieval & RAG",
    "AudioSkills": "Speech & Audio", "AF-Think": "Speech & Audio", "AF-Chat": "Speech & Audio",
    "LongAudio": "Speech & Audio", "MF-Skills": "Speech & Audio", "hifitts-2": "Speech & Audio",
    "Numb3rs": "Speech & Audio", "Audio2Face-3D-Dataset-v1.0.0-claire": "Speech & Audio",
    "av-skills": "Vision, Video & 3D", "video-full-duplex-benchmark": "Vision, Video & 3D",
    "MMOU": "Vision, Video & 3D", "ChronoEdit-Example-Dataset": "PhysicalAI: World Models & Cosmos",
    "g1_locomanip_dataset": "PhysicalAI: Robotics", "GR00T-N1.7-AppleToPlate": "PhysicalAI: Robotics",
    "RoboCasa-Cosmos-Policy": "PhysicalAI: Robotics", "ALOHA-Cosmos-Policy": "PhysicalAI: Robotics",
    "LIBERO-Cosmos-Policy": "PhysicalAI: Robotics",
    "embed-nemotron-dataset-v1": "QA, Retrieval & RAG", "Retrieval-Synthetic-NVDocs-v1": "QA, Retrieval & RAG",
}

# Ordered (first match wins), case-insensitive, matched against the repo name only.
RULES = [
    ("Safety & Content Moderation", r"Safety|Aegis|VISafe|CantTalkAboutThis|Jailbreak|Prompt-Injection"),
    ("Math & Reasoning", r"Math|IMO-Bench|GSM8K|AceReason|\bMIND\b"),
    ("Code & SWE", r"Code|SWE|CUDA|Competitive-Programming|Verilog|cvdp|ExecBench|coding"),
    ("Science", r"Science|bixbench|esm2"),
    ("Agents & Tool Use", r"Agentic|agent-|Tool|Terminal|NeMo-Gym|BFCL|ProCUA"),
    ("Instruction Following & Alignment",
     r"HelpSteer|Instruction-Following|instruction_following|IFEval|Multichallenge|SysBench|CFBench|Identity-Following|Chat-v"),
    ("QA, Retrieval & RAG", r"ChatQA|ChatRAG|RAG|Retrieval|embed-|knowledge-|Abstention"),
    ("Personas & Privacy (synthetic)", r"Personas|PII|Privasis"),
    ("Speech & Audio", r"Audio|Speech"),
    ("PhysicalAI: Autonomous Vehicles", r"Autonomous-Vehicle|NuRec-AV|AV-Data|LidarGen|Drive"),
    ("PhysicalAI: Robotics",
     r"Robotics|GR00T|Arena-|Cosmos-Policy|LIBERO|libero|BridgeData2|locomanip|PointWorld|DROID|video-to-data|video_to_data|GraspGen|mindmap|Embodiment"),
    ("PhysicalAI: World Models & Cosmos", r"WorldModel|Cosmos|GEN3C|ChronoEdit"),
    ("PhysicalAI: Smart Spaces & Spatial AI", r"SmartSpaces|Spatial|Traffic-Anomaly|VANTAGE|Event-Videos"),
    ("PhysicalAI: 3D Scenes & Sim Assets", r"SimReady|simready|DigitalCousin"),
    ("Vision, Video & 3D", r"vipe|stereo4d|\bOCR\b|VLM|Image|R4D|Video"),
    ("Domain Data (Sci/Eng/Med/Fin/Legal)",
     r"PhysicsNeMo|STRATA|Radiation|aerial-isac|NV-Raw2|SpecializedDomains|Legal|Finance"),
    ("Nemotron: Pretraining", r"Pretraining|Nemotron-CC|Climb"),
    ("Nemotron: RL & Reward", r"-RL-|RLHF|-RM-|RL-data|RL-Training|Cascade-RL|CrossThink|GenRM"),
    ("Nemotron: SFT & Post-training", r"SFT|Post-Training|Cascade"),
    ("LLM Evaluation Benchmarks", r"Bench|Eval|leaderboard"),
]
RULES = [(f, re.compile(p, re.I)) for f, p in RULES]


def family(ds_id, author):
    if author != "nvidia":
        return "3rd-party"
    name = ds_id.split("/", 1)[1]
    if name in EXACT:
        return EXACT[name]
    for fam, rx in RULES:
        if rx.search(name):
            return fam
    return "Misc / Internal"


# ----------------------------------------------------------------------------- formatting
def fmt_num(v):
    """Hub-style compact numbers: 456, 1.07k, 21.4k, 166k, 1.32M, 8.79B."""
    if v is None:
        return ""
    v = float(v)
    for unit, div in (("B", 1e9), ("M", 1e6), ("k", 1e3)):
        if v >= div:
            x = v / div
            s = f"{x:.2f}" if x < 10 else (f"{x:.1f}" if x < 100 else f"{x:.0f}")
            return s.rstrip("0").rstrip(".") + unit
    return f"{int(v)}"


def fmt_bytes(b):
    if not b:
        return ""
    b = float(b)
    for unit, div in (("TB", 1e12), ("GB", 1e9), ("MB", 1e6), ("kB", 1e3)):
        if b >= div:
            x = b / div
            s = f"{x:.2f}" if x < 10 else (f"{x:.1f}" if x < 100 else f"{x:.0f}")
            return s.rstrip("0").rstrip(".") + unit
    return f"{int(b)}B"


def fmt_date(s):
    return s[:10] if s else ""


def license_of(x):
    cd = x.get("cardData") or {}
    lic = cd.get("license")
    if isinstance(lic, list):
        lic = ", ".join(map(str, lic))
    if not lic:
        tags = [t.split(":", 1)[1] for t in x.get("tags", []) if t.startswith("license:")]
        lic = ", ".join(tags)
    if lic == "other" and cd.get("license_name"):
        lic = f"other ({cd['license_name']})"
    return lic or ""


def access_of(g):
    if g in (False, None, "false"):
        return "open"
    return f"gated ({g})"


def md_cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def wrap_tables(lines, open_max_rows=30):
    """Wrap every markdown table in a <details> block so it can be hidden or shown.
    Tables with at most `open_max_rows` data rows start expanded; larger ones start collapsed.
    The summary names the nearest heading above the table and the row count."""
    lines = [x for chunk in lines for x in chunk.split("\n")]  # some entries hold header+separator
    out, i, heading = [], 0, "Table"
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
        if line.startswith("|"):
            j = i
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            block = lines[i:j]
            n_rows = max(0, len(block) - 2)
            state = " open" if n_rows <= open_max_rows else ""
            out.append(f"<details{state}><summary><b>{heading}</b>: {n_rows} rows (click to hide or show)</summary>")
            out.append("")
            out.extend(block)
            out.append("")
            out.append("</details>")
            i = j
            continue
        out.append(line)
        i += 1
    return out


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-dir", default=os.path.expanduser("~/.cache/hf-nvidia-datasets"))
    ap.add_argument("--no-fetch", action="store_true", help="reuse cached api.json / ui.json")
    ap.add_argument("--out-md", default="d01/literature/notes_01.md")
    ap.add_argument("--out-csv", default=None)
    ap.add_argument("--fetched-on", default=dt.date.today().isoformat())
    a = ap.parse_args()
    os.makedirs(a.cache_dir, exist_ok=True)
    api_f, ui_f = os.path.join(a.cache_dir, "api.json"), os.path.join(a.cache_dir, "ui.json")

    if a.no_fetch and os.path.exists(api_f) and os.path.exists(ui_f):
        api, ui = json.load(open(api_f)), json.load(open(ui_f))
    else:
        api = fetch_api(SEARCH)
        json.dump(api, open(api_f, "w"))
        ui = fetch_ui(SEARCH, len(api))
        json.dump(ui, open(ui_f, "w"))
    print(f"api: {len(api)} datasets | ui: {len(ui)} records", file=sys.stderr)

    rows = []
    for rank, x in enumerate(api, 1):
        u = ui.get(x["id"], {})
        dsi = u.get("datasetsServerInfo") or {}
        viewer = dsi.get("viewer", "")
        num_rows = dsi.get("numRows") if viewer in ("viewer", "viewer-partial") else None
        mods = dsi.get("modalities") or [t.split(":", 1)[1] for t in x.get("tags", []) if t.startswith("modality:")]
        tasks = [t.split(":", 1)[1] for t in x.get("tags", []) if t.startswith("task_categories:")]
        arxiv = [t.split(":", 1)[1] for t in x.get("tags", []) if t.startswith("arxiv:")]
        rows.append({
            "rank": rank, "id": x["id"], "url": f"https://huggingface.co/datasets/{x['id']}",
            "author": x.get("author", ""), "nvidia_org": x.get("author") == "nvidia",
            "family": family(x["id"], x.get("author")), "modalities": ", ".join(mods),
            "task_categories": ", ".join(tasks), "license": license_of(x), "gated": x.get("gated"),
            "access": access_of(x.get("gated")), "viewer": viewer, "num_rows": num_rows,
            "main_size_bytes": x.get("mainSize"), "downloads_30d": x.get("downloads"),
            "downloads_all_time": x.get("downloadsAllTime"), "likes": x.get("likes"),
            "trending_score": x.get("trendingScore"), "last_modified": fmt_date(x.get("lastModified")),
            "created_at": fmt_date(x.get("createdAt")), "arxiv": ", ".join(arxiv),
        })
        rg = RM.REGEN.get(x["id"].split("/", 1)[1]) if x.get("author") == "nvidia" else None
        rows[-1].update({
            "regen_tier": rg["tier"] if rg else "", "regen_tool": rg["tool"] if rg else "",
            "regen_tool_url": rg["url"] if rg else "", "regen_status": rg["status"] if rg else "",
            "regen_note": rg["note"] if rg else "",
        })
        tb = TB.ROWS.get(x["id"].split("/", 1)[1]) if rg and rg["tier"] == RM.T1 else None
        rows[-1].update({
            "t1_paper_arxiv": "; ".join(tb["papers"]) if tb else "",
            "t1_benchmark_arxiv": "; ".join(tb["benchmarks"]) if tb else "",
            "t1_benchmark_other": tb["benchmarks_other"] if tb else "",
        })

    # ---- CSV
    if a.out_csv:
        os.makedirs(os.path.dirname(a.out_csv) or ".", exist_ok=True)
        with open(a.out_csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {a.out_csv}", file=sys.stderr)

    # ---- Markdown
    n_nv = sum(r["nvidia_org"] for r in rows)
    n_3p = len(rows) - n_nv
    authors_3p = Counter(r["author"] for r in rows if not r["nvidia_org"])
    fam_stats = defaultdict(lambda: {"n": 0, "dl": 0, "top": None})
    for r in rows:
        s = fam_stats[r["family"]]
        s["n"] += 1
        s["dl"] += r["downloads_30d"] or 0
        if s["top"] is None:
            s["top"] = r
    fam_order = sorted(fam_stats.items(), key=lambda kv: (kv[0] == "3rd-party", -kv[1]["dl"]))

    L = []
    L.append(f"# Hugging Face datasets matching \"{SEARCH}\" (sorted by downloads)\n")
    L.append(f"Source listing: <https://huggingface.co/datasets?p=1&sort=downloads&search={SEARCH}>  ")
    L.append(f"Snapshot: {a.fetched_on}, pulled from the Hub API (`/api/datasets?search={SEARCH}&sort=downloads`) "
             f"plus the listing pages' embedded viewer info (row counts). "
             f"Rebuild with `d01/literature/scripts/build_hf_nvidia_datasets.py`; "
             f"machine-readable copy in `d01/literature/data/`.\n")
    L.append("| Metric | Value |\n|---|---|")
    L.append(f"| Datasets in listing | {len(rows)} |")
    L.append(f"| Published by the `nvidia` org | {n_nv} |")
    L.append(f"| Third-party repos whose name contains \"{SEARCH}\" | {n_3p} (from {len(authors_3p)} accounts) |")
    L.append(f"| With a viewer row count | {sum(1 for r in rows if r['num_rows'] is not None)} |")
    L.append(f"| Gated (auto or manual approval) | {sum(1 for r in rows if r['access'] != 'open')} |")
    L.append("")
    L.append("Column notes: **#** is the position in the downloads-sorted listing (the first 60 rows are the two pages "
             "originally pasted into this file). **Rows** is the dataset-viewer count shown on the Hub card (blank when "
             "the viewer is disabled, gated, or preview-only). **Size** is the repo size on the Hub. **Downloads (30d)** is "
             "the number the Hub sorts by; **all-time** is cumulative. **Family** is a name-pattern grouping of nvidia-org "
             "repos (topic first, then Nemotron training stage); third-party repos are marked `3rd-party`. **Paper** links "
             "the arXiv ids declared on the dataset card.\n")

    L.append("## Families at a glance\n")
    L.append("| Family | Datasets | Downloads (30d, sum) | Most downloaded |\n|---|---:|---:|---|")
    for fam, s in fam_order:
        t = s["top"]
        L.append(f"| {fam} | {s['n']} | {fmt_num(s['dl'])} | [{t['id']}]({t['url']}) |")
    L.append("")
    L.append("Third-party accounts with the most matching repos: " + ", ".join(
        f"`{k}` ({v})" for k, v in authors_3p.most_common(10)) + ".\n")

    # ---- Regenerable datasets (simulators, data-generation libraries)
    rg_rows = [r for r in rows if r["regen_tier"]]
    tier_counts = {t: sum(1 for r in rg_rows if r["regen_tier"] == t) for t in RM.TIER_ORDER}
    L.append("## Regenerable datasets: simulators and data-generation pipelines\n")
    L.append(f"{len(rg_rows)} of the {n_nv} nvidia-org datasets were produced by a simulator, a renderer, or a data-generation "
             "library, or are asset packs meant to be loaded into one. Classification is from each dataset card's own text "
             "(README, or the rendered card for gated repos) on the snapshot date. Third-party repos are not classified. "
             "Real-world captures with only synthetic annotations (e.g. Audio Flamingo QA sets, DROID and BridgeData derivatives, "
             "Cosmos-Reason1 annotations) and human-labeled preference sets (HelpSteer, Aegis) are deliberately left out.\n")
    L.append("| Tier | Meaning | Datasets |\n|---|---|---:|")
    tier_meaning = {
        RM.T1: "Generated or rendered with an NVIDIA simulator or world model (Isaac Sim, Isaac Lab, Isaac Lab-Arena, Omniverse Replicator, NuRec, Cosmos, DriveSim, Video-to-Data)",
        RM.T2: "Generated with a third-party simulator or solver (MuJoCo, RoboCasa, LIBERO, BEHAVIOR, OpenFOAM, KiT-RT, SCREAM, k-Wave, commercial CFD)",
        RM.TA: "Sim-ready asset packs: inputs you load into a simulator, not generated outputs",
        RM.T3: "Generated with an NVIDIA data-generation library or pipeline (NeMo-Skills, NeMo Data Designer, NeMo Curator, NeMo Gym, ViPE, FoundationStereo, Magpie TTS, SAGE, and project pipelines)",
        RM.T4: "Generated with a third-party generation library (Reasoning Gym, SynthDoG)",
        RM.T5: "LLM-synthesized text where the card names the generator model(s) but no generation library is released",
    }
    for t in RM.TIER_ORDER:
        L.append(f"| {t} | {tier_meaning[t]} | {tier_counts[t]} |")
    L.append("")
    L.append("Status column: **Pipeline released** = scripts or configs to regenerate are public; **Public tools, scripts not released** = "
             "the tool is public but NVIDIA's exact generation scripts are not; **NVIDIA-internal tooling** = only partly reproducible; "
             "**NeMo Gym environment** = the prompt set is fixed while rollouts and verification regenerate inside the library; "
             "**Asset pack** = inputs; **Generator model(s) named only** = regenerable in principle by re-prompting the named models.\n")
    L.append("| # | Dataset | Tier | Tool / pipeline | Status | What the card says |")
    L.append("|---:|---|---|---|---|---|")
    order = {t: i for i, t in enumerate(RM.TIER_ORDER)}
    for r in sorted(rg_rows, key=lambda r: (order[r["regen_tier"]], r["rank"])):
        tool = f"[{md_cell(r['regen_tool'])}]({r['regen_tool_url']})" if r["regen_tool_url"] else md_cell(r["regen_tool"])
        L.append("| " + " | ".join([
            str(r["rank"]), f"[{md_cell(r['id'].split('/', 1)[1])}]({r['url']})", r["regen_tier"].split(" ", 1)[0],
            tool, RM.STATUS_LABEL[r["regen_status"]], md_cell(r["regen_note"]),
        ]) + " |")
    L.append("")
    L.append("Not classified because the card is missing or too thin to tell: " + ", ".join(
        f"[{n}](https://huggingface.co/datasets/nvidia/{n})" for n in RM.UNVERIFIED) + ".\n")

    # ---- T1: papers and public benchmarks with arXiv IDs
    def ax(i):
        return f"[{md_cell(TB.PAPERS[i]['short'])} ({i})](https://arxiv.org/abs/{i})"
    t1_rows = sorted((r for r in rows if r["regen_tier"] == RM.T1), key=lambda r: r["rank"])
    L.append("### T1 datasets: papers and public benchmarks (arXiv IDs)\n")
    L.append("Every arXiv ID below was resolved against the arXiv API on the snapshot date (title, first author and date are in the "
             "reference table that follows). **Papers behind the data** are the tool, pipeline or model papers the card cites or the "
             "generator's own report. **Public benchmarks** are evaluation suites the dataset feeds or on which the accompanying paper "
             "reports results; benchmarks without an arXiv ID are named in the Notes column. Rows marked 'no public benchmark named' "
             "are training sets whose cards and papers name no external benchmark.\n")
    L.append("| # | Dataset | Papers behind the data | Public benchmarks | Notes |")
    L.append("|---:|---|---|---|---|")
    for r in t1_rows:
        name = r["id"].split("/", 1)[1]
        tb = TB.ROWS[name]
        bench = ", ".join(ax(i) for i in tb["benchmarks"]) or "no public benchmark named"
        if tb["benchmarks_other"]:
            bench += f"; {md_cell(tb['benchmarks_other'])}"
        L.append("| " + " | ".join([
            str(r["rank"]), f"[{md_cell(name)}]({r['url']})", ", ".join(ax(i) for i in tb["papers"]), bench, md_cell(tb["note"]),
        ]) + " |")
    L.append("")
    L.append("### Domain-wide public benchmarks for simulator-generated Physical AI data\n")
    L.append("| Area | Benchmarks (arXiv) |\n|---|---|")
    for area, ids in TB.DOMAIN:
        L.append(f"| {area} | " + ", ".join(ax(i) for i in ids) + " |")
    L.append("")
    L.append("### arXiv references used in the T1 tables\n")
    L.append("| arXiv | Short name | Title | First author | Date |\n|---|---|---|---|---|")
    for i in sorted(TB.PAPERS, key=lambda k: (k.split(".")[0], k)):
        pmeta = TB.PAPERS[i]
        L.append(f"| [{i}](https://arxiv.org/abs/{i}) | {md_cell(pmeta['short'])} | {md_cell(pmeta['title'])} | {md_cell(pmeta['first_author'])} | {pmeta['date']} |")
    L.append("")

    L.append(f"## All {len(rows)} datasets\n")
    hdr = ["#", "Dataset", "Family", "Modality", "Rows", "Size", "Updated", "Downloads (30d)",
           "Downloads (all-time)", "Likes", "License", "Access", "Paper"]
    L.append("| " + " | ".join(hdr) + " |")
    L.append("|" + "|".join(["---:", "---", "---", "---", "---:", "---:", "---", "---:", "---:", "---:", "---", "---", "---"]) + "|")
    for r in rows:
        paper = " ".join(f"[{p}](https://arxiv.org/abs/{p})" for p in r["arxiv"].split(", ") if p)
        L.append("| " + " | ".join([
            str(r["rank"]), f"[{md_cell(r['id'])}]({r['url']})", md_cell(r["family"]), md_cell(r["modalities"]),
            fmt_num(r["num_rows"]), fmt_bytes(r["main_size_bytes"]), r["last_modified"],
            fmt_num(r["downloads_30d"]), fmt_num(r["downloads_all_time"]), fmt_num(r["likes"]),
            md_cell(r["license"]), r["access"], paper,
        ]) + " |")
    L.append("")
    os.makedirs(os.path.dirname(a.out_md) or ".", exist_ok=True)
    L = wrap_tables(L)
    open(a.out_md, "w").write("\n".join(L))
    print(f"wrote {a.out_md} ({len(rows)} rows)", file=sys.stderr)


if __name__ == "__main__":
    main()
