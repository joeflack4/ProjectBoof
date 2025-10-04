# ClinVar

## Overview

ClinVar is a freely available, public archive of human genetic variants and interpretations of their relationships to diseases and other phenotypic conditions. Maintained by the National Center for Biotechnology Information (NCBI) at the National Institutes of Health (NIH), ClinVar aggregates variant submissions from clinical laboratories, researchers, and expert panels worldwide, providing a centralized resource for variant interpretation in clinical genomics.

**Website**: https://www.ncbi.nlm.nih.gov/clinvar/
**FTP Server**: ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/
**Documentation**: https://www.ncbi.nlm.nih.gov/clinvar/docs/
**Version**: Current/Latest (as of 2025)

**Database Statistics:**
- >3 million variants
- >2,800 submitting organizations worldwide
- Updated weekly (Mondays for web; first Thursday of month for comprehensive releases)

## Data Types

ClinVar contains three main types of variant classifications and associated data:

### 1. Germline Variants

**Purpose:** Variants inherited or present in reproductive cells

**Content:**
- Pathogenicity classifications (Pathogenic, Likely Pathogenic, VUS, Likely Benign, Benign)
- Associated phenotypes/diseases
- Evidence supporting classifications
- Review status and submitter information
- Mode of inheritance
- Age of onset
- Prevalence

### 2. Somatic Variants (Oncogenicity)

**Purpose:** Variants acquired in somatic cells, typically cancer-related

**Content:**
- Oncogenicity classifications (Oncogenic, Likely Oncogenic, VUS, Likely Benign, Benign)
- Associated cancer types
- Evidence for oncogenicity
- Therapeutic implications

### 3. Somatic Variants (Clinical Impact)

**Purpose:** Clinical actionability of somatic variants for treatment decisions

**Content:**
- Clinical impact classifications
- Drug response associations
- Therapeutic significance
- Treatment recommendations

### Associated Data Elements

For all variant types:
- **Variant details**: HGVS expressions, genomic coordinates, molecular consequences
- **Genes**: Associated gene symbols and identifiers
- **Conditions**: Disease names, OMIM IDs, MedGen concepts
- **Submitter information**: Organization, submission date, assertion method
- **Review status**: Stars indicating expert review level (0-4)
- **Citations**: Supporting publications (PubMed IDs)
- **Clinical significance**: Primary pathogenicity/oncogenicity assertion
- **Supporting observations**: Individual case data, functional studies, computational predictions

## Access Methods

### 1. Web Interface

**URL**: https://www.ncbi.nlm.nih.gov/clinvar/

**Features:**
- Search by gene, variant, condition, or submitter
- Filter by clinical significance, review status, variant type
- View detailed variant records with supporting evidence
- Link to related NCBI resources (dbSNP, Gene, PubMed, GTR)
- Updated weekly on Mondays

### 2. FTP Download

**FTP Site**: ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/

#### Update Schedule

**Monthly releases** (First Thursday of each month):
- Complete public dataset
- Comprehensive XML files
- VCF files
- Tab-delimited summary files
- Archived indefinitely

**Weekly releases** (Mondays):
- Temporary XML updates
- Weekly_release directory

#### File Organization (as of 2025)

Main directories:
- `/clinvar/xml/` - VCV XML files (new format, default)
- `/clinvar/xml/weekly_release/` - Weekly VCV XML updates
- `/clinvar/xml/archive/` - Previous year releases (2024 files moved here in 2025)
- `/clinvar/vcf_GRCh37/` - VCF files for GRCh37/hg19
- `/clinvar/vcf_GRCh38/` - VCF files for GRCh38/hg38
- `/clinvar/tab_delimited/` - TSV summary files

#### Available File Formats

**1. XML Files**

Two aggregation types:

**VCV (Variant-level aggregation):**
- Filename: `ClinVarVCVRelease_00-latest.xml.gz`
- All data for a variant aggregated together
- Recommended for most use cases
- New format introduced in 2024

**RCV (Variant-Condition-level aggregation):**
- Filename: `ClinVarRCVRelease_00-latest.xml.gz`
- Data organized by variant-condition pairs
- Legacy format, still supported

**2. VCF Files**

**Filenames:**
- `clinvar.vcf.gz` (GRCh37)
- `clinvar.vcf.gz` (GRCh38)

**Content:**
- Short variants (< 10 kb)
- Simple alleles with precise genomic location
- Left-shifted coordinates (VCF standard)
- Includes ClinVar Variation ID in column 3
- INFO field annotations with clinical significance, review status, conditions

**Exclusions:**
- Structural variants identified only by microarray
- Haplotypes and genotypes
- Variants with imprecise location

**3. Tab-Delimited Files (TSV)**

**variant_summary.txt:**
- Summary of all variants
- Monthly updates
- Key fields for quick filtering and analysis

**Other TSV files:**
- `var_citations.txt` - Variant-publication links
- `cross_references.txt` - Links to external databases
- `gene_condition_source_id` - Gene-condition relationships
- `submission_summary.txt` - Submitter statistics

### 3. E-utilities API (Entrez)

ClinVar is accessible through NCBI's E-utilities as part of the Entrez system.

**Supported functions:**
- **esearch**: Find variant IDs matching query
- **esummary**: Retrieve variant record summaries
- **efetch**: Fetch complete variant records
- **elink**: Link to related NCBI databases

**Base URL**: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/

**Output formats:**
- XML (default)
- JSON (for esummary)

#### Example E-utilities Queries

**ESearch - Search by gene:**
```bash
# Web URL
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BRCA1[gene]&retmode=json

# Command line (Entrez Direct)
esearch -db clinvar -query "BRCA1[gene]" | efetch -format xml
```

**ESearch - Search by chromosomal coordinates:**
```bash
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=17[chr]+AND+43000000:44000000[chrpos38]&retmode=json
```

**ESearch - Search by HGVS notation:**
```bash
esearch -db clinvar -query 'NM_000546.6:c.993+409del' | esummary | xtract -pattern DocumentSummary -element Id,accession,title
```

**ESummary - Get variant summary:**
```bash
# Get summary for specific variant IDs
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=14206,41472&retmode=json

# Command line
esearch -db clinvar -query "TP53[gene]" | esummary | xtract -pattern DocumentSummary -element Id,accession,variation_name
```

**EFetch - Retrieve VCV records (variant-level):**
```bash
# By VCV accession
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=clinvar&rettype=vcv&id=VCV000014206

# By Variation ID
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=clinvar&rettype=variation&id=14206,41472
```

**EFetch - Retrieve RCV records (variant-condition level):**
```bash
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=clinvar&rettype=clinvarset&id=RCV000000606
```

#### Python Examples using E-utilities

```python
import requests

# Search for variants in BRCA1 gene
esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
    "db": "clinvar",
    "term": "BRCA1[gene]",
    "retmode": "json",
    "retmax": 100
}
response = requests.get(esearch_url, params=params)
ids = response.json()["esearchresult"]["idlist"]

# Fetch variant details
efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
params = {
    "db": "clinvar",
    "id": ",".join(ids[:10]),
    "rettype": "vcv",
    "retmode": "xml"
}
variants = requests.get(efetch_url, params=params)
print(variants.text)
```

#### R Examples using rentrez

```r
library(rentrez)

# Search for variants in TP53
search_results <- entrez_search(db="clinvar", term="TP53[gene]", retmax=100)
variant_ids <- search_results$ids

# Get summaries
summaries <- entrez_summary(db="clinvar", id=variant_ids[1:10])

# Fetch full records
variants <- entrez_fetch(db="clinvar", id=variant_ids[1:5], rettype="vcv")
```

### 4. ClinVar Submission API (REST)

**Base URL**: https://submit.ncbi.nlm.nih.gov/api/v1/submissions/
**Test Endpoint**: https://submit.ncbi.nlm.nih.gov/apitest/v1/submissions

**Purpose:** Submit new variant interpretations or updates to ClinVar programmatically.

**Authentication:**
- Requires NCBI Submission Portal service account
- API key (64 alphanumeric characters)
- API key sent in HTTP header: `SP-API-KEY`

**Request Format:**
- HTTP POST
- Content-Type: application/json
- JSON body with submission data

**Response Codes:**
- 200 OK: Successful submission
- 201 Created: Submission processed
- 400 Bad Request: Validation error
- 401 Unauthorized: Invalid API key

**Submission Types:**
- Germline submissions
- Oncogenicity submissions
- Clinical impact submissions
- Variant deletions

**Example Submission:**
```bash
curl -X POST \
  --header "Content-type: application/json" \
  --header "SP-API-KEY: YOUR_API_KEY_HERE" \
  -d '{
    "actions": [{
      "type": "AddData",
      "targetDb": "clinvar",
      "data": {
        "content": {
          "clinvarSubmission": [{
            "clinicalSignificance": {
              "clinicalSignificanceDescription": "Pathogenic",
              "comment": "Supporting evidence description"
            },
            "variantSet": {
              "variant": [{
                "hgvs": "NM_000277.1:c.1521_1523delCTT"
              }]
            },
            "conditionSet": {
              "condition": [{
                "name": "Cystic fibrosis"
              }]
            }
          }]
        }
      }
    }]
  }' \
  "https://submit.ncbi.nlm.nih.gov/api/v1/submissions/"
```

**Check Submission Status:**
```bash
curl --header "SP-API-KEY: YOUR_API_KEY_HERE" \
  "https://submit.ncbi.nlm.nih.gov/api/v1/submissions/SUB12345678/actions/"
```

## Cost and Requirements

### Cost
**FREE** - ClinVar is completely free to use
- No subscription fees
- No registration required for data access
- No API usage limits

### License and Public Domain Status

**Public Domain (US Government Work)**
- Written by US Government employees
- Public domain in the United States
- No copyright restrictions within the US

**Important Note:**
- NCBI does not assess validity of submitter claims
- No transfer of rights from submitters to NCBI
- NCBI cannot transfer rights to third parties
- Some submitted data may have restrictions from original submitters

### Registration
- **Not required** for web browsing, FTP downloads, or E-utilities API access
- **Required** for submitting data via Submission API (need NCBI Submission Portal account and API key)

### Attribution
- **Requested** but not legally required
- Provide attribution in publications and websites
- Recommended citation: Landrum MJ, et al. ClinVar: improving access to variant interpretations and supporting evidence. Nucleic Acids Res. 2018. PMID: 29165669

### Important Usage Notes
- **Not intended for direct medical decision-making**
- Data aggregated from multiple submitters with varying review levels
- Review status (0-4 stars) indicates level of expert review
- Users should evaluate evidence supporting assertions

## Data Structure

### Variant Identifiers

**ClinVar Variation ID:**
- Represents a set of related variants (canonical variant)
- Persistent identifier
- Example: 14206

**ClinVar Allele ID:**
- Represents individual alleles within a variant set
- Multiple alleles can share one Variation ID

**Accession Numbers:**
- **VCV**: Variant-level accessions (e.g., VCV000014206)
- **RCV**: Variant-condition-level accessions (e.g., RCV000000606)
- **SCV**: Submitter-level accessions (e.g., SCV000020155)

### File Formats and Key Fields

#### 1. XML Files (VCV Format)

**Root Structure:**
```xml
<ClinVarVariationRelease>
  <VariationArchive VariationID="14206" VariationType="single nucleotide variant">
    <VariationName>NM_000277.1(PAH):c.1222C>T (p.Arg408Trp)</VariationName>
    <ClassifiedRecord>
      <Classification>
        <GermlineClassification>
          <ReviewStatus>reviewed by expert panel</ReviewStatus>
          <Description>Pathogenic</Description>
        </GermlineClassification>
      </Classification>
      <SimpleAllele AlleleID="29223">
        <GeneList>
          <Gene Symbol="PAH" GeneID="5053"/>
        </GeneList>
        <VariantType>single nucleotide variant</VariantType>
        <Location>
          <SequenceLocation Assembly="GRCh38" Chr="12" start="102851234" stop="102851234"/>
        </Location>
        <HGVSlist>
          <HGVS Type="genomic">NC_000012.12:g.102851234C>T</HGVS>
          <HGVS Type="coding">NM_000277.3:c.1222C>T</HGVS>
          <HGVS Type="protein">NP_000268.1:p.Arg408Trp</HGVS>
        </HGVSlist>
      </SimpleAllele>
      <TraitSet Type="Disease">
        <Trait Type="Disease">
          <Name>Phenylketonuria</Name>
          <XRef DB="OMIM" ID="261600"/>
        </Trait>
      </TraitSet>
    </ClassifiedRecord>
    <Classifications>
      <GermlineClassification NumberOfSubmissions="5">
        <ConditionList>
          <TraitSet>Phenylketonuria</TraitSet>
        </ConditionList>
        <Description>Pathogenic</Description>
        <ReviewStatus>reviewed by expert panel</ReviewStatus>
      </GermlineClassification>
    </Classifications>
  </VariationArchive>
</ClinVarVariationRelease>
```

**Key XML Elements:**
- `VariationArchive`: Container for variant data
- `ClassifiedRecord`: Primary variant classification
- `SimpleAllele`, `Haplotype`, `Genotype`: Variant types
- `GeneList`: Associated genes
- `Location/SequenceLocation`: Genomic coordinates
- `HGVSlist`: HGVS expressions
- `Classification`: Clinical significance
- `ReviewStatus`: Expert review level
- `TraitSet`: Associated conditions
- `ClinicalAssertionList`: Individual submissions (SCVs)
- `FunctionalConsequence`: Molecular consequence
- `Citations`: Supporting publications

#### 2. VCF Files

**Key INFO Fields:**
- `CLNDN`: Condition name(s)
- `CLNVC`: Variant type
- `CLNSIG`: Clinical significance
- `CLNREVSTAT`: Review status
- `CLNHGVS`: HGVS expression
- `CLNVI`: Variant identifiers in other databases
- `GENEINFO`: Gene symbol and ID
- `MC`: Molecular consequence
- `AF_EXAC`: ExAC allele frequency
- `AF_ESP`: ESP allele frequency
- `AF_TGP`: 1000 Genomes allele frequency

**Example VCF Record:**
```
#CHROM  POS         ID      REF  ALT  QUAL  FILTER  INFO
12      102851234   14206   C    T    .     .       CLNDN=Phenylketonuria;CLNSIG=Pathogenic;CLNREVSTAT=reviewed_by_expert_panel;CLNHGVS=NC_000012.12:g.102851234C>T;GENEINFO=PAH:5053;MC=SO:0001583|missense_variant
```

#### 3. Tab-Delimited Files (variant_summary.txt)

**Key Fields (30 columns):**
- `AlleleID`: ClinVar Allele ID
- `Type`: Variant type (single nucleotide variant, deletion, etc.)
- `Name`: HGVS or descriptive name
- `GeneID`: NCBI Gene ID
- `GeneSymbol`: Gene symbol
- `ClinicalSignificance`: Primary classification
- `ReviewStatus`: Review level
- `NumberSubmitters`: Count of submitters
- `Assembly`: Reference genome build
- `Chromosome`: Chromosome
- `Start`: Start position
- `Stop`: End position
- `ReferenceAllele`: Reference allele
- `AlternateAllele`: Alternate allele
- `PhenotypeIDS`: OMIM, MedGen IDs
- `PhenotypeList`: Condition names
- `OriginSimple`: germline, somatic, etc.
- `VariationID`: ClinVar Variation ID
- `PositionVCF`: VCF-format position
- `ReferenceAlleleVCF`: VCF reference
- `AlternateAlleleVCF`: VCF alternate

### Genomic Coordinate Conventions

**XML and TSV files:**
- Right-shifted (HGVS convention)
- 1-based offset

**VCF files:**
- Left-shifted (VCF standard)
- 0-based offset for start position

**Genome Assemblies:**
- GRCh37 (hg19)
- GRCh38 (hg38)

### Review Status Levels (Star Ratings)

- **4 stars**: Practice guideline
- **3 stars**: Reviewed by expert panel
- **2 stars**: Criteria provided, multiple submitters, no conflicts
- **1 star**: Criteria provided, single submitter
- **0 stars**: No assertion criteria provided

## Additional Resources

- **Help Documentation**: https://www.ncbi.nlm.nih.gov/clinvar/docs/help/
- **FAQ**: https://www.ncbi.nlm.nih.gov/clinvar/docs/faq/
- **Variation Viewer**: https://www.ncbi.nlm.nih.gov/variation/view/
- **GTR (Genetic Testing Registry)**: https://www.ncbi.nlm.nih.gov/gtr/
- **GitHub Tools**: https://github.com/clingen-data-model/clinvar-api
- **API Demo**: https://github.com/clinvar/apidemo
- **Community Tools**: https://github.com/macarthur-lab/clinvar (TSV conversion)
- **Simple ClinVar**: https://simple-clinvar.broadinstitute.org/ (user-friendly interface)

## Summary

ClinVar is a free, public database containing >3 million human genetic variants with clinical interpretations from >2,800 organizations worldwide. It provides germline, somatic oncogenicity, and clinical impact classifications. Data is accessible via web interface, FTP downloads (XML, VCF, TSV formats), E-utilities API (esearch, esummary, efetch), and Submission API. Updated weekly on web and monthly for comprehensive releases. All data is in the public domain (US Government work) with attribution requested but not required. ClinVar uses variant-level (VCV) and variant-condition-level (RCV) aggregations with review status indicators (0-4 stars) showing expert curation level. Essential resource for clinical variant interpretation, though not intended for direct medical decision-making without professional evaluation.
