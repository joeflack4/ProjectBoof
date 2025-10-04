# COSMIC (Catalogue of Somatic Mutations in Cancer)

## Overview

COSMIC is the world's largest and most comprehensive resource for exploring the impact of somatic mutations in human cancer. Developed and maintained by the Wellcome Sanger Institute, COSMIC contains expert-curated genomic data designed to improve understanding of somatic mutations and their role in cancer development. With 20 years of curation experience, COSMIC provides standardized cancer genomics data to academic, industry, and clinical communities worldwide.

**Website**: https://cancer.sanger.ac.uk/cosmic (Academic)
**Website**: https://www.qiagen.com/cosmic (Commercial via QIAGEN)
**Knowledge Base**: https://www.cosmickb.org
**Current Version**: v102 (as of 2025)
**Email Contact**: cosmic@sanger.ac.uk

**Database Statistics:**
- >1.4 million cancer samples
- >38 million somatic coding mutations
- >750 genes in Cancer Gene Census
- >13,000 clinical trials linked
- Updated biannually (Core COSMIC)
- Quarterly updates (Actionability module)

## Data Types

COSMIC covers all genetic mechanisms by which somatic mutations promote cancer, organized into six specialized data modules:

### 1. Core COSMIC

**Purpose:** Comprehensive cancer genomics dataset

**Content:**
- Somatic coding mutations
- Non-coding mutations
- Mutation descriptions and effects
- Variant annotations
- Sample metadata
- Primary sites and histologies
- Publications (PubMed IDs)

**Data Types:**
- Point mutations (SNVs)
- Small insertions/deletions (indels)
- Substitutions
- Complex mutations
- Gene fusions
- Copy number variants (CNVs)
- Structural variants
- Drug resistance mutations

**Updates:** Biannually

**Recent Growth:** Over the last five quarterly updates, COSMIC added 3.4 million mutations, 93,000 samples, and 1,700 articles, increasing genomic mutations by >17%.

### 2. Cancer Gene Census (CGC)

**Purpose:** Expert-curated catalog of genes driving human cancer

**Content:**
- >750 cancer driver genes
- Gene roles in oncogenesis
- Gene classifications: oncogene, tumor suppressor gene (TSG), and/or fusion gene
- Mutation mechanisms (point mutations, fusions, amplifications, deletions)
- Tissue associations
- Somatic vs germline mutation profiles
- Tier 1 evidence for 75% of genes

**Use Cases:**
- Standard reference in cancer genetics
- Basic research
- Medical reporting
- Pharmaceutical development

### 3. Cancer Mutation Census (CMC)

**Purpose:** Identify coding mutations with highest functional impact

**Content:**
- Statistical analysis of mutation frequency
- Background gene mutation rate comparisons
- Integration of data from multiple sources
- Prioritized mutation lists
- Functional impact predictions

**Approach:** Combines recurrence analysis with multi-source evidence integration to answer "Which coding mutations matter the most?"

### 4. Actionability Module

**Purpose:** Link mutations to available therapies and clinical trials

**Content:**
- Mutation-therapy associations
- >13,000 clinical trials
- >1,000 genetic variants with trial associations
- FDA-approved therapies
- Investigational treatments
- Biomarker-drug relationships

**Updates:** Quarterly

### 5. Cell Lines Project

**Purpose:** Cancer cell line genomic characterization

**Content:**
- Cell line mutations and variants
- Gene expression data
- Cell line metadata
- Model system validation data

### 6. Resistance Mutations

**Purpose:** Track mutations conferring drug resistance

**Content:**
- Therapy resistance variants
- Drug-mutation associations
- Resistance mechanisms
- Clinical resistance data

## Access Methods

### 1. Web Interface

**URL**: https://cancer.sanger.ac.uk/cosmic

**Features:**
- Search by gene, mutation, sample, or publication
- Browse by cancer type, tissue, or histology
- Visualize mutation distributions
- View 3D protein structure with mapped mutations (CGC-3D)
- Filter by mutation type, impact, frequency
- Link to external databases
- Updated regularly

**Registration:** Required (free for academic use)

### 2. Data Downloads

**Download Page**: https://cancer.sanger.ac.uk/cosmic/download

**Access Requirements:**
- User registration with organizational email
- Academic users: Free access after registration
- Commercial users: License agreement required (contact COSMIC commercial team)

**Historical Note:** SFTP server deprecated in August 2018; downloads now via HTTPS endpoints

#### Download Authentication

**Method:** HTTP Authorization header
- Email: COSMIC registered email address
- Password: COSMIC account password

#### Available Data Products

Users can browse and download complete datasets for:
- **Core COSMIC**: Current and 3 previous releases
- **Cell Lines Project**: All versions
- **Actionability**: Quarterly updates
- **Cancer Mutation Census (CMC)**: All releases
- **Cancer Gene Census (CGC)**: All versions

#### File Formats

**1. VCF (Variant Call Format)**
- Genomic variants with precise coordinates
- Available for GRCh37 (hg19) and GRCh38 (hg38)
- Coding and non-coding variants
- INFO fields include gene, strand, HGVS notation, legacy IDs, mutation counts

**Example VCF INFO fields:**
```
GENE=OR4F5_ENST00000641515;
STRAND=+;
LEGACY_ID=COSN23957695;
CDS=c.9+224T>C;
AA=p.?;
HGVSC=ENST00000641515.2:c.9+224T>C;
HGVSG=1:g.65797T>C;
CNT=1
```

**2. TSV (Tab-Separated Values)**
- Coding mutations
- Non-coding mutations
- Structural variants
- Gene fusions
- Gene expression variants
- DNA methylation data
- Resistance mutations

**TSV Content (typical fields):**
- Sample IDs
- Primary sites
- Histologies
- PubMed IDs
- Somatic status
- Resistance mutation status
- Mutation descriptions
- Gene names
- HGVS notation

**3. Documentation Files**
- README files for each data product
- Entity Relationship Diagrams (ERD)
- COSMIC identifier reference lists
- Change logs for each release

### 3. Third-Party Access

#### Google BigQuery

**Provider:** Institute for Systems Biology Cancer Gateway to the Cloud (ISB-CGC)

**Access:** COSMIC data available as BigQuery tables for SQL-based queries

**URL:** https://cloud.google.com/life-sciences/docs/resources/public-datasets/cosmic

**Benefits:**
- Programmatic access via SQL
- Cloud-based analysis
- Integration with other GCP tools
- No local storage requirements

#### QIAGEN Commercial Portal

**URL:** https://digitalinsights.qiagen.com/products-overview/cosmic/

**Purpose:** Commercial licensing and distribution partner

**Target Users:** Commercial, clinical, and pharmaceutical organizations

### 4. API Access

**Note:** COSMIC's primary API capabilities are not extensively documented publicly. Most programmatic access occurs through:
- File downloads via authenticated HTTPS
- BigQuery SQL queries (via ISB-CGC)
- Web interface automation (not officially supported)

**GraphQL/REST API:** The search results reference Cosmic CMS (a different product - a content management system), not the COSMIC cancer database. The cancer COSMIC database does not appear to have a public GraphQL or REST API as of 2025.

### 5. Example Access Patterns

#### Download via cURL (Authenticated)
```bash
# Download COSMIC VCF file (requires authentication)
curl -u "your-email@institution.edu:your-password" \
  -o CosmicCodingMuts.vcf.gz \
  https://cancer.sanger.ac.uk/cosmic/file_download/GRCh38/cosmic/v102/VCF/CosmicCodingMuts.vcf.gz
```

#### Python Download Example
```python
import requests
from requests.auth import HTTPBasicAuth

# Set credentials
email = "your-email@institution.edu"
password = "your-cosmic-password"

# Download file
url = "https://cancer.sanger.ac.uk/cosmic/file_download/GRCh38/cosmic/v102/VCF/CosmicCodingMuts.vcf.gz"
response = requests.get(url, auth=HTTPBasicAuth(email, password))

with open('CosmicCodingMuts.vcf.gz', 'wb') as f:
    f.write(response.content)
```

#### BigQuery SQL Example
```sql
-- Query COSMIC mutations in BRAF gene (via ISB-CGC)
SELECT
  Gene_name,
  Mutation_AA,
  Primary_site,
  Primary_histology,
  COUNT(*) as sample_count
FROM
  `isb-cgc.COSMIC.grch38_v92`
WHERE
  Gene_name = 'BRAF'
GROUP BY
  Gene_name, Mutation_AA, Primary_site, Primary_histology
ORDER BY
  sample_count DESC
LIMIT 100
```

## Cost and Requirements

### Cost Structure

#### Academic/Non-Profit Access
**FREE** for qualifying organizations
- Educational institutions
- Non-profit research organizations
- Government research facilities

**Requirements:**
- Registration with organizational email
- Use limited to research and education
- Cannot create commercial products/services
- Cannot use for clinical reporting (commercial setting)

#### Commercial Access
**PAID LICENSE REQUIRED** for:
- Research and development in commercial settings
- Creating commercial products or services
- Patient services or clinical reporting
- Using data in product specifications
- Reference materials for commercial purposes

**Licensing:**
- Administered by QIAGEN (exclusive commercial distribution partner)
- Fees vary based on organization size and intended use
- Annual subscription model
- Fees waived for companies collaborating in research with Sanger's COSMIC team
- Specific pricing not publicly disclosed (customized per organization)

**Contact:** COSMIC commercial team via registration or QIAGEN

### Registration Process

1. **Register:** Create account at https://cancer.sanger.ac.uk/cosmic
2. **Email Verification:** Use organizational email address
3. **Re-registration:** Existing users required to re-register as of April 2nd (for current access cycle)
4. **License Determination:** Commercial users contacted by COSMIC team to complete licensing agreement
5. **Access:** Academic users gain immediate download access; commercial users after license completion

### License Checker

Interactive tool available on COSMIC licensing page to determine if your use case requires commercial licensing.

### Funding Model

COSMIC uses a dual licensing model where:
- Academic downloads are free
- Commercial subscriptions fund ongoing curation, development, and infrastructure
- Model ensures sustainability and continuous improvement

## Data Structure

### Identifiers and Relationships

**COSMIC Identifiers:**
- **Gene IDs**: COSMIC gene identifiers
- **Mutation IDs**:
  - Legacy format: COSM (coding), COSN (non-coding)
  - Current format varies by data type
- **Sample IDs**: COSMIC sample identifiers
- **Study IDs**: Links to publications

**External Cross-references:**
- Ensembl gene/transcript IDs
- HGNC gene symbols
- RefSeq accessions
- dbSNP rs IDs
- ClinVar IDs
- UniProt IDs
- PDB structure IDs
- PubMed IDs

### Entity Relationship Diagram (ERD)

COSMIC provides ERD documentation showing relationships between:
- Genes
- Mutations
- Samples
- Studies/Publications
- Tissues/Histologies
- Drugs/Therapies
- Clinical Trials

### Major Data File Types and Key Fields

#### 1. Coding Mutations (TSV/VCF)

**Key Fields:**
- `Gene name`: HGNC symbol
- `Accession Number`: Transcript accession
- `Gene CDS length`: Coding sequence length
- `HGVS genomic`: Genomic HGVS notation
- `HGVS coding`: Coding HGVS notation
- `HGVS protein`: Protein HGVS notation
- `Mutation ID`: COSMIC mutation identifier
- `Mutation CDS`: CDS change
- `Mutation AA`: Amino acid change
- `Mutation Description`: Type of mutation
- `Mutation zygosity`: Heterozygous/Homozygous/Unknown
- `GRCh`: Genome build (37 or 38)
- `Chromosome`: Chromosome location
- `Genomic position`: Position on chromosome
- `Primary site`: Tissue of origin
- `Site subtype`: Tissue subtype
- `Primary histology`: Tumor histology
- `Histology subtype`: Histology subtype
- `Sample name`: COSMIC sample ID
- `ID sample`: Internal sample ID
- `Tumour origin`: Primary/Metastatic/Recurrent
- `Age`: Patient age
- `Pubmed ID`: Associated publication
- `Somatic status`: Confirmed somatic/germline/variant of unknown origin
- `Sample Type`: Cell line/tumor/other

#### 2. Cancer Gene Census (TSV)

**Key Fields:**
- `Gene Symbol`: HGNC symbol
- `Name`: Gene full name
- `Entrez GeneId`: NCBI Gene ID
- `Genome Location`: Chromosomal location
- `Tier`: Evidence tier (1 or 2)
- `Hallmark`: Cancer hallmark categories
- `Chr Band`: Cytogenetic band
- `Somatic`: Somatic mutation indicator
- `Germline`: Germline mutation indicator
- `Tumour Types(Somatic)`: Cancer types with somatic mutations
- `Tumour Types(Germline)`: Cancer types with germline mutations
- `Cancer Syndrome`: Associated hereditary syndromes
- `Tissue Type`: Tissue specificity
- `Molecular Genetics`: Dominant/Recessive
- `Role in Cancer`: TSG/oncogene/fusion
- `Mutation Types`: Point mutation, fusion, amplification, deletion, etc.
- `Translocation Partner`: Fusion partners
- `Other Germline Mut`: Other germline alterations
- `Other Syndrome`: Additional syndromes

#### 3. Gene Fusions (TSV)

**Key Fields:**
- `Fusion ID`: COSMIC fusion identifier
- `Translocation Name`: Fusion designation (e.g., BCR-ABL1)
- `5' Gene`: 5' fusion partner
- `5' Chromosome`: 5' partner chromosome
- `5' Position`: 5' breakpoint
- `3' Gene`: 3' fusion partner
- `3' Chromosome`: 3' partner chromosome
- `3' Position`: 3' breakpoint
- `Fusion Type`: Intrachromosomal/Interchromosomal
- `Primary site`: Tissue
- `Sample name`: COSMIC sample ID
- `Pubmed ID`: Supporting publication

#### 4. Copy Number Variants (TSV)

**Key Fields:**
- `Gene name`: Gene affected
- `Sample name`: COSMIC sample ID
- `CNV Type`: Gain/Loss
- `Copy Number`: Total copy number
- `Primary site`: Tissue
- `Histology`: Tumor type
- `Pubmed ID`: Reference

#### 5. Resistance Mutations (TSV)

**Key Fields:**
- `Gene name`: Gene with resistance mutation
- `Mutation ID`: COSMIC mutation ID
- `Mutation AA`: Amino acid change
- `Drug name`: Associated drug
- `Primary site`: Tissue
- `Sample name`: Sample ID
- `Resistance status`: Confirmed/Reported

#### 6. VCF Files

**Standard VCF Columns:**
- `#CHROM`: Chromosome
- `POS`: Position
- `ID`: COSMIC mutation ID
- `REF`: Reference allele
- `ALT`: Alternate allele
- `QUAL`: Quality (typically '.')
- `FILTER`: Filter status
- `INFO`: Detailed annotations

**INFO Field Subfields:**
- `GENE`: Gene name and transcript
- `STRAND`: + or -
- `LEGACY_ID`: Legacy COSMIC ID (COSM/COSN)
- `CDS`: CDS change
- `AA`: Amino acid change (or p.? for non-coding)
- `HGVSC`: HGVS coding notation
- `HGVSG`: HGVS genomic notation
- `CNT`: Mutation count (samples with this variant)

### Genomic Builds

COSMIC provides data for:
- **GRCh37 (hg19)**: Legacy build
- **GRCh38 (hg38)**: Current standard

Separate file sets available for each build.

### Data Curation Approach

**Expert Curation:**
- Manual review by cancer genomics experts
- Literature-derived data
- Large-scale sequencing projects
- Clinical submissions
- Standardized nomenclature (HGVS)
- Quality control and validation

## Additional Resources

- **Knowledge Base**: https://www.cosmickb.org/knowledgebase/
- **Help Documentation**: Available after login
- **Tutorials**: Available on COSMIC website
- **Change Logs**: Detailed release notes for each version
- **Citation**: Tate JG, et al. COSMIC: the Catalogue Of Somatic Mutations In Cancer. Nucleic Acids Res. 2019. PMID: 30371878
- **Recent Publication**: Bamford S, et al. COSMIC: a curated database of somatic variants and clinical data for cancer. Nucleic Acids Res. 2024. PMID: 38183204
- **3D Structure Database**: COSMIC Cancer Gene Census 3D (CGC-3D)
- **GitHub Resources**: Community tools for COSMIC data processing (e.g., edawson/COSMIC2VCF)

## Summary

COSMIC is the world's most comprehensive cancer mutation resource, containing >38 million somatic mutations from >1.4 million samples, curated over 20 years by the Wellcome Sanger Institute. Data is organized into six modules: Core COSMIC, Cancer Gene Census (>750 genes), Cancer Mutation Census, Actionability (>13,000 trials), Cell Lines Project, and Resistance Mutations. Access is **free for academic/non-profit use** after registration; **commercial use requires paid license** through QIAGEN. Downloads available as VCF and TSV files for GRCh37/GRCh38 via authenticated HTTPS. Alternative access via Google BigQuery (ISB-CGC). Updated biannually (core data) with quarterly updates for actionability. Registration required; commercial users must complete licensing agreement with fees based on organization size and use case. Standard reference resource for cancer genomics research, clinical interpretation, and pharmaceutical development.
