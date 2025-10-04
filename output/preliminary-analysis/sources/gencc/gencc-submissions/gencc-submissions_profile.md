# Data Analysis Report: Unknown

**Generated**: 2025-10-04 22:15:40

---

## File Information

- **File**: N/A
- **Size**: 0.00 MB

## Field Analysis

Total fields: **30**

### uuid

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 24,124
- **Cardinality**: unique
- **Length**: 55-64 chars (avg: 59.4)
- **Top values**:
  - `GENCC_000101-HGNC_10896-OMIM_182212-HP_0000006-GENCC_100001`: 1 (0.0%)
  - `GENCC_000106-HGNC_16391-OMIM_212050-HP_0000007-GENCC_100002`: 1 (0.0%)
  - `GENCC_000106-HGNC_1514-OMIM_145980-HP_0000006-GENCC_100002`: 1 (0.0%)
  - `GENCC_000106-HGNC_1514-OMIM_612899-HP_0000006-GENCC_100004`: 1 (0.0%)
  - `GENCC_000106-HGNC_1513-OMIM_611938-HP_0000007-GENCC_100002`: 1 (0.0%)

### gene_curie

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 5,533
- **Cardinality**: high
- **Pattern**: HGNC ID
- **Length**: 6-10 chars (avg: 9.4)
- **Top values**:
  - `HGNC:2200`: 50 (0.2%)
  - `HGNC:3690`: 49 (0.2%)
  - `HGNC:3689`: 41 (0.2%)
  - `HGNC:6636`: 41 (0.2%)
  - `HGNC:4827`: 29 (0.1%)

### gene_symbol

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 5,533
- **Cardinality**: high
- **Length**: 2-10 chars (avg: 5.0)
- **Top values**:
  - `COL2A1`: 50 (0.2%)
  - `FGFR3`: 49 (0.2%)
  - `FGFR2`: 41 (0.2%)
  - `LMNA`: 41 (0.2%)
  - `HBB`: 29 (0.1%)

### disease_curie

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 7,566
- **Cardinality**: high
- **Pattern**: MONDO ID
- **Length**: 13-13 chars (avg: 13.0)
- **Top values**:
  - `MONDO:0100038`: 279 (1.2%)
  - `MONDO:0700092`: 157 (0.7%)
  - `MONDO:0044970`: 130 (0.5%)
  - `MONDO:0009723`: 125 (0.5%)
  - `MONDO:0019200`: 117 (0.5%)

### disease_title

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 7,555
- **Cardinality**: high
- **Length**: 6-144 chars (avg: 37.7)
- **Top values**:
  - `complex neurodevelopmental disorder`: 279 (1.2%)
  - `neurodevelopmental disorder`: 157 (0.7%)
  - `mitochondrial disease`: 130 (0.5%)
  - `Leigh syndrome`: 125 (0.5%)
  - `retinitis pigmentosa`: 117 (0.5%)

### disease_original_curie

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 11,050
- **Cardinality**: high
- **Length**: 10-15 chars (avg: 12.0)
- **Top values**:
  - `MONDO:0100038`: 279 (1.2%)
  - `MONDO:0700092`: 157 (0.7%)
  - `MONDO:0044970`: 130 (0.5%)
  - `MONDO:0009723`: 117 (0.5%)
  - `MONDO:0019497`: 94 (0.4%)

### disease_original_title

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 10,826
- **Cardinality**: high
- **Length**: 6-144 chars (avg: 32.6)
- **Top values**:
  - `complex neurodevelopmental disorder`: 279 (1.2%)
  - `neurodevelopmental disorder`: 157 (0.7%)
  - `mitochondrial disease`: 130 (0.5%)
  - `Leigh syndrome`: 117 (0.5%)
  - `nonsyndromic genetic hearing loss`: 94 (0.4%)

### classification_curie

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 8
- **Cardinality**: low
- **Length**: 12-12 chars (avg: 12.0)
- **Top values**:
  - `GENCC:100002`: 7,646 (31.7%)
  - `GENCC:100009`: 5,401 (22.4%)
  - `GENCC:100001`: 4,698 (19.5%)
  - `GENCC:100004`: 3,591 (14.9%)
  - `GENCC:100003`: 2,304 (9.6%)

### classification_title

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 8
- **Cardinality**: low
- **Length**: 6-29 chars (avg: 8.4)
- **Top values**:
  - `Strong`: 7,646 (31.7%)
  - `Supportive`: 5,401 (22.4%)
  - `Definitive`: 4,698 (19.5%)
  - `Limited`: 3,591 (14.9%)
  - `Moderate`: 2,304 (9.6%)

### moi_curie

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 8
- **Cardinality**: low
- **Length**: 10-10 chars (avg: 10.0)
- **Top values**:
  - `HP:0000007`: 11,723 (48.6%)
  - `HP:0000006`: 10,020 (41.5%)
  - `HP:0001417`: 1,202 (5.0%)
  - `HP:0000005`: 928 (3.8%)
  - `HP:0032113`: 140 (0.6%)

### moi_title

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 8
- **Cardinality**: low
- **Length**: 7-20 chars (avg: 17.5)
- **Top values**:
  - `Autosomal recessive`: 11,723 (48.6%)
  - `Autosomal dominant`: 10,020 (41.5%)
  - `X-linked`: 1,202 (5.0%)
  - `Unknown`: 928 (3.8%)
  - `Semidominant`: 140 (0.6%)

### submitter_curie

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 16
- **Cardinality**: medium
- **Length**: 12-12 chars (avg: 12.0)
- **Top values**:
  - `GENCC:000106`: 5,528 (22.9%)
  - `GENCC:000110`: 5,401 (22.4%)
  - `GENCC:000101`: 4,216 (17.5%)
  - `GENCC:000112`: 3,339 (13.8%)
  - `GENCC:000102`: 2,609 (10.8%)

### submitter_title

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 16
- **Cardinality**: medium
- **Length**: 3-67 chars (avg: 16.2)
- **Top values**:
  - `Labcorp Genetics (formerly Invitae)`: 5,528 (22.9%)
  - `Orphanet`: 5,401 (22.4%)
  - `Ambry Genetics`: 4,216 (17.5%)
  - `G2P`: 3,339 (13.8%)
  - `ClinGen`: 2,609 (10.8%)

### submitted_as_hgnc_id

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 5,534
- **Cardinality**: high
- **Pattern**: HGNC ID
- **Length**: 6-11 chars (avg: 9.4)
- **Top values**:
  - `HGNC:2200`: 50 (0.2%)
  - `HGNC:3690`: 49 (0.2%)
  - `HGNC:6636`: 41 (0.2%)
  - `HGNC:3689`: 41 (0.2%)
  - `HGNC:4827`: 29 (0.1%)

### submitted_as_hgnc_symbol

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 5,577
- **Cardinality**: high
- **Length**: 2-10 chars (avg: 5.0)
- **Top values**:
  - `COL2A1`: 50 (0.2%)
  - `FGFR3`: 49 (0.2%)
  - `FGFR2`: 41 (0.2%)
  - `LMNA`: 41 (0.2%)
  - `HBB`: 29 (0.1%)

### submitted_as_disease_id

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 11,051
- **Cardinality**: high
- **Length**: 10-15 chars (avg: 12.0)
- **Top values**:
  - `MONDO:0100038`: 279 (1.2%)
  - `MONDO:0700092`: 157 (0.7%)
  - `MONDO:0044970`: 130 (0.5%)
  - `MONDO:0009723`: 117 (0.5%)
  - `MONDO:0019497`: 94 (0.4%)

### submitted_as_disease_name

- **Type**: string
- **Non-null**: 24,119 / 24,124 (100.0%)
- **Unique values**: 16,597
- **Cardinality**: high
- **Length**: 2-145 chars (avg: 39.7)
- **Top values**:
  - `complex neurodevelopmental disorder`: 229 (0.9%)
  - `mitochondrial disease`: 124 (0.5%)
  - `Leigh syndrome`: 119 (0.5%)
  - `nonsyndromic genetic hearing loss`: 90 (0.4%)
  - `Retinitis pigmentosa`: 89 (0.4%)

### submitted_as_moi_id

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 11
- **Cardinality**: medium
- **Length**: 10-11 chars (avg: 10.0)
- **Top values**:
  - `HP:0000007`: 11,724 (48.6%)
  - `HP:0000006`: 9,998 (41.4%)
  - `HP:0001417`: 1,202 (5.0%)
  - `HP:0000005`: 925 (3.8%)
  - `HP:0032113`: 130 (0.5%)

### submitted_as_moi_name

- **Type**: string
- **Non-null**: 23,705 / 24,124 (98.3%)
- **Unique values**: 26
- **Cardinality**: medium
- **Length**: 2-65 chars (avg: 24.2)
- **Top values**:
  - `Autosomal recessive inheritance`: 5,874 (24.3%)
  - `Autosomal dominant inheritance`: 5,652 (23.4%)
  - `Autosomal recessive`: 3,879 (16.1%)
  - `Autosomal dominant`: 2,942 (12.2%)
  - `biallelic_autosomal`: 1,814 (7.5%)

### submitted_as_submitter_id

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 16
- **Cardinality**: medium
- **Length**: 12-12 chars (avg: 12.0)
- **Top values**:
  - `GENCC:000106`: 5,528 (22.9%)
  - `GENCC:000110`: 5,401 (22.4%)
  - `GENCC:000101`: 4,216 (17.5%)
  - `GENCC:000112`: 3,339 (13.8%)
  - `GENCC:000102`: 2,609 (10.8%)

### submitted_as_submitter_name

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 22
- **Cardinality**: medium
- **Length**: 4-67 chars (avg: 9.8)
- **Top values**:
  - `Orphanet`: 5,401 (22.4%)
  - `Invitae`: 5,328 (22.1%)
  - `Ambry Genetics`: 4,036 (16.7%)
  - `TGMI`: 3,339 (13.8%)
  - `ClinGen`: 2,609 (10.8%)

### submitted_as_classification_id

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 9
- **Cardinality**: low
- **Length**: 12-13 chars (avg: 12.0)
- **Top values**:
  - `GENCC:100002`: 7,646 (31.7%)
  - `GENCC:100009`: 5,401 (22.4%)
  - `GENCC:100001`: 4,698 (19.5%)
  - `GENCC:100004`: 3,590 (14.9%)
  - `GENCC:100003`: 2,304 (9.6%)

### submitted_as_classification_name

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 23
- **Cardinality**: medium
- **Length**: 6-29 chars (avg: 8.4)
- **Top values**:
  - `Strong`: 6,887 (28.5%)
  - `Supportive`: 5,401 (22.4%)
  - `Limited`: 3,132 (13.0%)
  - `Definitive`: 2,757 (11.4%)
  - `Moderate`: 2,095 (8.7%)

### submitted_as_date

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 10,790
- **Cardinality**: high
- **Length**: 19-19 chars (avg: 19.0)
- **Top values**:
  - `2021-09-14 00:00:00`: 5,330 (22.1%)
  - `2015-07-22 00:00:00`: 599 (2.5%)
  - `2023-05-24 00:00:00`: 239 (1.0%)
  - `2020-10-09 00:00:00`: 223 (0.9%)
  - `2025-01-21 00:00:00`: 184 (0.8%)

### submitted_as_public_report_url

- **Type**: string
- **Non-null**: 8,256 / 24,124 (34.2%)
- **Unique values**: 6,275
- **Cardinality**: high
- **Pattern**: URL
- **Length**: 33-125 chars (avg: 72.3)
- **Top values**:
  - `https://onlinelibrary.wiley.com/doi/full/10.1002/humu.24033`: 148 (0.6%)
  - `https://panelapp.genomicsengland.co.uk/panels/474`: 102 (0.4%)
  - `https://panelapp.genomicsengland.co.uk/panels/540`: 73 (0.3%)
  - `https://panelapp.genomicsengland.co.uk/panels/179`: 72 (0.3%)
  - `https://panelapp.genomicsengland.co.uk/panels/53`: 64 (0.3%)

### submitted_as_notes

- **Type**: string
- **Non-null**: 443 / 24,124 (1.8%)
- **Unique values**: 176
- **Cardinality**: medium
- **Length**: 120-3562 chars (avg: 521.9)
- **Top values**:
  - `This gene-disease relationship has undergone rapid assessment. Classifications are based on preliminary review of gene-disease validity during analysis of genomic sequencing results.`: 260 (1.1%)
  - `Alhathal et al., 2020 (PMID: 32719396) reported a missense variant in a large male infertility cohort (n=285 infertile man and case–control fertile man). Gene is scored according to ClinGen classification. Limited with total score of 4. Single variant segregation (3 points), experimental evidence: testicular expression (1 points) (PMID: 27965440).`: 5 (0.0%)
  - `Convincing evidence disputing a role for this gene is this disease has arisen since the initial report identifying an association between the gene and disease. Alhathal et al., 2020 (PMID: 32719396) reported a LOF variant in a large male infertility cohort (n=285 infertile man and case–control fertile man).`: 2 (0.0%)
  - `13 families with an anosmic form of IGD (Kallmann syndrome) were found to carry loss-of-function mutations in TCF12 gene.`: 2 (0.0%)
  - `Alhathal et al., 2020 (PMID: 32719396) reported a missense variant in a large male infertility cohort (n=285 infertile man and case–control fertile man). Gene is scored according to ClinGen classification. Moderate with total score of 8. Single-variant analysis (3 points), experimental evidence: Animal model (4 points) and testicular expression (1 points) (PMID: 21478856; PMID: 21079677).`: 2 (0.0%)

### submitted_as_pmids

- **Type**: string
- **Non-null**: 14,973 / 24,124 (62.1%)
- **Unique values**: 13,318
- **Cardinality**: high
- **Length**: 1-790 chars (avg: 31.6)
- **Top values**:
  - `0`: 66 (0.3%)
  - `20301607[PMID]_24148127[PMID]`: 57 (0.2%)
  - `20301590[PMID]`: 50 (0.2%)
  - `28472652`: 49 (0.2%)
  - `32719396`: 39 (0.2%)

### submitted_as_assertion_criteria_url

- **Type**: string
- **Non-null**: 22,877 / 24,124 (94.8%)
- **Unique values**: 224
- **Cardinality**: medium
- **Pattern**: URL
- **Length**: 14-126 chars (avg: 75.0)
- **Top values**:
  - `https://www.orpha.net/orphacom/cahiers/docs/GB/Orphanet_Genes_inventory_R1_Ann_gen_EP_02.pdf`: 5,401 (22.4%)
  - `https://view.publitas.com/invitae/invitaeposter_nsgc2019_curatingthehumangenome/page/1`: 5,326 (22.1%)
  - `https://www.ebi.ac.uk/gene2phenotype/about/terminology`: 3,339 (13.8%)
  - `https://www.clinicalgenome.org/docs/?doc-type=curation-activity-procedures&curation-procedure=gene-disease-validity`: 2,667 (11.1%)
  - `PMID: 28106320`: 1,574 (6.5%)

### submitted_as_submission_id

- **Type**: string
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 21,640
- **Cardinality**: high
- **Length**: 1-46 chars (avg: 13.2)
- **Top values**:
  - `1`: 59 (0.2%)
  - `15769`: 17 (0.1%)
  - `16186`: 16 (0.1%)
  - `16364`: 15 (0.1%)
  - `16664`: 11 (0.0%)

### submitted_run_date

- **Type**: date
- **Non-null**: 24,124 / 24,124 (100.0%)
- **Unique values**: 41
- **Cardinality**: medium
