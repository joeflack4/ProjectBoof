# Data Download Summary (Session 1)

## Completed
- Automated cBioPortal PanCan Atlas BRCA & LUAD downloads via `db/sources/by_source/cbioportal/download.py`, with manifests now capturing per-file SHA-256 hashes and sentinel timestamps.
- Implemented ClinGen downloader (`db/sources/by_source/clingen/download.py`) covering gene validity, dosage sensitivity gene/region TSVs, recurrent CNV BEDs, clinical actionability JSON (adult & pediatric), and variant pathogenicity CSV.
- Implemented ClinVar downloader (`db/sources/by_source/clinvar/download.py`) for GRCh37/38 VCFs, monthly tabular releases, and VCV/RCV XML bundles; manifests record remote release metadata.
- Wired all three workflows into `make download-sources` and refreshed documentation (README, AGENTS guidelines, source docs, manifests, checklists).

## Next Steps
1. Add automation for remaining open-access sources (e.g., TCGA GDC clinical/molecular files) and integrate into the Makefile.
2. Plan credential-dependent workflows (COSMIC, OncoKB, TCGA controlled) pending human-provided access tokens.
3. Consider download throttling/parallelism controls and integrity validation (md5/gzip tests) for very large ClinVar XML files.
4. Establish storage monitoring and archival strategy for multi-GB assets to avoid local disk exhaustion.

## Outstanding Tasks (from `notes/dl-data.md`)
- TCGA open-access clinical/molecular downloads (install `gdc-client`, stage manifests, README).
- Optional ClinVar E-utilities scripted queries (esearch/efetch/esummary) if needed for targeted panels.
- Human-task prerequisites for COSMIC and OncoKB authentication, plus follow-on scripted downloads once credentials arrive.
