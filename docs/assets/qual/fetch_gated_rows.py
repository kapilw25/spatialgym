#!/usr/bin/env python3
"""Fetch 8 verified sample rows each for the two gated rivals once access is granted.

Run from the repo root after (1) requesting access on both dataset pages with your Hugging Face account and
(2) putting a READ token in `.env` as `HF_TOKEN=...` (the file is gitignored). The token is read, never printed.

    python3 papers/p01-spatial-vqa/docs/assets/qual/fetch_gated_rows.py [warehouse500k|spatialqa50k]

Every saved image comes from an HTTP 200 download that PIL opens; provenance_rows.json is rewritten with the rows
(the earlier "gated" status entry is dropped), then rebuild the page with `node shared/docs_builder/build_plan_page.mjs papers/p01-spatial-vqa/docs/page_config.json`.
"""
import io, json, os, re, sys, urllib.parse, urllib.request, urllib.error, zipfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../../../../.."))
TODAY = "2026-09-24"
MAXPX = 1600

def token():
    t = os.environ.get("HF_TOKEN")
    if not t and os.path.exists(os.path.join(ROOT, ".env")):
        for ln in open(os.path.join(ROOT, ".env")):
            m = re.match(r"\s*(?:export\s+)?HF_TOKEN\s*=\s*['\"]?([^'\"\s]+)", ln)
            if m: t = m.group(1)
    if not t:
        sys.exit("HF_TOKEN not found in the environment or in .env at the repo root")
    return t

TOKEN = token()
HDR = {"Authorization": f"Bearer {TOKEN}", "User-Agent": "lab-qual-page/1.0"}

def get(url, rng=None, timeout=120):
    h = dict(HDR)
    if rng: h["Range"] = f"bytes={rng[0]}-{rng[1]}"
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, b"", dict(e.headers or {})

def save_image(data, path):
    im = Image.open(io.BytesIO(data)); im.verify()
    im = Image.open(io.BytesIO(data)); note = None
    if max(im.size) > MAXPX:
        im = im.convert("RGBA" if path.endswith(".png") else "RGB"); im.thumbnail((MAXPX, MAXPX))
        note = f"resized to fit {MAXPX} px on {TODAY}; source bytes at source_url"
    im.save(path, optimize=True) if path.endswith(".png") else im.save(path, quality=88, optimize=True)
    return note

def rows_api(repo, split="train", offset=0, length=20, config="default"):
    q = urllib.parse.quote(repo, safe="")
    url = f"https://datasets-server.huggingface.co/rows?dataset={q}&config={config}&split={split}&offset={offset}&length={length}"
    st, body, _ = get(url)
    print(f"  rows API {st}: {url}")
    return (json.loads(body) if st == 200 else None), url

def first_turns(conv):
    q = next((c.get("value", "") for c in conv if c.get("from") == "human"), "")
    a = next((c.get("value", "") for c in conv if c.get("from") == "gpt"), "")
    return q, a

class HttpFile(io.RawIOBase):
    """Range-request backed read-only file, so zipfile can pull single members out of a remote zip."""
    def __init__(self, url):
        self.url = url; self.pos = 0
        st, _, h = get(url, rng=(0, 0))
        if st not in (200, 206): raise RuntimeError(f"HTTP {st} for {url}")
        cr = h.get("Content-Range") or h.get("content-range") or ""
        self.size = int(cr.split("/")[-1]) if "/" in cr else int(h.get("Content-Length", "0"))
    def readable(self): return True
    def seekable(self): return True
    def seek(self, off, whence=io.SEEK_SET):
        self.pos = {io.SEEK_SET: off, io.SEEK_CUR: self.pos + off, io.SEEK_END: self.size + off}[whence]; return self.pos
    def tell(self): return self.pos
    def read(self, n=-1):
        if n is None or n < 0: n = self.size - self.pos
        if n <= 0: return b""
        st, body, _ = get(self.url, rng=(self.pos, self.pos + n - 1))
        if st not in (200, 206): raise RuntimeError(f"HTTP {st} reading {self.url}")
        self.pos += len(body); return body
    def readinto(self, b):
        data = self.read(len(b)); b[:len(data)] = data; return len(data)

# ---------------------------------------------------------------- warehouse500k
def warehouse():
    repo = "nvidia/PhysicalAI-Spatial-Intelligence-Warehouse"; folder = os.path.join(HERE, "warehouse500k"); os.makedirs(folder, exist_ok=True)
    out = []
    data, url = rows_api(repo)
    if data and data.get("rows"):
        for r in data["rows"][:8]:
            row = r["row"]; idx = r["row_idx"]
            img = next((v for v in row.values() if isinstance(v, dict) and v.get("src")), None)
            conv = row.get("conversations") or []
            q, a = first_turns(conv) if conv else (json.dumps({k: v for k, v in row.items() if not isinstance(v, dict)})[:300], "")
            fn = None
            if img:
                st, body, _ = get(img["src"])
                if st == 200:
                    fn = f"row_{idx}.png"; note = save_image(body, os.path.join(folder, fn))
            out.append({"file": fn, "media": "image" if fn else "annotation-only", "source_url": img["src"] if img else url, "dataset": repo,
                        "config": "default", "split": "train", "row_index": idx, "question": q[:300], "answer": str(row.get("normalized_answer", a))[:120],
                        "question_type": row.get("category"), "licence": "cc-by-4.0", "fetched_on": TODAY})
    else:
        base = f"https://huggingface.co/datasets/{repo}/resolve/main/train_sample/"
        st, body, _ = get(base + "train_sample.json")
        print(f"  train_sample.json {st}")
        if st != 200: sys.exit("  still no access: request it on the dataset page and wait for the approval mail")
        items = json.loads(body)
        per_cat, chosen = {}, []
        for i, it in enumerate(items):                       # two items per category, in file order
            c = it.get("category") or "?"
            if per_cat.get(c, 0) < 2: per_cat[c] = per_cat.get(c, 0) + 1; chosen.append((i, it))
            if len(chosen) >= 8 and len(per_cat) >= 4: break
        print(f"  categories in train_sample.json: {sorted({it.get('category') for it in items})}; chosen {per_cat}")
        for i, it in chosen[:8]:
            q, a = first_turns(it.get("conversations", []))
            img_rel = it.get("image") or ""
            img_url = base + "images/" + os.path.basename(img_rel)
            st2, data2, _ = get(img_url); fn = None; note = None
            if st2 == 200:
                fn = f"row_{i}.jpg"; note = (save_image(data2, os.path.join(folder, fn)) or "") + "; PNG re-encoded as JPEG q88 for the page"
                note = note.lstrip("; ")
            print(f"  image {st2}: {img_url}")
            e = {"file": fn, "media": "image" if fn else "annotation-only", "source_url": img_url, "dataset": repo, "config": "train_sample",
                 "split": "train_sample", "row_index": i, "question": q[:300], "answer": str(it.get("normalized_answer", a))[:120],
                 "question_type": it.get("category"), "licence": "cc-by-4.0", "fetched_on": TODAY}
            if note: e["local_processing"] = note
            out.append(e)
    return folder, out

# ---------------------------------------------------------------- spatialqa50k
def spatialqa():
    repo = "RussRobin/SpatialQA"; folder = os.path.join(HERE, "spatialqa50k"); os.makedirs(folder, exist_ok=True)
    out = []
    data, url = rows_api(repo)
    if data and data.get("rows"):
        for r in data["rows"][:8]:
            row = r["row"]; idx = r["row_idx"]
            img = next((v for v in row.values() if isinstance(v, dict) and v.get("src")), None)
            q, a = first_turns(row.get("conversations") or [])
            fn = None
            if img:
                st, body, _ = get(img["src"])
                if st == 200: fn = f"row_{idx}.jpg"; save_image(body, os.path.join(folder, fn))
            out.append({"file": fn, "media": "image" if fn else "annotation-only", "source_url": img["src"] if img else url, "dataset": repo,
                        "config": "default", "split": "train", "row_index": idx, "question": q[:300], "answer": a[:120], "question_type": None,
                        "licence": "cc-by-4.0", "fetched_on": TODAY})
        return folder, out
    # no viewer: read the head of SpatialQA.json (a JSON list in LLaVA format) and pull images out of the depth zips by range requests
    base = f"https://huggingface.co/datasets/{repo}/resolve/main/"
    st, body, _ = get(base + "SpatialQA.json", rng=(0, 4_000_000))
    print(f"  SpatialQA.json head {st}")
    if st not in (200, 206): sys.exit("  still no access: request it on the dataset page and wait for the approval mail")
    text = body.decode("utf-8", "ignore")
    # cut at the last complete top-level object
    depth = 0; last = 0
    for i, ch in enumerate(text):
        if ch == "{": depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0: last = i
    items = json.loads("[" + text[text.index("{"): last + 1] + "]")   # the complete leading objects of the list
    zips = {}
    ZIPMAP = {"2d3ds": "2d3ds.zip", "kitti": "kitti.zip", "nyudepthv2": "nyudepthv2.zip", "nyudepthv2_d": "nyudepthv2_d.zip"}
    def zip_for(img_path):
        top = img_path.split("/")[0]
        cand = ZIPMAP.get(top)
        if not cand: return None, None
        if cand not in zips:
            try: zips[cand] = zipfile.ZipFile(HttpFile(base + cand))
            except Exception as e: print(f"  zip {cand}: {e}"); zips[cand] = None
        return zips[cand], cand
    # pick: up to 4 items with 2d3ds RGB, up to 2 with nyudepthv2 RGB (+ depth), plus 2 text-only from the Bunny-hosted sources
    quota = {"2d3ds": 4, "nyudepthv2": 2, "text": 2}; picked = []
    for i, it in enumerate(items):
        ims = it.get("image"); ims = ims if isinstance(ims, list) else ([ims] if ims else [])
        top = str(ims[0]).split("/")[0] if ims else "None"
        key = top if top in ("2d3ds", "nyudepthv2") else "text"
        if key == "text" and top not in ("visual_genome", "coco_2017"): continue
        if key == "text" and not (len(ims) == 2 or " A. " in (it.get("conversations") or [{}])[0].get("value", "")): continue
        if quota[key] > 0: quota[key] -= 1; picked.append((i, it, ims, key))
        if sum(quota.values()) == 0: break
    print(f"  picked {len(picked)} entries from {len(items)} in the head")
    for i, it, ims, key in picked:
        q, a = first_turns(it.get("conversations", []))
        img_rel = ims[0] if ims else ""; fn = None; src = base + "SpatialQA.json"; depth_fn = None
        if key != "text":
            z, zname = zip_for(img_rel)
            if z:
                names = [m for m in z.namelist() if m.endswith(os.path.basename(img_rel))]
                if names:
                    data2 = z.read(names[0]); fn = f"row_{i}{os.path.splitext(names[0])[1] or '.jpg'}"
                    try: save_image(data2, os.path.join(folder, fn)); src = f"{base}{zname} member {names[0]}"
                    except Exception as e: print(f"  bad image {names[0]}: {e}"); fn = None
            if fn and len(ims) > 1 and str(ims[1]).split("/")[0] in ZIPMAP:       # matching depth map
                zd, zdname = zip_for(ims[1])
                if zd:
                    dn = [m for m in zd.namelist() if m.endswith(os.path.basename(ims[1]))]
                    if dn:
                        try:
                            depth_fn = f"row_{i}_depth{os.path.splitext(dn[0])[1] or '.png'}"; save_image(zd.read(dn[0]), os.path.join(folder, depth_fn))
                        except Exception as e: print(f"  bad depth {dn[0]}: {e}"); depth_fn = None
            print(f"  {i}: {img_rel} -> {fn} {depth_fn or ''}")
        e = {"file": fn, "media": "image" if fn else "annotation-only", "source_url": src, "dataset": repo, "config": "SpatialQA.json head",
             "split": "train", "row_index": i, "question": q[:300], "answer": a[:120], "question_type": img_rel.split("/")[0] or None,
             "licence": "cc-by-4.0", "fetched_on": TODAY, "image_paths": ims, "depth_file": depth_fn,
             "note": None if fn else "image hosted in BoyaWu10/Bunny-v1_0-data (low and middle level sources), not in this repo"}
        out.append({k: v for k, v in e.items() if v is not None})
    return folder, out

if __name__ == "__main__":
    which = sys.argv[1:] or ["warehouse500k", "spatialqa50k"]
    for w in which:
        print(f"== {w}")
        folder, rows = warehouse() if w == "warehouse500k" else spatialqa()
        if rows:
            json.dump(rows, open(os.path.join(folder, "provenance_rows.json"), "w"), indent=1, ensure_ascii=False)
            print(f"  wrote {len(rows)} rows, {sum(1 for r in rows if r.get('file'))} with images -> {folder}/provenance_rows.json")
    print("now run: node shared/docs_builder/build_plan_page.mjs papers/p01-spatial-vqa/docs/page_config.json")
