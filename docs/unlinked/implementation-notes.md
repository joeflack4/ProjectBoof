## Implementation Notes
- cBioPortal downloads reuse `db/sources/by_source/cbioportal/download.py`, which unpacks archives into `data/raw/cbioportal/<category>/<study_id>/` and maintains `.download-complete` sentinels.
- ClinGen automation (`db/sources/by_source/clingen/download.py`) captures gene validity, dosage (gene/region/BED), actionability (adult & pediatric JSON), and variant pathogenicity CSV.
- ClinVar automation (`db/sources/by_source/clinvar/download.py`) pulls GRCh37/38 VCFs, tabular summaries, and VCV/RCV XML bundles with remote release metadata.
- TCGA automation (`db/sources/by_source/tcga/download.py`) uses GDC Data Transfer Tool to fetch open-access clinical and molecular data for TCGA-BRCA and TCGA-LUAD projects via GDC API.
- Additional tooling guidance for contributors lives in [`AGENTS.md`](AGENTS.md) and [`db/sources/AGENTS.md`](db/sources/AGENTS.md).
