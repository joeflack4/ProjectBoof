# ClinGen (Clinical Genome Resource)

## Overview

ClinGen is a National Institutes of Health (NIH)-funded resource dedicated to building a central repository that defines the clinical relevance of genes and variants for use in precision medicine and research. It is a global collaborative effort involving over 2,700 expert contributors from 72+ countries who curate genomic knowledge through standardized processes.

**Website**: https://clinicalgenome.org
**Data Portal**: https://search.clinicalgenome.org
**FTP Server**: https://ftp.clinicalgenome.org
**Allele Registry**: https://reg.clinicalgenome.org
**Version**: Current/Latest (as of 2025)

## Data Types

ClinGen provides several categories of curated genomic knowledge:

### 1. Gene-Disease Validity

Determines whether gene variations can cause specific diseases through systematic evidence evaluation.

**Content:**
- Gene-disease relationship classifications
- Evidence supporting associations
- Clinical validity assessments
- Expert panel curations

**Statistics (as of Jan 2024):**
- 2,420 gene-disease relationships curated

### 2. Variant Pathogenicity

Identifies which specific genetic changes (variants) cause disease using ACMG/AMP guidelines.

**Content:**
- Variant pathogenicity classifications (Pathogenic, Likely Pathogenic, VUS, Likely Benign, Benign)
- Evidence criteria and strength assessments
- Expert panel variant interpretations
- ACMG/AMP criterion specifications per gene/disease

**Statistics (as of Jan 2024):**
- 5,161 unique variants classified

### 3. Dosage Sensitivity

Evaluates how changes in gene copy number (deletions or duplications) impact health.

**Content:**
- Haploinsufficiency scores (loss of one copy)
- Triplosensitivity scores (gain of one copy)
- Gene-level dosage sensitivity
- Region-level dosage sensitivity
- Supporting evidence and assertions

**Statistics (as of Jan 2024):**
- 1,557 genes curated for dosage sensitivity

### 4. Clinical Actionability

Assesses potential medical actions that can improve patient outcomes based on genetic findings.

**Content:**
- Actionability assertions for gene-condition pairs
- Adult and pediatric context evaluations
- Actionability scores and evidence
- Intervention recommendations

**Statistics (as of Jan 2024):**
- 447 gene-condition pairs curated for actionability

### 5. Somatic Cancer Variant Curation

Cancer-specific variant classifications and gene-disease relationships.

### 6. Baseline Annotation

Structured evidence from biomedical literature to support genomic curation.

## Access Methods

### 1. Web Interface

**Main Portal**: https://clinicalgenome.org
**Search Interface**: https://search.clinicalgenome.org

Browse and search gene and variant curations through interactive web interface.

### 2. File Downloads (Direct Download & FTP)

**Downloads Page**: https://search.clinicalgenome.org/kb/downloads
**FTP Server**: ftp://ftp.clinicalgenome.org

#### Available File Formats
- **CSV**: Comma-separated values
- **TSV**: Tab-separated values
- **JSON**: JavaScript Object Notation
- **BED**: Browser Extensible Data (for genomic regions)
- **AED**: Array Element Data (for array analysis)

#### Download Categories

**Gene-Disease Validity:**
- Real-time CSV download of all gene-disease curations
- Curations organized by expert panel
- Gene-disease classification scores

**Dosage Sensitivity:**
- Gene-level curation files
- Region-level curation files
- Support for GRCh37 and GRCh38 genome builds
- Haploinsufficiency and triplosensitivity data
- Gene tables: `https://search.clinicalgenome.org/kb/gene-dosage/download?build=GRCh37|GRCh38`
- Region TSVs: `ftp://ftp.clinicalgenome.org/ClinGen_region_curation_list_GRCh37.tsv` / `...GRCh38.tsv`
- Recurrent CNV BED files: `ftp://ftp.clinicalgenome.org/ClinGen%20recurrent%20CNV%20.bed%20file%20V1.1-hg19.bed` (hg19) and `...hg38.bed`

**Clinical Actionability:**
- JSON APIs (Adult and Pediatric contexts)
- Nested and flat JSON formats
- TSV downloads for scoring and assertions
- Adult summary API: `https://actionability.clinicalgenome.org/ac/Adult/api/summ?flavor=flat`
- Pediatric summary API: `https://actionability.clinicalgenome.org/ac/Pediatric/api/summ?flavor=flat`

**Variant Pathogenicity:**
- CSV download of all variant curations
- Variant-level assertions and evidence
- Aggregated CSV: `https://erepo.clinicalgenome.org/evrepo/api/classifications/all?format=csv`

**Update Frequency:**
- Nightly file refreshes
- 60-day file archives maintained

### 3. REST APIs

ClinGen provides several REST APIs for programmatic access:

#### ClinGen Allele Registry API

**Base URL**: https://reg.clinicalgenome.org
**API Specification**: https://reg.clinicalgenome.org/doc/AlleleRegistry_1.01.xx_api_v1.pdf

**Purpose:** Provides unique, persistent identifiers for genetic variants (ClinGen Allele IDs) and links variant representations across databases.

**Key Features:**
- Query variants using HGVS expressions
- Search by locus, gene, ClinVar ID, or dbSNP ID
- Register new alleles
- Bulk query/registration capabilities
- Returns JSON-LD (Linked Data format) or annotated VCF

**Example Endpoint:**
```
http://reg.clinicalgenome.org/alleles.json?file=hgvs&fields=none+@id
```

**Performance:**
- Processes hundreds of variants in < 10 seconds
- Recommended batch size: < 1M variants per query
- Supports > 500,000 reference sequences

**Authentication:**
- Public queries: No authentication required
- Allele registration: Login required (request via brl-allele-reg@bcm.edu)

#### Gene Curation Interface (GCI) API

**Documentation**: https://vci-gci-docs.clinicalgenome.org/vci-gci-docs/gci-help/gci-api

**Purpose:** Provides access to gene-disease validity curations.

**Features:**
- Query gene-disease validity reports
- Access GCEP (Gene Curation Expert Panel) curations

**Access:**
- Limited to authorized Gene Curation Expert Panels
- API keys available through GCEP coordinator

#### Variant Pathogenicity API

**OpenAPI Documentation**: Available on downloads page

**Purpose:** Access variant pathogenicity classifications programmatically.

**Features:**
- Query variant classifications
- Retrieve evidence and criteria specifications
- REST endpoints for variant-level data

#### ClinGen Linked Data Hub (LDH)

**Purpose:** Facilitates efficient access to collated genomic information through RESTful APIs.

**Focus:** Links information about human genes and variants to support ClinGen curation efforts.

**Data Models:**
- Allele Model (released 2017): JSON-LD representation in Allele Registry
- Interpretation Model (released 2018): Variant Pathogenicity Interpretations based on ACMG/AMP guidelines

### 4. ClinVar Integration

**Website**: https://www.ncbi.nlm.nih.gov/clinvar/

ClinGen classified variants are submitted to ClinVar (NCBI's public database), providing an additional access point for ClinGen variant pathogenicity data.

### 5. Example Code Snippets

#### Python - Query Allele Registry
```python
import requests

# Query variant by HGVS expression
hgvs_expr = "NM_000277.1:c.1521_1523delCTT"
url = f"https://reg.clinicalgenome.org/allele?hgvs={hgvs_expr}"

response = requests.get(url)
allele_data = response.json()

print(f"ClinGen Allele ID: {allele_data['@id']}")
```

#### Python - Download Gene-Disease Validity Data
```python
import pandas as pd

# Download gene-disease validity curations
url = "https://search.clinicalgenome.org/kb/gene-validity/download"
df = pd.read_csv(url)

# Filter for Definitive classifications
definitive = df[df['Classification'] == 'Definitive']
print(f"Definitive gene-disease associations: {len(definitive)}")
```

#### R - Access ClinGen Data
```r
library(httr)
library(jsonlite)

# Query Allele Registry
hgvs <- "NM_000277.1:c.1521_1523delCTT"
url <- paste0("https://reg.clinicalgenome.org/allele?hgvs=", hgvs)

response <- GET(url)
allele_data <- content(response, "parsed")

cat("ClinGen Allele ID:", allele_data$`@id`, "\n")
```

#### Bash - Download via FTP
```bash
# Download dosage sensitivity files
wget ftp://ftp.clinicalgenome.org/ClinGen_gene_curation_list_GRCh38.tsv

# Download all gene-disease validity data
curl -o gene_validity.csv https://search.clinicalgenome.org/kb/gene-validity/download
```

## Cost and Requirements

### Cost
**FREE** - ClinGen is completely free to use
- No subscription fees
- No registration required for data access
- No usage limits

### License
**CC0 1.0 Universal Public Domain Dedication**
- Most permissive open license
- No legal restrictions on use
- Content placed in public domain
- Can be freely captured, redistributed, and reused
- Commercial use allowed

### Attribution
- **Not legally required** (due to CC0 license)
- **Requested**: Give attribution to ClinGen and provide access date when appropriate
- Suggested citation format available at: https://clinicalgenome.org/docs/terms-of-use/

### Registration
- **Not required** for browsing, downloads, or most API access
- **Required** for Allele Registry variant registration (email request to brl-allele-reg@bcm.edu)
- **Required** for Gene Curation Interface API (limited to expert panels)

### FDA Recognition
- FDA recognized ClinGen's hereditary germline variant curations as a valid source of accurate human variant interpretation data (December 2018)

## Data Structure

### File Organization

ClinGen data is organized by curation activity type with standardized file formats for downloads.

### Major Data Categories and Key Fields

#### 1. Gene-Disease Validity Files (CSV/TSV)

**Key Fields:**
- `Gene Symbol`: HGNC gene symbol
- `Gene ID (HGNC)`: HGNC gene identifier
- `Disease Label`: Disease name
- `Disease ID (MONDO)`: MONDO ontology ID
- `MOI`: Mode of Inheritance
- `SOP`: Standard Operating Procedures version used
- `Classification`: Validity classification (Definitive, Strong, Moderate, Limited, Disputed, Refuted, No Known Disease Relationship)
- `Classification Date`: Date of classification
- `GCEP`: Gene Curation Expert Panel name
- `Online Report`: Link to full curation report

#### 2. Dosage Sensitivity Files (TSV/BED)

**Gene-Level Files - Key Fields:**
- `Gene Symbol`: HGNC gene symbol
- `Gene ID`: HGNC identifier
- `Cytogenetic Location`: Chromosomal band location
- `Genomic Location` (GRCh37/GRCh38): Coordinates
- `Haploinsufficiency Score`: 0 (Unlikely), 1 (Little Evidence), 2 (Emerging), 3 (Sufficient Evidence), 30 (Gene associated with autosomal recessive disease), 40 (Dosage sensitivity unlikely)
- `Triplosensitivity Score`: Same scale as haploinsufficiency
- `Haploinsufficiency Description`: Evidence summary
- `Triplosensitivity Description`: Evidence summary
- `Haploinsufficiency PMID`: Supporting publications
- `Triplosensitivity PMID`: Supporting publications

**Region-Level Files - Key Fields:**
- `ISCA ID`: Region identifier
- `ISCA Region Name`: Region description
- `Cytogenetic Location`: Chromosomal location
- `Genomic Location` (GRCh37/GRCh38): Coordinates
- `Haploinsufficiency Score`: Same scale as gene-level
- `Triplosensitivity Score`: Same scale as gene-level
- `Loss/Gain Phenotype`: Associated clinical features

**BED Format Files:**
- Chromosome
- Start position
- End position
- Gene symbol or region ID
- Haploinsufficiency/Triplosensitivity score

#### 3. Clinical Actionability Files (JSON/TSV)

**JSON Format - Key Fields:**
```json
{
  "gene": "Gene symbol",
  "condition": "Condition name",
  "context": "Adult or Pediatric",
  "actionability_assertion": "Assertion outcome",
  "actionability_score": "Numeric score",
  "report_date": "Publication date",
  "report_url": "Link to full report"
}
```

**TSV Format - Key Fields:**
- `Gene`: Gene symbol
- `Condition`: Associated condition
- `Adult/Pediatric Context`: Population context
- `Assertion`: Actionable or Not Actionable
- `Score`: Actionability score
- `Topic Team`: Expert panel
- `Report Date`: Publication date

#### 4. Variant Pathogenicity Files (CSV)

**Key Fields:**
- `ClinGen Allele ID`: Unique ClinGen variant identifier
- `Gene Symbol`: HGNC gene symbol
- `HGVS Nucleotide`: Nucleotide-level HGVS expression
- `HGVS Protein`: Protein-level HGVS expression
- `Classification`: Pathogenic, Likely Pathogenic, VUS, Likely Benign, Benign
- `Classification Date`: Date of classification
- `Assertion Method`: ACMG/AMP criteria version
- `VCEP`: Variant Curation Expert Panel
- `Condition`: Associated disease/phenotype
- `Condition ID`: MONDO or other ontology ID
- `MOI`: Mode of Inheritance
- `ClinVar Variation ID`: ClinVar identifier (if available)
- `Evidence Summary`: Brief description of supporting evidence

#### 5. Allele Registry API Response (JSON-LD)

**Key Fields:**
```json
{
  "@id": "ClinGen Allele ID (CAxxxxx)",
  "externalRecords": {
    "ClinVarVariations": ["ClinVar IDs"],
    "dbSNP": ["rs IDs"],
    "CARiD": ["CAID"]
  },
  "genomicAlleles": [
    {
      "referenceGenome": "GRCh38",
      "chromosome": "chr17",
      "coordinates": [...],
      "hgvs": ["NC_000017.11:g.43094692C>T"]
    }
  ],
  "transcriptAlleles": [
    {
      "geneSymbol": "BRCA1",
      "refSeq": "NM_007294.4",
      "hgvs": "NM_007294.4:c.5266dupC"
    }
  ],
  "proteinAlleles": [
    {
      "hgvs": "NP_009225.1:p.Gln1756fs"
    }
  ]
}
```

### Data Models

#### ClinGen Data Exchange Models

**1. Allele Model (2017)**
- JSON-LD representation
- Used in ClinGen Allele Registry
- Links variant representations across databases
- Incorporates HGVS, genomic coordinates, and external IDs

**2. Interpretation Model (2018)**
- Supports Variant Pathogenicity Interpretations
- Based on ACMG/AMP 2015 guidelines
- Structured evidence types
- Uses HL7 FHIR concepts (Codings, Codeable Concepts)
- Disease representation via ontologies (MONDO, Orphanet)

#### CSpec Registry

**Purpose:** Stores Variant Curation Expert Panel Criteria Specifications in structured, machine-readable format.

**Content:**
- Gene/disease-specific ACMG/AMP criteria specifications
- Evidence strength modifications
- Rule sets for automated variant classification

### Database/Repository Structure

ClinGen maintains several interconnected systems:

1. **ClinGen Website**: Main portal for browsing curations
2. **Allele Registry**: Variant identifier resolution and linking
3. **Variant Curation Interface (VCI)**: Platform for variant pathogenicity curation
4. **Gene Curation Interface (GCI)**: Platform for gene-disease validity curation
5. **Dosage Sensitivity Map**: Browser for CNV-related gene/region curations
6. **FTP Server**: Bulk file downloads
7. **ClinVar**: External integration for variant submissions

## Additional Resources

- **User Guides**: https://clinicalgenome.org/tools/
- **Training Materials**: Available for each curation activity
- **Community Support**: Google Groups and contact forms
- **Documentation**: https://clinicalgenome.org/docs/
- **GitHub**: https://github.com/ClinGen
- **Data Model Repository**: https://github.com/clingen-data-model

## Summary

ClinGen provides authoritative, expert-curated genomic knowledge across gene-disease validity, variant pathogenicity, dosage sensitivity, and clinical actionability. Data is freely accessible via web interface, bulk file downloads (CSV, TSV, JSON, BED), FTP server, and REST APIs. All content is released under CC0 public domain license with no restrictions. The Allele Registry API provides unique variant identifiers and links variants across databases. ClinGen data represents the gold standard for clinical genomic interpretation, with FDA recognition and global expert panel curation involving 2,700+ contributors from 72+ countries.
