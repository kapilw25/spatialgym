// Generic plan page builder: one tabbed HTML page per paper from its plan markdown plus a qualitative grid of verified rival samples.
// Usage: node shared/docs_builder/build_plan_page.mjs papers/<paper>/docs/page_config.json
// Config keys: plan (md path), out (html path), title, qual_dir (assets/qual), labels ([[headingStartsWith, "emoji label"], ...]),
//              rivals ([{key, name, pics, size, paper, card, note}]), ours ({title, meta, cells:[{icon,title,text}], note}), lede.
// No runtime dependencies: marked.js is vendored beside this script; the output HTML is self-contained.
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const markedMod = require(path.join(here, "vendor/marked.min.js"));
const marked = markedMod.marked || markedMod;
marked.setOptions({ gfm: true, breaks: false });

const cfgPath = process.argv[2];
if (!cfgPath) { console.error("usage: node build_plan_page.mjs <page_config.json>"); process.exit(1); }
const cfgDir = path.dirname(path.resolve(cfgPath));
const cfg = JSON.parse(fs.readFileSync(cfgPath, "utf8"));
const rel = p => path.resolve(cfgDir, p);
const PLAN = rel(cfg.plan), OUT = rel(cfg.out), QUAL = rel(cfg.qual_dir || "assets/qual");
const BUILT = new Date().toISOString().slice(0, 10);
const esc = s => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
function readJson(p) { try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return null; } }

// ---------- split the markdown ----------
const md = fs.readFileSync(PLAN, "utf8");
const sections = []; let pre = []; let cur = null;
for (const ln of md.split("\n")) {
  const m = /^## (.+)$/.exec(ln);
  if (m) { cur = { heading: m[1].trim(), body: [] }; sections.push(cur); continue; }
  if (cur) cur.body.push(ln); else pre.push(ln);
}
// a "## 🔔 ..." section is the decisions log: it feeds the notification drawer, not a tab
const logIdx = sections.findIndex(s => s.heading.startsWith("🔔"));
const LOG = [];
if (logIdx >= 0) {
  for (const ln of sections[logIdx].body) {
    const m = /^- (\S+) · (.+)$/.exec(ln.trim()); if (!m) continue;
    LOG.push({ date: m[1], open: m[1] === "open", html: marked.parseInline(m[2]) });
  }
  sections.splice(logIdx, 1);
}
const mdTitle = (pre.find(l => l.startsWith("# ")) || "# Plan").slice(2).trim();
const title = cfg.title || mdTitle;
const preHtml = marked.parse(pre.filter(l => !l.startsWith("# ")).join("\n"));
function label(heading) {
  const bare = heading.replace(/^\S+\s*/, "");
  for (const [start, lab] of cfg.labels || []) if (heading.startsWith(start) || bare.startsWith(start)) return lab;
  const em = heading.startsWith("🗺️") ? "🗺️" : [...heading][0];
  return `${em} ${bare.split(/[:,(]/)[0].split(" ").slice(0, 3).join(" ")}`;
}

// ---------- qualitative tab ----------
function qualCard(r) {
  const dir = path.join(QUAL, r.key);
  const rows = readJson(path.join(dir, "provenance_rows.json")) || [];
  const figs = readJson(path.join(dir, "provenance_figs.json")) || [];
  const items = [];
  const rowCap = x => [x.question || x.instruction, x.answer ? `A: ${x.answer}` : ""].filter(Boolean).join(" ");
  const rowProv = x => [x.dataset, x.split, x.row_index != null ? `row ${x.row_index}` : "", x.episode != null ? `episode ${x.episode}` : "",
    x.frame_time_s != null ? `t=${x.frame_time_s}s` : "", x.camera].filter(Boolean).join(" ");
  for (const x of rows) {
    if (x.depth_file && !fs.existsSync(path.join(dir, x.depth_file))) x.depth_file = null;
    if (x.masked_file && !fs.existsSync(path.join(dir, x.masked_file))) x.masked_file = null;
    if (x.row_index === -1 && x.file && fs.existsSync(path.join(dir, x.file)))
      items.push({ src: `${cfg.qual_dir || "assets/qual"}/${r.key}/${x.file}`, kind: "figure", cap: x.question || x.note || "dataset card figure", prov: `${x.dataset || ""} dataset card`, url: x.source_url });
    else if (x.row_index === -1) continue;
    else if (x.file && fs.existsSync(path.join(dir, x.file)) && !rowCap(x))   // a card or page figure saved by the rows pass: caption from its note
      items.push({ src: `${cfg.qual_dir || "assets/qual"}/${r.key}/${x.file}`, kind: "figure", cap: x.note || "figure", prov: `${x.dataset || ""} card or page figure`, url: x.source_url });
    else if (x.file && fs.existsSync(path.join(dir, x.file)))
      items.push({ src: `${cfg.qual_dir || "assets/qual"}/${r.key}/${x.masked_file || x.file}`, orig: x.masked_file ? `${cfg.qual_dir || "assets/qual"}/${r.key}/${x.file}` : null,
        depth: x.depth_file ? `${cfg.qual_dir || "assets/qual"}/${r.key}/${x.depth_file}` : null, kind: "row", cap: rowCap(x), prov: rowProv(x), url: x.source_url,
        type: x.question_type || x.robot, masked: !!x.masked_file });
    else if (!x.file && (x.question || x.instruction))
      items.push({ src: null, kind: x.media === "annotation-only" ? "annotation-only" : "video", cap: rowCap(x), prov: rowProv(x), url: x.source_url, type: x.question_type || x.robot });
  }
  for (const x of figs) if (x.file && fs.existsSync(path.join(dir, x.file)))
    items.push({ src: `${cfg.qual_dir || "assets/qual"}/${r.key}/${x.file}`, kind: "figure", cap: x.caption || "", prov: `${x.paper || ""} ${x.figure || ""}`.trim(), url: x.paper_url || x.source_url });
  const gated = rows.some(x => x.gated && !x.file);
  const cells = items.length ? items.map(it => `
      <figure class="q ${it.kind}">
        ${it.src ? `<div class="${it.depth ? "pair" : ""}"><a href="${esc(it.src)}" target="_blank" rel="noopener"><img loading="lazy" src="${esc(it.src)}" alt=""></a>${it.depth ? `<a href="${esc(it.depth)}" target="_blank" rel="noopener"><img loading="lazy" src="${esc(it.depth)}" alt="depth map"></a><span class="dtag">RGB + depth</span>` : ""}${it.masked ? `<span class="dtag">regions drawn · <a href="${esc(it.orig)}" target="_blank" rel="noopener">original</a></span>` : ""}</div>`
                 : `<div class="nomedia">${it.kind === "video" ? "🎬 frames inside the archive, not downloaded" : "🧾 text only: the image is hosted outside this repo (see the note above)"}</div>`}
        <figcaption>${it.type ? `<span class="tag">${esc(it.type)}</span> ` : ""}${esc(it.cap).slice(0, 220)}
          <div class="prov">${it.kind === "figure" ? (String(it.prov).includes("card") || String(it.prov).includes("README") ? "🖼️ card or README figure" : "📄 paper figure") : "🗃️ dataset row"} · ${esc(it.prov)}${it.url ? ` · <a href="${esc(it.url)}" target="_blank" rel="noopener">source</a>` : ""}</div>
        </figcaption>
      </figure>`).join("") : `<div class="empty">${gated ? "🔒 gated on Hugging Face; no viewer rows. Paper figures only, if any were found." : "⏳ no verified samples fetched yet"}</div>`;
  return `
  <section class="rival">
    <h3>🥊 ${esc(r.name)} <small>${esc(r.pics)} · ${esc(r.size)} · <a href="${r.paper}" target="_blank" rel="noopener">paper</a>${r.card ? ` · <a href="${r.card}" target="_blank" rel="noopener">card</a>` : ""}</small></h3>
    ${r.note ? `<p class="note">${esc(r.note)}</p>` : ""}
    <div class="qgrid">${cells}</div>
  </section>`;
}
const O = cfg.ours || { title: "OURS", meta: "planned", cells: [] };
const oursHtml = `
  <section class="rival ours">
    <h3>🏁 ${esc(O.title || "OURS")} <small>${esc(O.meta || "")}</small></h3>
    <div class="qgrid">${(O.cells || []).map(c => `
      <figure class="q blank">
        <div class="ph"><span class="ico">${c.icon}</span><span class="planned">planned</span></div>
        <figcaption><b>${esc(c.title)}</b> ${esc(c.text)}</figcaption>
      </figure>`).join("")}
    </div>
    ${O.note ? `<p class="note">${O.note}</p>` : ""}
  </section>`;
const qualHtml = `
  <p class="lede">${cfg.lede || "What each training set actually looks like, from verified samples only: 🗃️ rows pulled from the Hugging Face viewer API or the repos' own files and 📄 example figures from the arXiv HTML of each paper, each with its source. Nothing here is generated or described from memory; a dataset with no verified sample says so."} Fetched ${BUILT}.</p>
  ${(cfg.rivals || []).map(qualCard).join("\n")}
  ${oursHtml}
  <p class="note">Provenance files: <code>${esc(cfg.qual_dir || "assets/qual")}/&lt;rival&gt;/provenance_rows.json</code>, <code>provenance_figs.json</code>; reports: <code>ROWS_REPORT.md</code>, <code>FIGS_REPORT.md</code> in the same folder. Images are reproduced for research comparison; each dataset keeps its own licence.</p>`;

// ---------- assemble: flat tabs, or a nested tree when cfg.nav is given ----------
const leafTabs = [{ id: "qualitative", label: "🔍 Qualitative", html: qualHtml, heading: "qualitative" }]
  .concat(sections.map(s => ({ id: slug(label(s.heading).replace(/^\S+\s*/, "")), label: label(s.heading), heading: s.heading, html: `<h2>${esc(s.heading)}</h2>` + marked.parse(s.body.join("\n")) })));
const findLeaf = start => start === "qualitative" ? leafTabs[0]
  : leafTabs.find(t => t.heading !== "qualitative" && (t.heading.startsWith(start) || t.heading.replace(/^\S+\s*/, "").startsWith(start)));
let navHtml = "", panelsHtml = "", treeJson = "[]";
if (cfg.nav) {
  const nodes = []; const used = new Set();
  function build(node, parent, depth) {
    const own = node.section ? findLeaf(node.section) : null;
    if (node.section && !own) console.warn(`nav: no section starts with "${node.section}"`);
    const id = own ? own.id : slug(node.label.replace(/^\S+\s*/, ""));
    const n = { id, label: node.label, parent, depth, children: [], leaf: null };
    nodes.push(n);
    if (node.children && node.children.length) {
      if (own) { used.add(own.id); n.children.push({ id: own.id + "-overview", label: node.label.replace(/^(\S+\s*)/, "$1") + " (overview)", parent: id, depth: depth + 1, children: [], leaf: own }); nodes.push(n.children[0]); }
      for (const c of node.children) n.children.push(build(c, id, depth + 1));
    } else if (own) { used.add(own.id); n.leaf = own; }
    return n;
  }
  const tops = cfg.nav.map(t => build(t, null, 0));
  // any section left out of the tree lands in the last top tab
  for (const t of leafTabs) if (!used.has(t.id)) { const n = { id: t.id, label: t.label, parent: tops[tops.length - 1].id, depth: 1, children: [], leaf: t }; tops[tops.length - 1].children.push(n); nodes.push(n); }
  const firstLeaf = n => n.leaf ? n : firstLeaf(n.children[0]);
  const bar = (items, cls, parentId) => `<nav class="tabs ${cls}"${parentId ? ` data-parent="${parentId}"` : ""} role="tablist">${items.map(n => `<button role="tab" data-node="${n.id}" data-leaf="${firstLeaf(n).id}" aria-selected="false">${esc(n.label)}</button>`).join("")}</nav>`;
  navHtml = bar(tops, "lvl1") + nodes.filter(n => n.children.length).map(n => bar(n.children, n.depth === 0 ? "lvl2" : "lvl3", n.id)).join("");
  panelsHtml = nodes.filter(n => n.leaf).map(n => `<section class="panel" id="tab-${n.id}" role="tabpanel">${n.leaf.html}</section>`).join("\n");
  treeJson = JSON.stringify(nodes.map(n => ({ id: n.id, parent: n.parent, leaf: !!n.leaf })));
} else {
  navHtml = `<nav class="tabs lvl1" role="tablist">${leafTabs.map(t => `<button role="tab" data-node="${t.id}" data-leaf="${t.id}" aria-selected="false">${esc(t.label)}</button>`).join("")}</nav>`;
  panelsHtml = leafTabs.map(t => `<section class="panel" id="tab-${t.id}" role="tabpanel">${t.html}</section>`).join("\n");
  treeJson = JSON.stringify(leafTabs.map(t => ({ id: t.id, parent: null, leaf: true })));
}
const css = fs.readFileSync(path.join(here, "page.css"), "utf8");
const js = fs.readFileSync(path.join(here, "page.js"), "utf8");
const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title><style>${css}</style></head>
<body><div class="wrap">
<header>${LOG.length ? `<button class="bell" id="bell" aria-label="decisions log" aria-expanded="false">🔔<span class="badge" id="badge" hidden></span></button>
<div class="drawer" id="drawer" hidden><div class="dhead"><b>🔔 Decisions log</b><span class="muted" id="dcount"></span></div>
<ol class="dlist">${LOG.filter(e => e.open).concat(LOG.filter(e => !e.open)).map(e => `<li data-date="${esc(e.date)}"><span class="when">${e.open ? "open" : esc(e.date)}</span><div>${e.html}</div></li>`).join("")}</ol></div>` : ""}
<h1>${esc(mdTitle)}</h1><div class="pre">${preHtml}</div></header>
<div class="navs">${navHtml}</div>
${panelsHtml}
<footer>Built ${BUILT} from <a href="${esc(path.relative(path.dirname(OUT), PLAN))}">${esc(path.relative(cfgDir, PLAN))}</a> by <code>shared/docs_builder/build_plan_page.mjs</code> with <code>${esc(path.basename(cfgPath))}</code>. Rebuild after editing the plan.</footer>
</div><script>const TREE=${treeJson};const LOG_DATES=${JSON.stringify(LOG.map(e => e.date))};\n${js}</script></body></html>`;
fs.writeFileSync(OUT, html);
console.log(`wrote ${path.relative(process.cwd(), OUT)}: ${leafTabs.length} sections${cfg.nav ? ", nested nav" : ""}, ${(html.length / 1024).toFixed(0)} KB`);
