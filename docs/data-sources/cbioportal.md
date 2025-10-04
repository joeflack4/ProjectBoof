# cBioPortal for Cancer Genomics

## Overview

cBioPortal is an open-source, open-access platform for exploring, visualizing, and analyzing multidimensional cancer genomics data. It provides an intuitive web interface and comprehensive API for researchers to access large-scale cancer genomics datasets from various studies and institutions.

**Website**: https://www.cbioportal.org
**Documentation**: https://docs.cbioportal.org
**GitHub**: https://github.com/cbioportal/cbioportal
**Version**: Current/Latest (as of 2025)

## Data Types

cBioPortal is a multimodal cancer data visualization tool supporting various data types:

### Molecular Data Types

1. **Bulk DNA Sequencing**
   - Mutations (somatic mutations, germline variants)
   - Copy Number Alterations (CNAs)
   - Structural Variants (fusions, translocations)
   - Mutational Signatures

2. **Bulk RNA Sequencing**
   - Gene Expression (mRNA expression levels)

3. **Other Molecular Data**
   - DNA Methylation
   - Protein Expression (RPPA, mass spectrometry)
   - Genetic Ancestry

### Clinical Data

- Patient-level clinical attributes (demographics, diagnoses)
- Sample-level clinical attributes (tumor type, stage, grade)
- Treatment timeline data
- Cancer type categorization using Oncotree ontology
- Free-form, de-identified clinical annotations

### External Viewer Integration

Supports linking to external viewers for specialized data types:
- Single-cell RNA/DNA/ATAC sequencing
- Spatial transcriptomics (GeoMx, CyCIF)
- Imaging data (H&E slides, CT scans)

## Access Methods

### 1. Web Interface

**URL**: https://www.cbioportal.org

Interactive web portal for browsing, querying, and visualizing cancer genomics data through a graphical interface.

### 2. Web API (REST API)

**Base URL**: https://www.cbioportal.org/api/v3
**API Documentation**: https://www.cbioportal.org/api/swagger-ui/index.html
**Specification**: OpenAPI/Swagger

#### Key API Endpoint Categories

- **Cancer Types**: Browse cancer type classifications
- **Studies**: Access study metadata and available datasets
- **Patients**: Retrieve patient-level data
- **Samples**: Access sample-level information
- **Molecular Profiles**: Query available molecular data types per study
- **Mutations**: Retrieve mutation data
- **Discrete Copy Number Alterations**: Access CNA data
- **Molecular Data**: Fetch expression, methylation, and protein data
- **Clinical Data**: Retrieve clinical attributes and annotations
- **Clinical Events**: Access treatment and outcome timelines
- **Gene Panels**: Information about sequencing panels used
- **Genes**: Gene-level annotations and metadata
- **Sample Lists**: Predefined or custom sample cohorts

#### Example API Queries

**Python (using bravado):**
```python
from bravado.client import SwaggerClient

# Initialize client
cbioportal = SwaggerClient.from_url(
    'https://www.cbioportal.org/api/v3/api-docs'
)

# Get all cancer studies
studies = cbioportal.Studies.getAllStudiesUsingGET().result()

# Get mutations for a specific study
mutations = cbioportal.Mutations.getMutationsInMolecularProfileBySampleListIdUsingGET(
    molecularProfileId="msk_impact_2017_mutations",
    sampleListId="msk_impact_2017_all",
    projection="DETAILED"
).result()
```

**R (using cbioportalR):**
```r
library(cbioportalR)

# Set database connection
set_cbioportal_db("public")

# Get available studies
studies <- get_studies()

# Get mutations for specific samples
mutations <- get_mutations_by_sample(
  study_id = "msk_impact_2017",
  sample_id = c("P-0001234-T01-IM3", "P-0005678-T01-IM5")
)

# Get clinical data
clinical <- get_clinical_by_study(study_id = "msk_impact_2017")
```

**R (using cBioPortalData - MultiAssayExperiment):**
```r
library(cBioPortalData)

# Connect to cBioPortal
cbio <- cBioPortal()

# Download study as MultiAssayExperiment
mae <- cBioPortalData(
  api = cbio,
  studyId = "msk_impact_2017",
  genePanelId = "IMPACT468"
)
```

#### Authentication

- **Public instance**: No authentication required for public datasets
- **Private instances**: Token-based authentication
  ```r
  # Example for authenticated access
  cbio_private <- cBioPortal(
    hostname = 'genie.cbioportal.org',
    token = '~/Downloads/cbioportal_data_access_token.txt'
  )
  ```

### 3. Direct Data Download

#### Datasets Page
- **URL**: https://www.cbioportal.org/datasets
- Each study available as downloadable ZIP file
- Contains all molecular and clinical data files

#### DataHub Git Repository
- **URL**: https://github.com/cBioPortal/datahub
- Git LFS repository with all study data
- Extracted versions of ZIP files from datasets page

#### MySQL Database Dump
- **URL**: https://public-db-dump.assets.cbioportal.org/
- Complete database dump of cbioportal.org
- Includes cancer types, genes, UniProt mappings, drug information
- Useful for seeding new cBioPortal instances

### 4. API Clients

#### R Clients
1. **cbioportalR** (Recommended)
   - Tidyverse-compatible
   - User-friendly functions for data retrieval
   - CRAN package

2. **cBioPortalData** (Recommended)
   - Returns MultiAssayExperiment objects
   - Automatic local caching
   - Bioconductor package

3. **cgdsr** (Legacy)
   - CRAN package for older CGDS API

#### Python Clients
1. **bravado**
   - Direct Swagger client generation
   - Supports authenticated and unauthenticated access

2. **cbio_py**
   - Simple API wrapper

#### MATLAB
- **CGDS Cancer Genomics Toolbox**
- Available on MATLAB Central File Exchange

## Cost and Requirements

### Cost
**FREE** - cBioPortal is completely free to use
- No subscription fees
- No usage limits on public instance
- Open-access to all public datasets

### Registration
- **Not required** for browsing public data via web interface
- **Not required** for API access to public datasets
- **May be required** for private institutional instances

### License
- **Software**: GNU Affero General Public License v3 (AGPL v3)
- **Open source**: Full source code available on GitHub
- **Commercial use**: Allowed, but modifications must be shared (AGPL requirement)
- **Self-hosting**: Permitted for private data

### Important Notes
- OncoKB integration within cBioPortal may require separate OncoKB licensing for commercial use
- Public instance hosted by Memorial Sloan Kettering Cancer Center
- Private instances can be deployed for institutional data

## Data Structure

### File Organization

cBioPortal studies are organized as directories containing data files with accompanying metadata files.

#### Study Directory Structure
```
study_directory/
├── meta_study.txt              # Study metadata
├── meta_cancer_type.txt        # Cancer type definition
├── cancer_type.txt             # Cancer type data
├── meta_clinical_patient.txt   # Patient clinical metadata
├── data_clinical_patient.txt   # Patient clinical data
├── meta_clinical_sample.txt    # Sample clinical metadata
├── data_clinical_sample.txt    # Sample clinical data
├── meta_mutations.txt          # Mutation metadata
├── data_mutations.txt          # Mutation data
├── meta_CNA.txt                # CNA metadata
├── data_CNA.txt                # CNA data
├── meta_expression.txt         # Expression metadata
├── data_expression.txt         # Expression data
└── case_lists/                 # Sample list definitions
    ├── cases_all.txt
    ├── cases_sequenced.txt
    └── cases_cna.txt
```

### File Formats

#### Primary Format
- **Tab-separated values (TSV)** for all data and metadata files
- UTF-8 encoding
- Headers define column names

#### Metadata Files
- Prefix or suffix with 'meta' (e.g., `meta_study.txt`, `meta.txt`, `study.meta`)
- Define data file properties and types
- Required fields vary by data type

#### Data Files
- Referenced by `data_filename` property in metadata file
- Specific column requirements per data type
- Support custom annotations

### Major Data File Types and Key Fields

#### 1. Study Metadata (`meta_study.txt`)
Key fields:
- `type_of_cancer`: Cancer type identifier
- `cancer_study_identifier`: Unique study ID
- `name`: Study display name
- `description`: Study description
- `citation`: Publication reference (optional)
- `pmid`: PubMed ID (optional)
- `groups`: Access groups (optional)
- `reference_genome`: Reference genome build (e.g., hg19, hg38)

#### 2. Clinical Data Files

**Patient Data (`data_clinical_patient.txt`)**
Key fields:
- `PATIENT_ID`: Unique patient identifier (required)
- `SEX`: Patient sex
- `AGE`: Age at diagnosis
- `OS_STATUS`: Overall survival status
- `OS_MONTHS`: Overall survival time
- Custom clinical attributes

**Sample Data (`data_clinical_sample.txt`)**
Key fields:
- `PATIENT_ID`: Links to patient (required)
- `SAMPLE_ID`: Unique sample identifier (required)
- `CANCER_TYPE`: Cancer type
- `CANCER_TYPE_DETAILED`: Detailed cancer subtype
- `SAMPLE_TYPE`: Primary, Metastatic, etc.
- `TUMOR_STAGE`: Tumor staging
- Custom sample attributes

#### 3. Mutation Data (`data_mutations.txt`)

Key fields:
- `Hugo_Symbol`: Gene symbol
- `Entrez_Gene_Id`: NCBI gene ID
- `Chromosome`: Chromosome location
- `Start_Position`: Genomic start position
- `End_Position`: Genomic end position
- `Reference_Allele`: Reference allele
- `Tumor_Seq_Allele1`: Tumor allele 1
- `Tumor_Seq_Allele2`: Tumor allele 2
- `Variant_Classification`: Mutation type (Missense, Nonsense, etc.)
- `Variant_Type`: SNP, INS, DEL
- `Tumor_Sample_Barcode`: Sample identifier
- `Protein_Change`: Protein change notation
- `HGVSp_Short`: HGVS protein notation

#### 4. Copy Number Alteration Data (`data_CNA.txt`)

Matrix format:
- Rows: Genes (Hugo_Symbol, Entrez_Gene_Id)
- Columns: Sample IDs
- Values: -2 (deep deletion), -1 (shallow deletion), 0 (diploid), 1 (gain), 2 (amplification)

#### 5. Gene Expression Data (`data_expression.txt`)

Matrix format:
- Rows: Genes (Hugo_Symbol, Entrez_Gene_Id)
- Columns: Sample IDs
- Values: Expression levels (log2-transformed, z-scores, or RPKM/TPM)

#### 6. Structural Variant/Fusion Data (`data_fusions.txt`)

Key fields:
- `Hugo_Symbol`: Gene symbol
- `Entrez_Gene_Id`: Gene ID
- `Tumor_Sample_Barcode`: Sample ID
- `Fusion`: Fusion description
- `DNA_support`: YES/NO
- `RNA_support`: YES/NO
- `Method`: Detection method

#### 7. Copy Number Segments (`data_segments.txt`)

Key fields:
- `ID`: Sample ID
- `chrom`: Chromosome
- `loc.start`: Segment start position
- `loc.end`: Segment end position
- `num.mark`: Number of probes/markers
- `seg.mean`: Segment mean (log2 ratio)

### Database Schema

For the MySQL database backend:
- **Studies table**: Study metadata
- **Patients table**: Patient information
- **Samples table**: Sample information
- **Genetic profiles**: Molecular profile types per study
- **Mutations**: Mutation annotations
- **CNA events**: Copy number alterations
- **Clinical data**: Patient and sample attributes
- **Gene table**: Gene annotations from NCBI/Ensembl
- **Cancer types**: Oncotree classifications

Access full database schema via MySQL dump at: https://public-db-dump.assets.cbioportal.org/

## Additional Resources

- **User Guide**: https://docs.cbioportal.org/user-guide/
- **FAQ**: https://docs.cbioportal.org/user-guide/faq/
- **Tutorials**: Available on documentation site
- **Community Support**: Google Group (https://groups.google.com/g/cbioportal)
- **Issue Tracker**: https://github.com/cbioportal/cbioportal/issues
- **Blog**: https://blog.cbioportal.org/

## Summary

cBioPortal provides comprehensive access to cancer genomics data through multiple channels (web, API, bulk download), supports diverse molecular and clinical data types, is completely free and open source, and offers robust API clients in R, Python, and MATLAB for programmatic access. The platform uses standardized TSV file formats with flexible metadata structure, making it suitable for both individual research queries and large-scale data integration projects.
