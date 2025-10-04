# OncoKB (Precision Oncology Knowledge Base)

## Overview

OncoKB™ is a precision oncology knowledge base developed by Memorial Sloan Kettering Cancer Center (MSK) that annotates the biological consequences and clinical implications of genetic variants in cancer. OncoKB provides expert-curated, evidence-based information about the oncogenic effects, prognostic significance, and therapeutic implications of somatic molecular alterations, with partial FDA recognition as a genetic variant database. The knowledge base is guided by the MSK Clinical Genomics Annotation Committee and incorporates information from FDA labeling, NCCN guidelines, expert panels, and medical literature.

**Website**: https://www.oncokb.org
**API Documentation**: https://api.oncokb.org
**GitHub**: https://github.com/oncokb
**Contact**: contact@oncokb.org
**Version**: Current/Latest (continuously updated)

**Database Statistics:**
- >800 genes annotated
- >7,800 genomic alterations
- >3,000 unique mutations, fusions, and copy number alterations in 418 cancer-associated genes (as of publication)

## Data Types

OncoKB focuses on somatic variants in cancer, with plans to expand to germline variants.

### 1. Gene-Level Information

**Content:**
- Oncogene and tumor suppressor gene designations
- Background information on gene function
- Gene summary and clinical relevance
- Links to external databases

### 2. Alteration-Level Annotations

OncoKB annotates several types of genomic alterations:

#### Mutation Types

**Point Mutations and Small Variants:**
- Missense mutations
- Nonsense mutations
- Frameshift mutations
- Splice site mutations
- In-frame insertions/deletions
- Nonstop mutations

**Supported Formats:**
- HGVSp (protein change)
- HGVSp_Short (short protein notation)
- HGVSg (genomic change)
- Genomic Change format

#### Structural Variants

**Gene Fusions:**
- Fusion genes (e.g., BCR-ABL1, EML4-ALK)
- Intragenic deletions
- Fusion partner information
- Breakpoint details

**Other Structural Variant Types:**
- DELETION
- TRANSLOCATION
- DUPLICATION
- INSERTION
- INVERSION
- FUSION
- UNKNOWN

#### Copy Number Alterations

**Amplifications:**
- Gene-level amplifications
- Oncogene amplifications

**Deletions:**
- Homozygous deletions
- Tumor suppressor deletions

### 3. Variant-Level Annotations

For each alteration, OncoKB provides:

**Biological Annotations:**
- **Mutation Effect**: Impact on protein function (e.g., Gain-of-function, Loss-of-function, Switch-of-function, Likely Gain-of-function, Unknown)
- **Oncogenic Effect**: Oncogenic, Likely Oncogenic, Likely Neutral, Inconclusive, Unknown
- **Hotspot**: Whether variant occurs at known mutational hotspot
- **VUS Status**: Variant of Unknown Significance designation

**Clinical Annotations:**
- Tumor type-specific therapeutic implications
- Prognostic implications
- Diagnostic implications
- FDA-approved therapies
- Standard of care treatments
- Clinical trial eligibility
- Off-label uses

### 4. Therapeutic Implications (Levels of Evidence)

OncoKB uses a tiered system to classify the strength of evidence for therapeutic actionability:

#### Standard Care (FDA-Approved)

**Level 1:**
- FDA-recognized biomarkers predictive of response to FDA-approved drugs in specific indications
- Strongest evidence level

**Level 2:**
- Standard care biomarker recommended by NCCN or other expert panels
- Predictive of response to FDA-approved drug in the indication

#### Investigational

**Level 3A:**
- FDA- or non-FDA-recognized biomarkers
- Predictive of response to novel targeted agents
- Promising results in clinical trials

**Level 3B:**
- Standard care or investigational biomarker
- Predictive of response to FDA-approved or investigational drug in another indication (off-label use)

**Level 4:**
- Non-FDA-recognized biomarkers
- Predictive of response to novel targeted agents
- Based on compelling biological data

#### Resistance

**Level R1:**
- Standard care biomarker predictive of resistance to FDA-approved drug in a specific indication

**Level R2:**
- Non-FDA-recognized biomarker predictive of resistance to FDA-approved or investigational drug

### 5. Prognostic Implications

**Levels:**
- Prognostic Level 1: FDA-recognized or well-validated prognostic biomarker
- Prognostic Level 2: Emerging prognostic biomarkers

### 6. Diagnostic Implications

Information about the diagnostic utility of alterations for specific cancer types

## Access Methods

### 1. Web Interface

**URL**: https://www.oncokb.org

**Features:**
- Search by gene, alteration, or tumor type
- Browse cancer genes and actionable genes
- View detailed variant annotations
- Access therapeutic level of evidence information
- Links to clinical trials
- Integration with cBioPortal

**Registration:**
- Not required for browsing public content
- Required for API access

### 2. API Access

**API Base URL**: https://www.oncokb.org/api/v1/
**API Documentation**: https://api.oncokb.org (Swagger/OpenAPI interface)

#### Authentication

**Token Required:**
- All API access requires authentication token
- Obtain token by registering account on OncoKB website
- Token included in request headers

#### Key API Endpoints

**Mutation Annotation:**
```
GET /api/v1/annotate/mutations/byProteinChange
GET /api/v1/annotate/mutations/byGenomicChange
GET /api/v1/annotate/mutations/byHGVSg
POST /api/v1/annotate/mutations
```

**Copy Number Alteration Annotation:**
```
GET /api/v1/annotate/copyNumberAlterations
POST /api/v1/annotate/copyNumberAlterations
```

**Structural Variant Annotation:**
```
GET /api/v1/annotate/structuralVariants
POST /api/v1/annotate/structuralVariants
```

**Gene Information:**
```
GET /api/v1/genes
GET /api/v1/genes/{entrezGeneId}
```

**Tumor Type Information:**
```
GET /api/v1/tumorTypes
```

#### Example API Usage

**Python Example:**
```python
import requests

# Set up authentication
headers = {
    'Authorization': 'Bearer YOUR_ONCOKB_TOKEN'
}

# Annotate a mutation
url = 'https://www.oncokb.org/api/v1/annotate/mutations/byProteinChange'
params = {
    'hugoSymbol': 'BRAF',
    'alteration': 'V600E',
    'tumorType': 'Melanoma'
}

response = requests.get(url, headers=headers, params=params)
annotation = response.json()

print(f"Mutation Effect: {annotation['mutationEffect']['knownEffect']}")
print(f"Oncogenic: {annotation['oncogenic']}")
print(f"Highest Level: {annotation['highestSensitiveLevel']}")
```

**cURL Example:**
```bash
curl -X GET "https://www.oncokb.org/api/v1/annotate/mutations/byProteinChange?hugoSymbol=EGFR&alteration=L858R&tumorType=Lung%20Adenocarcinoma" \
  -H "Authorization: Bearer YOUR_ONCOKB_TOKEN"
```

### 3. OncoKB Annotator (GitHub Tools)

**Repository**: https://github.com/oncokb/oncokb-annotator

OncoKB provides command-line annotation tools for batch processing:

#### Available Annotators

**MafAnnotator.py:**
- Annotates variants in MAF (Mutation Annotation Format) files
- Adds OncoKB oncogenicity and therapeutic annotations

**FusionAnnotator.py:**
- Annotates gene fusions
- Requires fusion partner information

**CnaAnnotator.py:**
- Annotates copy number alterations
- Handles amplifications and deletions

**ClinicalDataAnnotator.py:**
- Combines all annotations at sample/patient level
- Generates comprehensive clinical reports

#### Example Usage

**MAF Annotation:**
```bash
# Install oncokb-annotator
pip install oncokb-annotator

# Annotate MAF file
python MafAnnotator.py \
  -i input.maf \
  -o output.maf \
  -b YOUR_ONCOKB_TOKEN \
  -q HGVSp_Short
```

**Fusion Annotation:**
```bash
python FusionAnnotator.py \
  -i fusions.txt \
  -o fusions_annotated.txt \
  -b YOUR_ONCOKB_TOKEN
```

**CNA Annotation:**
```bash
python CnaAnnotator.py \
  -i cna_data.txt \
  -o cna_annotated.txt \
  -b YOUR_ONCOKB_TOKEN
```

### 4. cBioPortal Integration

**Integration:** OncoKB annotations are incorporated into cBioPortal for Cancer Genomics

**Access:** When viewing patient genomic data in cBioPortal, OncoKB annotations appear automatically

**Benefits:** Seamless integration for clinical interpretation

### 5. Data Dump Access

**Availability:** Complete data dump available upon request

**Process:**
- Contact OncoKB team at contact@oncokb.org
- Requires license agreement
- Typically used for local database implementation
- Additional fees may apply

## Cost and Requirements

### Cost Structure

#### Academic/Research Use (NO FEE)

**Qualifications:**
- Research in academic/non-profit setting
- Educational institutions
- Government research facilities

**Access:**
- Free website browsing
- Free API access with institutional email registration
- No license agreement required for academic research

#### Commercial Use (FEE REQUIRED)

**Use Cases Requiring License:**
- Research and development in commercial settings
- Creating commercial products or services
- Patient services or clinical reporting (healthcare settings)
- Annotation of clinical sequencing reports
- Integration into commercial software/platforms

**Pricing:**
- **Research in commercial setting**: Based on company size and intended data use
- **Clinical sequencing reports**: Based on anticipated annual report volume
- **Local database copies**: Rare; requires additional fees
- Specific pricing not publicly disclosed (customized per organization)

**Contact:** licensing@oncokb.org

### License Types

1. **Academic Research License**: Free, requires institutional email
2. **Commercial Research License**: Annual fee based on company size
3. **Clinical Use License**: Annual fee based on report volume
4. **Enterprise License**: Custom terms for large organizations

### Registration Process

**Academic Users:**
1. Register at oncokb.org
2. Use institutional/university email address
3. Agree to academic use license terms
4. Receive API token

**Commercial Users:**
1. Register on API/License Page
2. OncoKB team will contact to discuss use case
3. Negotiate license terms and fees
4. Sign license agreement
5. Pay annual license fee
6. Receive API token

### Important Restrictions

**AI/ML Training:**
- **NOT ALLOWED**: Cannot use OncoKB data to train AI/ML models
- Explicitly prohibited in license terms

**Attribution:**
- **REQUIRED**: Must cite OncoKB in publications and products
- Recommended citations:
  - Chakravarty D, et al. OncoKB: A Precision Oncology Knowledge Base. JCO Precision Oncology. 2017. PMID: 28890946
  - Suehnholz SP, et al. Quantifying the Expanding Landscape of Clinical Actionability for Patients with Cancer. Cancer Discovery. 2023.

**Disclaimer:**
- OncoKB is NOT a medical product
- NOT a substitute for professional medical advice
- Not intended for direct diagnostic use without professional review

### FDA Recognition

- Partial FDA recognition as a genetic variant database (not full medical device approval)
- FDA Decision Summary available at: https://www.fda.gov/media/152847/download

## Data Structure

### Hierarchical Organization

OncoKB information is hierarchically organized by:
1. **Gene**
2. **Alteration** (mutation, fusion, CNA)
3. **Tumor Type**
4. **Clinical Implication** (therapeutic, prognostic, diagnostic)

### Database Backend

**Storage:** MySQL database

**Access Interfaces:**
- Web interface
- REST API
- cBioPortal integration
- Annotator tools

### Annotation Fields

#### Gene-Level Fields
- `entrezGeneId`: NCBI Entrez Gene ID
- `hugoSymbol`: HGNC gene symbol
- `oncogene`: Boolean (oncogene designation)
- `tsg`: Boolean (tumor suppressor gene designation)
- `geneAliases`: Alternative gene names
- `grch37Isoform`: GRCh37 reference transcript
- `grch38Isoform`: GRCh38 reference transcript

#### Alteration-Level Fields
- `alteration`: Variant description
- `alterationType`: Mutation, Fusion, Copy Number Alteration
- `mutationEffect`: Functional effect
- `mutationEffectDescription`: Detailed explanation
- `mutationEffectPmids`: Supporting publications
- `mutationEffectAbstracts`: Abstract summaries

#### Oncogenicity Fields
- `oncogenic`: Oncogenic classification
- `oncogenicPmids`: Supporting publications

#### Therapeutic Fields
- `treatments`: List of associated therapies
- `drugs`: Specific drug names
- `level`: Level of evidence (1, 2, 3A, 3B, 4, R1, R2)
- `fdaLevel`: FDA approval status
- `tumorType`: Specific cancer type
- `indication`: Clinical indication
- `pmids`: Supporting publications

#### Diagnostic/Prognostic Fields
- `diagnosticImplications`: Diagnostic utility
- `prognosticImplications`: Prognostic significance
- `prognosticLevel`: Strength of prognostic evidence

### MAF Output Fields (from Annotator)

When using oncokb-annotator, additional columns added to MAF:

- `GENE_IN_ONCOKB`: Gene is in OncoKB (Yes/No)
- `VARIANT_IN_ONCOKB`: Variant is in OncoKB (Yes/No)
- `MUTATION_EFFECT`: Functional effect
- `MUTATION_EFFECT_CITATIONS`: PMIDs
- `ONCOGENIC`: Oncogenicity classification
- `ONCOGENIC_CITATIONS`: Supporting PMIDs
- `HIGHEST_LEVEL`: Highest therapeutic level
- `HIGHEST_SENSITIVE_LEVEL`: Highest sensitivity level
- `HIGHEST_RESISTANCE_LEVEL`: Highest resistance level
- `TREATMENTS`: Pipe-separated list of treatments
- `TUMOR_TYPE_SPECIFIC_THERAPEUTIC_IMPLICATIONS`: Detailed therapeutic info

### External Cross-References

OncoKB integrates data from:
- **FDA** (drug approvals, labels)
- **NCCN Guidelines** (standard of care)
- **PubMed** (literature evidence)
- **ClinicalTrials.gov** (clinical trials)
- **cBioPortal** (patient genomic data)
- **HGNC** (gene nomenclature)
- **RefSeq/Ensembl** (transcript information)

## Additional Resources

- **FAQ**: https://faq.oncokb.org
- **Technical Documentation**: https://faq.oncokb.org/technical
- **Data Curation**: https://faq.oncokb.org/data-curation
- **Licensing**: https://faq.oncokb.org/licensing
- **GitHub Organization**: https://github.com/oncokb
- **Therapeutic Levels**: https://www.oncokb.org/therapeutic-levels
- **Cancer Genes**: https://www.oncokb.org/cancer-genes
- **Actionable Genes**: https://www.oncokb.org/actionable-genes
- **FDA Decision Summary**: https://www.fda.gov/media/152847/download

## Summary

OncoKB is MSK's precision oncology knowledge base containing expert-curated annotations for >800 genes and >7,800 genomic alterations, including mutations, fusions, and copy number alterations. Provides biological (mutation effect, oncogenicity) and clinical (therapeutic, prognostic, diagnostic) implications using evidence-based levels (1, 2, 3A, 3B, 4, R1, R2). **Free for academic research** with institutional email registration; **commercial use requires paid license** with fees based on organization size and use case. Access via web interface, REST API (requires token), and GitHub annotator tools (MafAnnotator, FusionAnnotator, CnaAnnotator). Integrated into cBioPortal. Partial FDA recognition. **Cannot be used for AI/ML training**. Currently focuses on somatic variants; germline support planned. Data dump available upon request. Essential resource for clinical oncology variant interpretation, precision medicine, and therapeutic decision-making, though not a substitute for professional medical advice.
