# GenCC (Gene Curation Coalition)

## Overview

GenCC is a global collaborative effort to harmonize gene-disease validity curation across different international resources. The Gene Curation Coalition standardizes terminology and creates a shared database of gene-disease relationships, with a primary focus on Mendelian diseases. GenCC brings together 17 member organizations including research resources, databases, and diagnostic laboratories to provide consistent, expert-curated gene-disease validity assertions.

**Website**: https://thegencc.org
**Search Portal**: https://search.thegencc.org
**Download Page**: https://search.thegencc.org/download
**Version**: Current/Latest (periodic updates from member submissions)

## Data Types

GenCC provides a single, focused data type:

### Gene-Disease Validity Assertions

**Purpose:** Standardized expert curations of the validity of gene-disease relationships

**Content:**
- Gene-disease associations
- Clinical validity classifications
- Mode of inheritance
- Supporting evidence and references
- Submitter information
- Assertion criteria and methodology

**Focus:** Primarily Mendelian (monogenic) diseases

**Scope:**
- Each entry represents one assertion linking:
  - A specific gene
  - A specific disease
  - A mode of inheritance
  - Supporting evidence

### Standardized Validity Classifications

GenCC uses 8 harmonized classification terms agreed upon through a Delphi survey:

1. **Definitive**: Gene-disease relationship is well-established
2. **Strong**: Strong evidence supports gene-disease relationship
3. **Moderate**: Moderate evidence supports gene-disease relationship
4. **Limited**: Limited evidence for gene-disease relationship
5. **Disputed Evidence**: Evidence conflicts regarding gene-disease relationship
6. **Refuted Evidence**: Gene-disease relationship has been refuted
7. **Animal Model Only**: Evidence exists only in animal models
8. **No Known Disease Relationship**: No evidence of gene-disease relationship

**Classification Basis:** Strength of human evidence supporting the gene-disease connection

### Disease Ontology Mapping

**Standard:** Diseases mapped to Monarch Disease Ontology (MONDO)
- Provides consistent disease identifiers
- Enables cross-resource integration
- Supports computational analysis

## Member Organizations

GenCC aggregates curations from 17 member organizations:

### Research Resources
- **ClinGen** (Clinical Genome Resource)
- **DECIPHER** (Database of Chromosomal Imbalance and Phenotype in Humans using Ensembl Resources)
- **Genomics England PanelApp**
- **OMIM** (Online Mendelian Inheritance in Man)
- **Orphanet** (Rare diseases and orphan drugs)

### Diagnostic Laboratories
- **Ambry Genetics**
- **Illumina**
- **Invitae**
- **Myriad Women's Health**
- **Mass General Brigham Laboratory for Molecular Medicine**

### Additional Contributing Organizations
Organizations that perform gene-level curations and share content publicly according to curation standards

## Access Methods

### 1. Web Interface

**Search Portal**: https://search.thegencc.org

**Features:**
- Search by gene symbol, disease name, submitter, or classification
- Filter by:
  - Gene symbol
  - Disease
  - Submitter organization
  - Mode of inheritance
  - Clinical validity classification
- View individual gene-disease assertions
- Access supporting evidence and publications
- Links to member organization details

**Upcoming Features:**
- Ability to follow specific genes
- Search using previous gene symbols

### 2. Data Downloads

**Download Page**: https://search.thegencc.org/download

#### Available File Formats

**All formats contain identical data:**
1. **Excel (.xlsx)** - Modern Excel format
2. **Excel Legacy (.xls)** - Older Excel format
3. **Tab-Separated Values (.tsv)** - Plain text, tab-delimited
4. **Comma-Separated Values (.csv)** - Plain text, comma-delimited

#### Download Process

1. Navigate to download page
2. Select desired format
3. Direct download (no authentication required)
4. Files contain complete database snapshot

### 3. UCSC Genome Browser Integration

**Access:** GenCC track available in UCSC Genome Browser
**Genome Builds:** hg19 (GRCh37) and hg38 (GRCh38)
**Schema**: https://genome.ucsc.edu/cgi-bin/hgTables?db=hg38&hgta_group=phenDis&hgta_track=genCC&hgta_table=genCC&hgta_doSchema=describe+table+schema

**Features:**
- Visualize gene-disease associations in genomic context
- Integrate with other UCSC tracks
- Query via UCSC Table Browser

### 4. API Access

**Status:** Coming soon (as of 2025)

**Interest Registration:** Users can sign up at thegencc.org to be notified when API access or early access becomes available

**Expected Features:**
- Programmatic data retrieval
- Query by gene, disease, or classification
- Integration into clinical annotation pipelines

### 5. Example Download and Usage

#### Download via Command Line
```bash
# Download TSV format
curl -o gencc_data.tsv https://search.thegencc.org/download/gencc.tsv

# Download CSV format
wget https://search.thegencc.org/download/gencc.csv
```

#### Load into Python (Pandas)
```python
import pandas as pd

# Load GenCC data
gencc = pd.read_csv('gencc_data.tsv', sep='\t')

# Filter for Definitive classifications
definitive = gencc[gencc['classification_label'] == 'Definitive']

# Find all genes for a specific disease
disease_genes = gencc[gencc['disease_label'].str.contains('Cardiomyopathy', na=False)]

# Count assertions by submitter
submitter_counts = gencc['submitter_label'].value_counts()

print(f"Total assertions: {len(gencc)}")
print(f"Definitive classifications: {len(definitive)}")
```

#### Load into R
```r
library(readr)

# Load GenCC data
gencc <- read_tsv("gencc_data.tsv")

# Filter by classification
strong_evidence <- gencc[gencc$classification_label %in% c("Definitive", "Strong"), ]

# Summarize by mode of inheritance
inheritance_summary <- table(gencc$moi_label)

# Export subset for specific genes
brca_genes <- gencc[grepl("BRCA", gencc$gene_symbol), ]
write_csv(brca_genes, "brca_gencc_assertions.csv")
```

## Cost and Requirements

### Cost
**FREE** - GenCC is completely free to use
- No subscription fees
- No registration required for access
- No usage limits
- No authentication needed for downloads

### License
**CC0 1.0 Universal (Public Domain Dedication)**
- Most permissive open license
- No legal restrictions on use
- Data placed in public domain
- Free for any purpose including commercial use
- No permission required

### Attribution
- **Not legally required** (due to CC0 license)
- **Recommended**: Provide attribution to GenCC and contributing sources when possible
- **Suggested Citation**: "The Gene Curation Coalition. https://thegencc.org [date accessed]"

### Registration
- **Not required** for browsing, searching, or downloading
- **Optional**: Sign up for API access notifications

### Important Notes

**OMIM Data Exclusion:**
- GenCC downloads do NOT include OMIM data due to licensing restrictions
- OMIM data must be accessed separately at https://www.omim.org

**Not for Direct Clinical Use:**
- Data not intended for direct diagnostic use or medical decision-making
- Should be reviewed by qualified genetics professionals
- Represents periodic submissions; may not be fully up-to-date at all times

## Data Structure

### Database Fields/Columns

GenCC downloads contain the following key fields:

#### Core Identifiers

**GenCC Submission ID:**
- Unique identifier for each assertion
- Links to specific curation in GenCC database

**Gene Information:**
- `gene_id`: Gene identifier (typically HGNC ID)
- `gene_symbol`: HGNC gene symbol (e.g., BRCA1, TP53)

**Disease Information:**
- `disease_id`: Disease identifier (primarily MONDO IDs)
- `disease_label`: Human-readable disease name

#### Classification

**Clinical Validity:**
- `classification_id`: Classification identifier
- `classification_label`: One of 8 standardized terms:
  - Definitive
  - Strong
  - Moderate
  - Limited
  - Disputed Evidence
  - Refuted Evidence
  - Animal Model Only
  - No Known Disease Relationship

#### Mode of Inheritance

**Inheritance Pattern:**
- `moi_id`: Mode of inheritance identifier
- `moi_label`: Inheritance pattern description
  - Autosomal dominant
  - Autosomal recessive
  - X-linked dominant
  - X-linked recessive
  - Mitochondrial
  - Other patterns

#### Submitter Information

**Source Organization:**
- `submitter_id`: Submitter organization identifier
- `submitter_label`: Organization name (e.g., ClinGen, DECIPHER, Invitae)

#### Evidence and Documentation

**Supporting Information:**
- `public_report_url`: Link to detailed curation report
- `submission_notes`: Additional notes from submitter
- `assertion_criteria_url`: Link to criteria/methodology used
- `submission_pmids`: PubMed IDs supporting assertion (comma-separated)

#### Temporal Information

**Dates:**
- Date fields related to submission and updates (specific field names may vary)
- Dates provide temporal context for assertions

### File Format Structure

#### TSV/CSV Format Example

```
gencc_submission_id  gene_id      gene_symbol  disease_id         disease_label                     classification_label  moi_label              submitter_label
GC-1234567          HGNC:1100    BRCA1        MONDO:0007254      Breast-ovarian cancer syndrome   Definitive            Autosomal dominant     ClinGen
GC-1234568          HGNC:11998   TP53         MONDO:0016419      Li-Fraumeni syndrome             Definitive            Autosomal dominant     ClinGen
GC-1234569          HGNC:3467    CFTR         MONDO:0009061      Cystic fibrosis                  Definitive            Autosomal recessive    Orphanet
```

### Data Curation Process

**Methodology:**
1. Member organizations curate gene-disease relationships using internal standards
2. Curations mapped to GenCC standardized terminology
3. Diseases mapped to MONDO ontology
4. Periodic data submissions to GenCC
5. Aggregation and public release

**Quality Assurance:**
- Expert curation by genetics professionals
- Evidence-based classifications
- Standardized criteria application
- Peer review within member organizations

### Database Characteristics

**Coverage:**
- Focuses on Mendelian diseases
- Includes both well-established and emerging gene-disease relationships
- Represents consensus and individual organization perspectives

**Update Frequency:**
- Periodic submissions from member organizations
- Database updated as new curations become available
- Not real-time; some delay between organization curation and GenCC release

**Heterogeneity:**
- Different submitters may have different assertions for same gene-disease pair
- Multiple entries possible for single gene-disease combination
- Users should evaluate evidence and submitter when conflicting classifications exist

## Integration with Other Resources

### Cross-Database Links

**Integrated Resources:**
- **MONDO**: Disease ontology mapping
- **HGNC**: Gene nomenclature
- **UCSC Genome Browser**: Genomic visualization
- **PubMed**: Literature evidence
- **Member Organizations**: Detailed curation reports via public_report_url

**Use in Pipelines:**
- Clinical annotation workflows
- Variant interpretation pipelines
- Research databases
- Genetic testing panels

## Membership and Contribution

### Joining GenCC

**Eligibility:**
- Organizations performing gene-level curations
- Commitment to public data sharing
- Adherence to curation standards

**Process:**
- Contact GenCC via website
- Review membership criteria
- Submit application

### Individual Submissions

**Status:** GenCC does not currently accept individual submissions

**Rationale:** Focus on aggregating curations from established, expert organizations

## Additional Resources

- **Published Research**: Rehm HL, et al. The Gene Curation Coalition: A global effort to harmonize gene-disease evidence resources. *Genetics in Medicine*. 2022. PMID: 35507016
- **Conference Presentations**: Presented at ACMG, GA4GH Plenary, International Biocuration Society Conference
- **FAQ**: https://thegencc.org/faq
- **About**: https://thegencc.org/about.html

## Summary

GenCC is a global coalition of 17 organizations harmonizing gene-disease validity curation with standardized 8-level classification system (Definitive, Strong, Moderate, Limited, Disputed, Refuted, Animal Model Only, No Known Disease Relationship). Data is **completely free** under **CC0 public domain license** with no registration required. Available as downloadable files in XLSX, XLS, TSV, and CSV formats. Focuses on Mendelian diseases with diseases mapped to MONDO ontology. Data includes gene-disease assertions, mode of inheritance, submitter organization, supporting evidence (PMIDs), and links to detailed reports. API access coming soon. Note: OMIM data excluded due to licensing restrictions. Essential resource for clinical genomics, variant interpretation, and gene panel development, though not intended for direct diagnostic use without professional review.
