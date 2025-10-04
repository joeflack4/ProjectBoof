# TCGA (The Cancer Genome Atlas)

## Overview

The Cancer Genome Atlas (TCGA) is a landmark cancer genomics program that molecularly characterized over 20,000 primary cancer and matched normal samples spanning 33 cancer types. Started by the National Cancer Institute (NCI) and the National Human Genome Research Institute (NHGRI), TCGA generated comprehensive, multi-dimensional maps of the key genomic changes in major types and subtypes of cancer. TCGA data is now housed and distributed through the NCI's Genomic Data Commons (GDC), which provides harmonized genomic data, analysis tools, and programmatic access.

**Website**: https://www.cancer.gov/ccg/research/genome-sequencing/tcga
**GDC Portal**: https://portal.gdc.cancer.gov
**GDC Website**: https://gdc.cancer.gov
**GDC API**: https://api.gdc.cancer.gov
**Documentation**: https://docs.gdc.cancer.gov
**Version**: Current/Latest (continuous updates through GDC)

**Database Statistics:**
- >20,000 tumor and matched normal samples
- 33 cancer types
- Multiple molecular characterization platforms
- Petabytes of genomic data
- >11,000 patients

## Data Types

TCGA collected multiple types of data for each sample, now available through the GDC:

### 1. Clinical Data

**Content:**
- Demographic information (age, sex, race, ethnicity)
- Exposure history (smoking, alcohol, environmental)
- Treatment details (therapies, surgeries, radiation)
- Survival outcomes (overall survival, disease-free survival)
- Pathology reports and classifications
- Vital status and follow-up information
- Tumor stage and grade
- Cancer diagnosis and histology

**Format:** TSV, JSON, XML

**Access:** Open Access (de-identified)

### 2. Biospecimen Data

**Content:**
- Sample metadata
- Tissue source site information
- Sample type (primary tumor, metastatic, normal)
- Specimen collection details
- Aliquot and analyte information
- Preservation method
- Pathology annotations

**Format:** TSV, JSON, XML

**Access:** Open Access

### 3. Genomic Sequencing Data

#### DNA Sequencing

**Whole Exome Sequencing (WXS):**
- Somatic mutations
- Germline variants
- Coverage and quality metrics

**Whole Genome Sequencing (WGS):**
- Comprehensive genomic alterations
- Structural variants
- Non-coding variants

**Targeted Sequencing:**
- Gene panel sequencing
- Focused mutation analysis

**Formats:**
- Raw: FASTQ, BAM
- Processed: VCF, MAF (Mutation Annotation Format)

**Access:**
- Raw data (BAM, FASTQ): Controlled Access
- Somatic mutations (MAF, VCF): Open Access
- Germline variants: Controlled Access

#### RNA Sequencing

**RNA-Seq:**
- Gene expression quantification
- Transcript abundance
- Alternative splicing
- Fusion detection

**miRNA-Seq:**
- microRNA expression profiling
- Small RNA analysis

**Formats:**
- Raw: FASTQ, BAM
- Processed: TSV (counts, TPM, FPKM)

**Access:**
- Raw data: Controlled Access
- Gene/miRNA expression: Open Access

### 4. Copy Number Analysis

**Content:**
- DNA copy number alterations
- Amplifications and deletions
- Allele-specific copy number
- Segmentation data

**Platforms:**
- SNP arrays
- Array comparative genomic hybridization (aCGH)
- Low-pass whole genome sequencing

**Formats:**
- Segmentation files (SEG)
- Array data (CEL, IDAT)
- VCF

**Access:** Open Access (processed); Controlled (raw array data)

### 5. DNA Methylation

**Content:**
- CpG methylation profiling
- Methylation beta values
- Differentially methylated regions
- Epigenetic alterations

**Platforms:**
- Illumina HumanMethylation450 (450K)
- Illumina MethylationEPIC (850K)
- Whole-genome bisulfite sequencing (WGBS)

**Formats:**
- IDAT (raw array data)
- TXT/TSV (processed beta values)

**Access:** Open Access (processed); Controlled (raw)

### 6. Protein Expression

**Reverse Phase Protein Array (RPPA):**
- Protein abundance
- Phosphorylation states
- Pathway activation

**Content:**
- >200 antibodies
- Quantitative protein measurements
- Post-translational modifications

**Format:** TSV

**Access:** Open Access

### 7. Imaging Data

**Diagnostic Whole Slide Images:**
- H&E stained tissue sections
- High-resolution digital pathology
- Frozen and FFPE samples

**Radiological Images (select cases):**
- MRI
- CT scans
- PET imaging

**Formats:**
- SVS (Aperio)
- DICOM

**Access:** Open Access (whole slide images)

### 8. Derived Data Products

**Pan-Cancer Analyses:**
- PanCanAtlas publications and datasets
- Integrated multi-omic analyses
- Pathway and network analyses

**Harmonized Data:**
- GDC-aligned BAMs (GRCh38)
- Standardized variant calls
- Unified gene expression quantification

## Access Methods

All TCGA data is now accessed through the NCI Genomic Data Commons (GDC):

### 1. GDC Data Portal (Web Interface)

**URL**: https://portal.gdc.cancer.gov

**Features:**
- Interactive data exploration
- Faceted search and filtering
- Cohort building and analysis
- Visualization tools
- Data download via manifest generation
- No login required for open access data

**Search Capabilities:**
- By project (TCGA, TARGET, etc.)
- By cancer type
- By data type
- By experimental strategy
- By case/sample/file IDs

**Analysis Tools:**
- Cohort comparison
- Survival analysis
- Gene/mutation frequency
- OncoGrid visualizations

### 2. GDC Data Transfer Tool (Command Line)

**Repository**: https://github.com/NCI-GDC/gdc-client
**Documentation**: https://docs.gdc.cancer.gov/Data_Transfer_Tool/Users_Guide/

#### Installation

Download binary for your platform:
- Linux
- macOS
- Windows

Recommended: Add to system PATH

#### Basic Usage

**Download using manifest file (recommended for multiple files):**
```bash
# Generate manifest from GDC Portal, then:
gdc-client download -m gdc_manifest.txt
```

**Download using file UUIDs:**
```bash
gdc-client download 22a29915-6712-4f7a-8dba-985ae9a1f005
```

**Download controlled access data (requires authentication token):**
```bash
gdc-client download -m gdc_manifest.txt -t gdc-user-token.txt
```

**Resume interrupted downloads:**
```bash
# Simply repeat the download command in the same directory
gdc-client download -m gdc_manifest.txt
```

#### Key Features
- Optimized transfer speeds
- Automatic resumption of interrupted transfers
- Multi-threaded downloads
- MD5 checksum verification

### 3. GDC API (Programmatic Access)

**Base URL**: https://api.gdc.cancer.gov

**Documentation**: https://docs.gdc.cancer.gov/API/Users_Guide/

#### Main Endpoints

- `/files` - Query and retrieve file metadata
- `/cases` - Query patient/case information
- `/projects` - Access project-level data (TCGA, TARGET, etc.)
- `/annotations` - Retrieve annotations and notes
- `/_mapping` - Discover available fields and filters
- `/data` - Download files by UUID

#### Python Examples

**Basic query for files:**
```python
import requests
import json

# Query files endpoint
files_endpt = 'https://api.gdc.cancer.gov/files'

# Filters for TCGA lung adenocarcinoma RNA-Seq data
filters = {
    "op": "and",
    "content": [
        {
            "op": "=",
            "content": {
                "field": "cases.project.project_id",
                "value": "TCGA-LUAD"
            }
        },
        {
            "op": "=",
            "content": {
                "field": "files.experimental_strategy",
                "value": "RNA-Seq"
            }
        },
        {
            "op": "=",
            "content": {
                "field": "files.data_format",
                "value": "BAM"
            }
        }
    ]
}

params = {
    "filters": json.dumps(filters),
    "fields": "file_id,file_name,cases.submitter_id,file_size",
    "format": "JSON",
    "size": "100"
}

response = requests.get(files_endpt, params=params)
data = response.json()

print(f"Total files: {data['data']['pagination']['total']}")
for hit in data['data']['hits']:
    print(f"{hit['file_name']}: {hit['file_size']} bytes")
```

**Download files using API:**
```python
import requests

# List of file UUIDs to download
file_uuids = ['22a29915-6712-4f7a-8dba-985ae9a1f005']

data_endpt = 'https://api.gdc.cancer.gov/data'

params = {'ids': file_uuids}

response = requests.post(data_endpt,
                        data=json.dumps(params),
                        headers={"Content-Type": "application/json"})

# Save to file
with open("downloaded_file.tar.gz", "wb") as f:
    f.write(response.content)
```

#### R Package (GenomicDataCommons)

**Bioconductor Package**: GenomicDataCommons

**Installation:**
```r
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("GenomicDataCommons")
```

**Example Usage:**
```r
library(GenomicDataCommons)

# Check GDC status
status()

# Query projects
projects <- projects()

# Query TCGA-BRCA files
qfiles <- files() %>%
  filter(~ cases.project.project_id == 'TCGA-BRCA' &
         data_type == 'Gene Expression Quantification') %>%
  select(c('file_name', 'cases.submitter_id', 'file_size'))

# Execute query
results <- results(qfiles)

# Download files (requires manifest or UUIDs)
fnames <- gdcdata(results$file_id[1:5])
```

### 4. Alternative Access Points

#### cBioPortal

**URL**: https://www.cbioportal.org

Provides integrated TCGA data with visualization and analysis tools

#### UCSC Xena

**URL**: https://xenabrowser.net

TCGA data with visualization and cohort analysis

#### Google Cloud Platform

**Resource**: TCGA data available as BigQuery tables and Cloud Storage

**URL**: https://cloud.google.com/life-sciences/docs/resources/public-datasets/tcga

#### ISB Cancer Genomics Cloud

**URL**: https://isb-cancer-genomics-cloud.readthedocs.io

Cloud-based TCGA data access and analysis

## Cost and Requirements

### Cost
**FREE** - All TCGA/GDC data access is completely free
- No subscription fees
- No download charges
- No API usage limits
- No storage fees for downloaded data

### Access Tiers

#### Open Access Data

**Content:**
- Somatic mutation data (MAF files)
- Gene expression data
- Clinical and biospecimen data
- Copy number segmentation
- DNA methylation (processed)
- Protein expression (RPPA)
- Derived data products

**Requirements:**
- No registration required
- No authentication needed
- Immediate download access

#### Controlled Access Data

**Content:**
- Raw sequencing data (BAM, FASTQ)
- Germline variant calls
- SNP genotypes
- Individual-level data that could identify participants
- Raw microarray data (some types)

**Requirements:**
- **NIH eRA Commons account** (required)
- **dbGaP authorization** (granted by NIH Data Access Committee)
- Research use limitation compliance
- Data use certification
- Institutional approval

**Authorization Process:**
1. Create NIH eRA Commons account
2. Submit Data Access Request through dbGaP (https://dbgap.ncbi.nlm.nih.gov)
3. Specify research use
4. Obtain institutional approval
5. Await DAC (Data Access Committee) decision
6. Download authentication token from GDC
7. Use token with GDC Data Transfer Tool or API

### License and Data Use

**Data Use:**
- Open for research purposes
- Publication allowed with attribution
- Commercial use permitted for research
- Clinical use requires appropriate validation

**Attribution:**
- **Required**: Cite TCGA in publications
- Recommended citation: Cancer Genome Atlas Research Network publications specific to cancer type
- Acknowledge NCI and NHGRI funding

**Data Use Limitations:**
- Cannot attempt to identify individual participants
- Controlled access data restricted to approved research use
- Must comply with dbGaP data use certification

## Data Structure

### GDC Data Model

Data organized hierarchically:
1. **Program** (e.g., TCGA, TARGET)
2. **Project** (e.g., TCGA-BRCA, TCGA-LUAD)
3. **Case** (patient/participant)
4. **Sample** (tumor, normal)
5. **Aliquot** (portion used in assay)
6. **Read Group** (sequencing run)
7. **File** (data file)

### TCGA Project Codes

33 cancer types with project codes like:
- **TCGA-BRCA**: Breast Invasive Carcinoma
- **TCGA-LUAD**: Lung Adenocarcinoma
- **TCGA-LUSC**: Lung Squamous Cell Carcinoma
- **TCGA-COAD**: Colon Adenocarcinoma
- **TCGA-GBM**: Glioblastoma Multiforme
- **TCGA-OV**: Ovarian Serous Cystadenocarcinoma
- **TCGA-KIRC**: Kidney Renal Clear Cell Carcinoma

(Full list available at GDC Portal)

### File Formats and Key Fields

#### MAF (Mutation Annotation Format)

**Key Fields:**
- `Hugo_Symbol`: Gene symbol
- `Chromosome`: Chromosome
- `Start_Position`: Genomic start
- `End_Position`: Genomic end
- `Variant_Classification`: Mutation type
- `Variant_Type`: SNP, DNP, INS, DEL
- `Reference_Allele`: Reference
- `Tumor_Seq_Allele1/2`: Tumor alleles
- `Tumor_Sample_Barcode`: Sample ID
- `HGVSp_Short`: Protein change
- `FILTER`: Quality filter status

#### Gene Expression (TSV)

**Key Fields:**
- `gene_id`: Ensembl gene ID
- `gene_name`: HGNC symbol
- `gene_type`: Protein coding, lncRNA, etc.
- `unstranded`: Raw counts
- `stranded_first`: First strand counts
- `stranded_second`: Second strand counts
- `tpm_unstranded`: Transcripts per million
- `fpkm_unstranded`: Fragments per kilobase per million

#### Clinical Data (TSV/JSON)

**Key Fields:**
- `case_id`: GDC case UUID
- `submitter_id`: TCGA barcode
- `age_at_diagnosis`: Age in days
- `vital_status`: Alive/Dead
- `days_to_death`: Survival time
- `tumor_stage`: Pathologic stage
- `primary_diagnosis`: Cancer diagnosis
- `tissue_or_organ_of_origin`: Anatomic site
- `prior_treatment`: Yes/No
- `treatment_type`: Chemotherapy, radiation, etc.

#### Copy Number Segments (SEG)

**Columns:**
- Sample ID
- Chromosome
- Start position
- End position
- Num_Probes: Number of probes
- Segment_Mean: Log2 copy number ratio

#### VCF (Variant Call Format)

Standard VCF format with INFO fields for:
- `SOMATIC`: Somatic status
- `SS`: Somatic status code
- `DP`: Read depth
- `AF`: Allele frequency
- Functional annotations

### TCGA Barcodes

**Structure:** TCGA-XX-XXXX-XXX-XXX-XXXX-XX

**Components:**
- Project: TCGA
- Tissue Source Site: 2-character code
- Participant: 4-character ID
- Sample Type: 01 (Primary Tumor), 10 (Normal), 11 (Normal Blood), etc.
- Vial: 2-character
- Portion: 2-character
- Plate: 4-character
- Center: 2-character

### Data Levels (Legacy)

Historical TCGA data levels:
- **Level 1**: Raw data (e.g., FASTQ, unprocessed)
- **Level 2**: Processed (e.g., aligned BAMs)
- **Level 3**: Aggregated/normalized (e.g., gene expression matrices)
- **Level 4**: Integrated analyses

GDC now uses "Harmonized" vs. "Legacy" categories instead

### Reference Genome

**GDC Harmonized Data**: GRCh38 (hg38)
**Legacy TCGA Data**: GRCh37 (hg19)

## Additional Resources

- **TCGA Publications**: https://www.cancer.gov/ccg/research/genome-sequencing/tcga/publications
- **PanCanAtlas**: https://gdc.cancer.gov/about-data/publications/pancanatlas
- **GDC Documentation**: https://docs.gdc.cancer.gov
- **GDC Support**: support@nci-gdc.datacommons.io
- **dbGaP**: https://dbgap.ncbi.nlm.nih.gov
- **Data Use Certification**: https://gdc.cancer.gov/access-data/obtaining-access-controlled-data
- **GDC GitHub**: https://github.com/NCI-GDC
- **Tutorial Videos**: Available on GDC YouTube channel

## Summary

TCGA is a landmark cancer genomics program with >20,000 samples across 33 cancer types, now housed in the NCI Genomic Data Commons (GDC). Data includes clinical, genomic (WXS, WGS, RNA-Seq), epigenomic (methylation), copy number, protein expression (RPPA), and imaging data. **Completely free access** with no fees or registration for open access data (mutations, gene expression, clinical); controlled access data (raw sequencing, germline variants) requires **dbGaP authorization** via NIH eRA Commons account. Access through GDC Data Portal (web interface), GDC Data Transfer Tool (command line), GDC API (REST, supports Python/R), and alternative platforms (cBioPortal, UCSC Xena, Google Cloud). Data formats include BAM, FASTQ, VCF, MAF, TSV, JSON. Harmonized to GRCh38 by GDC. Essential resource for cancer research, precision medicine, and pan-cancer analyses. Must cite TCGA in publications and comply with data use certifications for controlled data.
