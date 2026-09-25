# Release

Exported from the lab repo at commit `aa92b87`; shared tooling vendored under [third_party/paperkit](third_party/paperkit) and [third_party/docs_builder](third_party/docs_builder) at the same commit. Rebuild the docs page with:

```
node third_party/docs_builder/build_plan_page.mjs docs/page_config.json
```

- 10 link(s) into private lab notes were rewritten to plain text.
- Third-party figures without a permissive licence were removed from [docs/assets/qual](docs/assets/qual); their provenance entries keep the source pointer. Dataset rows under their own licences stay, with provenance.
  - robospatial1m/fig_1.png (source: https://arxiv.org/html/2411.16537v5/figure2.png)
  - robospatial1m/fig_2.png (source: https://arxiv.org/html/2411.16537v5/figures/figure1.png)
  - warehouse500k/fig_1.png (source: https://arxiv.org/html/2508.13564v1/fig_warehouse_spatial_intelligence.png)
  - sat175k/fig_2.png (source: https://arxiv.org/html/2412.07755v3/QualExamplesSATSynth.svg)
  - sat175k/fig_3.png (source: https://arxiv.org/html/2412.07755v3/staticSYnth.svg)
  - spatialqa50k/fig_1.png (source: https://arxiv.org/html/2406.13642v7/figure_2.png)
  - spatialqa50k/fig_2.png (source: https://arxiv.org/html/2406.13642v7/spatialqa_samples_depth.png)
  - spatialqa50k/fig_3.png (source: https://arxiv.org/html/2406.13642v7/spatialqa_samples_spatial.png)
  - osd87m/fig_2.png (source: https://arxiv.org/html/2406.01584v3/dataset_samples.png)
  - vsi590k/fig_2.png (source: https://arxiv.org/html/2511.04670v1/annotated_real_video_1.png)
  - vsi590k/fig_3.png (source: https://arxiv.org/html/2511.04670v1/procthor.png)
- Docs page: wrote docs/plan_area_a.html: 13 sections, nested nav, 110 KB
