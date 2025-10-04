# Data Sources for Real World Evidence Analysis

## Overview

This document provides an overview of the major genomic and clinical data sources that will be used for Real World Evidence (RWE) analysis, virtual cohort aggregation, and harmonization across data sources. The focus is primarily on clinical questions and analysis involving individual and population-level queries.

All data sources have been researched and documented with details about:
- Data types and content
- Access methods (Web, API, FTP, downloads)
- File formats and structure
- Cost and licensing requirements
- Example queries and code snippets

## Data Sources Summary

| Data Source | Type | Focus | Cost | Access Level | API | Documentation |
|-------------|------|-------|------|--------------|-----|---------------|
| [cBioPortal](#cbioportal) | Cancer Genomics Database | Multidimensional cancer data | Free | Open | REST | [cbioportal.md](data-sources/cbioportal.md) |
| [ClinGen](#clingen) | Gene-Disease Curation | Clinical genome resource | Free (CC0) | Open | REST, Files | [clingen.md](data-sources/clingen.md) |
| [ClinVar](#clinvar) | Variant Database | Variant-disease relationships | Free (Public Domain) | Open | E-utilities | [clinvar.md](data-sources/clinvar.md) |
| [COSMIC](#cosmic) | Cancer Mutations | Somatic mutations in cancer | Academic: Free<br>Commercial: Paid | Gated | Files only | [cosmic.md](data-sources/cosmic.md) |
| [GenCC](#gencc) | Gene-Disease Validity | Harmonized gene-disease assertions | Free (CC0) | Open | Coming soon | [gencc.md](data-sources/gencc.md) |
| [OncoKB](#oncokb) | Precision Oncology | Therapeutic implications of variants | Academic: Free<br>Commercial: Paid | Gated | REST | [oncokb.md](data-sources/oncokb.md) |
| [TCGA](#tcga) | Cancer Genomics | Large-scale cancer genomics | Free | Open + Controlled | REST, Files | [tcga.md](data-sources/tcga.md) |

## Quick Reference

### Data Source Categories

#### Cancer-Focused Databases
- **cBioPortal**: Multi-omic cancer data visualization and analysis
- **COSMIC**: Catalogue of somatic mutations in cancer
- **OncoKB**: Precision oncology knowledge base for therapeutic implications
- **TCGA**: The Cancer Genome Atlas - comprehensive cancer genomics

#### Variant Interpretation
- **ClinVar**: Variant pathogenicity and clinical significance
- **ClinGen**: Gene-disease validity, dosage sensitivity, actionability
- **GenCC**: Harmonized gene-disease validity assertions
- **OncoKB**: Oncogenic and therapeutic variant annotations

#### Gene-Disease Relationships
- **ClinGen**: Expert-curated gene-disease validity
- **GenCC**: Aggregated gene-disease curations from multiple sources
- **OncoKB**: Cancer gene annotations

### Cost and Licensing Quick Reference

#### Completely Free (No Restrictions)
- **ClinVar**: Public domain (US Gov work)
- **ClinGen**: CC0 1.0 Public Domain
- **GenCC**: CC0 1.0 Public Domain
- **TCGA**: Free (open access data)

#### Free for Academic, Paid for Commercial
- **COSMIC**: Free for academic/non-profit; paid license for commercial
- **OncoKB**: Free for academic research; paid license for commercial

#### Always Free
- **cBioPortal**: Free and open source (AGPL v3)
- **TCGA** (open access tier): Free for all

#### Requires Authorization (But Free)
- **TCGA** (controlled access tier): Free but requires dbGaP authorization

### API Availability

#### REST APIs Available Now
- cBioPortal (Swagger/OpenAPI)
- ClinGen (Allele Registry, downloads)
- ClinVar (E-utilities)
- OncoKB (Swagger/OpenAPI, requires token)
- TCGA/GDC (REST API)

#### File Downloads Only
- COSMIC (authenticated HTTPS downloads)
- GenCC (direct file downloads; API coming soon)

#### No Public API
- COSMIC (no public REST/GraphQL API for the cancer database)

## Detailed Source Descriptions

### cBioPortal

**Purpose**: Open-source platform for exploring and analyzing multidimensional cancer genomics data

**Key Features**:
- >1.4M samples with >38M mutations
- Web interface and comprehensive API
- Multiple molecular data types (mutations, CNAs, expression, fusions)
- Clinical data integration
- Free and open source

**Best For**: Interactive exploration of cancer genomics datasets, integrated multi-omic analysis

**Documentation**: [data-sources/cbioportal.md](data-sources/cbioportal.md)

---

### ClinGen

**Purpose**: NIH-funded resource defining clinical relevance of genes and variants for precision medicine

**Key Features**:
- >2,700 expert curators from 72+ countries
- Gene-disease validity (2,420 curated)
- Variant pathogenicity (5,161 variants)
- Dosage sensitivity (1,557 genes)
- Clinical actionability (447 gene-condition pairs)
- Allele Registry for variant identifiers

**Best For**: Authoritative gene-disease validity, variant pathogenicity, dosage sensitivity

**Documentation**: [data-sources/clingen.md](data-sources/clingen.md)

---

### ClinVar

**Purpose**: Public archive of variant-disease relationships from >2,800 organizations

**Key Features**:
- >3M variants with clinical interpretations
- Germline, somatic oncogenicity, and clinical impact classifications
- Updated weekly (web) and monthly (comprehensive releases)
- NCBI E-utilities API access
- VCF, XML, TSV formats

**Best For**: Comprehensive variant interpretation data, clinical significance of variants

**Documentation**: [data-sources/clinvar.md](data-sources/clinvar.md)

---

### COSMIC

**Purpose**: World's largest resource for somatic mutations in cancer

**Key Features**:
- >1.4M samples, >38M mutations
- Cancer Gene Census (>750 genes)
- Cancer Mutation Census
- Actionability module (>13,000 clinical trials)
- Cell lines and resistance mutations
- Curated by Wellcome Sanger Institute

**Best For**: Comprehensive somatic mutation data, cancer driver genes, mutation frequencies

**Documentation**: [data-sources/cosmic.md](data-sources/cosmic.md)

---

### GenCC

**Purpose**: Global coalition harmonizing gene-disease validity curation

**Key Features**:
- 17 member organizations (ClinGen, DECIPHER, Orphanet, etc.)
- 8 standardized validity classifications
- Focused on Mendelian diseases
- MONDO disease ontology mapping
- CC0 public domain license

**Best For**: Aggregated gene-disease validity from multiple expert sources

**Documentation**: [data-sources/gencc.md](data-sources/gencc.md)

---

### OncoKB

**Purpose**: MSK's precision oncology knowledge base for variant therapeutic implications

**Key Features**:
- >800 genes, >7,800 alterations annotated
- Therapeutic levels of evidence (1, 2, 3A, 3B, 4, R1, R2)
- Oncogenicity and mutation effect annotations
- FDA-recognized database (partial)
- Integrated into cBioPortal

**Best For**: Therapeutic actionability of cancer variants, FDA-approved and investigational therapies

**Documentation**: [data-sources/oncokb.md](data-sources/oncokb.md)

---

### TCGA

**Purpose**: Landmark cancer genomics program with >20,000 samples across 33 cancer types

**Key Features**:
- Comprehensive multi-omic data (DNA-seq, RNA-seq, methylation, CNAs, protein)
- Clinical and imaging data
- Accessible through NCI Genomic Data Commons (GDC)
- Open access and controlled access tiers
- PanCanAtlas integrated analyses

**Best For**: Large-scale cancer genomics research, multi-omic integration, pan-cancer studies

**Documentation**: [data-sources/tcga.md](data-sources/tcga.md)

---

## Data Harmonization Considerations

### Common Data Elements

Across sources, key common elements for harmonization:

**Genes**:
- HGNC symbols (standardized)
- Entrez Gene IDs
- Ensembl Gene IDs

**Variants**:
- HGVS notation (genomic, coding, protein)
- Genomic coordinates (GRCh37/hg19 and GRCh38/hg38)
- dbSNP rs IDs
- ClinVar Variation IDs
- ClinGen Allele IDs

**Diseases**:
- MONDO (Monarch Disease Ontology) - used by GenCC, ClinGen
- OMIM IDs
- MedGen concepts
- Oncotree (cancer types) - used by cBioPortal, OncoKB

**Clinical Classifications**:
- ACMG/AMP pathogenicity terms (ClinVar, ClinGen)
- Gene-disease validity terms (ClinGen, GenCC)
- Oncogenicity classifications (OncoKB, COSMIC)
- Therapeutic levels of evidence (OncoKB)

### Genome Builds

**GRCh37 (hg19)**: Legacy TCGA data, some COSMIC/ClinVar files
**GRCh38 (hg38)**: GDC harmonized data, current standard for most sources

Coordinate liftover will be necessary for integration.

### File Format Compatibility

**Common formats across sources**:
- VCF (variants): ClinVar, COSMIC, TCGA, cBioPortal
- TSV/CSV (tabular): All sources
- JSON: ClinVar, ClinGen, OncoKB, TCGA/GDC, cBioPortal
- MAF (mutations): cBioPortal, TCGA, COSMIC, OncoKB

## Integration Strategies

### For Variant-Level Analysis

1. **Variant Normalization**:
   - Standardize to HGVS notation
   - Use ClinGen Allele Registry for variant identifiers
   - Map to both GRCh37 and GRCh38

2. **Pathogenicity**:
   - ClinVar: Germline pathogenicity
   - ClinGen: Expert panel variant classifications
   - OncoKB: Somatic oncogenicity
   - COSMIC: Mutation frequencies in cancer

3. **Therapeutic Implications**:
   - OncoKB: FDA-approved and investigational therapies
   - COSMIC Actionability: Clinical trials
   - cBioPortal: Integrated therapeutic annotations

### For Gene-Level Analysis

1. **Gene-Disease Validity**:
   - ClinGen: Authoritative curations
   - GenCC: Aggregated from multiple sources
   - OncoKB: Cancer gene roles

2. **Gene Function**:
   - COSMIC: Cancer Gene Census
   - OncoKB: Oncogene/TSG classification
   - ClinGen: Dosage sensitivity

### For Cohort-Level Analysis

1. **Cancer Cohorts**:
   - TCGA: Large-scale, multi-omic cancer data
   - cBioPortal: Aggregated cancer studies
   - COSMIC: Cell line models

2. **Population Frequencies**:
   - COSMIC: Mutation frequencies in tumors
   - TCGA: Frequencies across cancer types
   - cBioPortal: Study-specific frequencies

## Next Steps

This documentation serves as Phase 1 of the data source research. Future phases may include:

1. **Phase 2** (from notes/docs-start2.md):
   - Comprehensive field-level detail for all file formats
   - Harmonization mapping between data sources
   - Common field identification and crosswalks

2. **Implementation**:
   - Data download and preprocessing pipelines
   - Harmonization workflows
   - Database schema design for integrated data
   - Query optimization strategies

3. **Analysis Development**:
   - Virtual cohort aggregation methods
   - Individual and population-level query templates
   - Clinical question frameworks

## References and Citations

When using these data sources, please cite appropriately:

- **cBioPortal**: Cerami E, et al. (2012); Gao J, et al. (2013)
- **ClinGen**: Rehm HL, et al. (2015)
- **ClinVar**: Landrum MJ, et al. (2018, 2025)
- **COSMIC**: Tate JG, et al. (2019); Bamford S, et al. (2024)
- **GenCC**: Rehm HL, et al. (2022)
- **OncoKB**: Chakravarty D, et al. (2017); Suehnholz SP, et al. (2023)
- **TCGA**: Cancer Genome Atlas Research Network (various cancer-specific papers)

Full citation details available in individual data source documentation files.

---

*Last Updated: 2025*
*For questions or updates, refer to individual source documentation files.*
