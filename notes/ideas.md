# HarmonaQuery: Ideas & Future Directions

## Overview
This document catalogs potential tasks, analyses, features, and research questions we can pursue with the harmonized genomic/clinical data from GenCC, ClinGen, ClinVar, cBioPortal, TCGA, COSMIC, and OncoKB.

## Contents
Document Contents

**12 Major Sections with actionable tasks:

1. Data Analysis & Exploration (30+ tasks): Profiling, cross-source reconciliation,
cancer genomics, clinical relevance
2. Research Questions (30 questions): Gene-disease relationships, variant
interpretation, therapeutic actionability, cancer biology
3. CLI Features: Query, ETL/import, export commands with examples
4. Web Frontend: Search/browse, visualizations, interactive tools, data explorer
5. API Features: RESTful endpoints, GraphQL schema
6. Data Science & ML: Predictive models, clustering, network analysis, Jupyter
notebooks
7. Integration: External data sources, standards compliance, export formats
8. Quality Assurance: Data validation, automated testing, documentation
9. Deployment: Docker, database management, CI/CD
10. Advanced Features: Ontology integration, batch processing, privacy/security
11. Immediate Next Steps: 5 high-priority tasks you can assign tonight + 4
medium-priority for this week
12. Success Metrics: Measurable goals for quality, performance, usability

Highlighted: Tasks for Tonight

The "Immediate Next Steps" section includes 5 tasks perfect for now:

1. Data profiling scripts - Count records, identify missing values
2. Basic exploration queries - Top mutated genes, gene-disease overlaps
3. Identifier mapping research - Test APIs for HGNC/variant normalization
4. ETL prototype - Parse GenCC, create sample schema
5. CLI skeleton - Set up framework with basic stats commands

---

## 1. Data Analysis & Exploration Tasks

### 1.1 Data Profiling & Quality Assessment
- [ ] **Source coverage analysis**: Compare gene-disease associations across ClinGen vs GenCC - overlap, conflicts, unique entries
- [ ] **Variant annotation completeness**: Count variants with HGVS notation (genomic/coding/protein) across sources
- [ ] **Missing data analysis**: Identify fields with high missingness (age, race, treatment data in TCGA)
- [ ] **Identifier mapping coverage**: Measure success rate of HGNC/MONDO/dbSNP mappings
- [ ] **Temporal analysis**: Track assertion dates across sources - identify stale vs recent curations
- [ ] **Submitter diversity**: Analyze how many different organizations contribute to each source
- [ ] **Evidence strength distribution**: Count assertions by classification (Definitive, Strong, Moderate, etc.)

### 1.2 Cross-Source Reconciliation
- [ ] **Conflict detection**: Find gene-disease pairs with conflicting validity classifications across sources
- [ ] **Variant pathogenicity disagreement**: Identify variants classified differently by ClinVar submitters
- [ ] **Dosage sensitivity validation**: Compare ClinGen dosage scores with cancer gene amplification/deletion patterns in TCGA
- [ ] **Gene-disease network comparison**: Build bipartite graphs from ClinGen and GenCC, measure structural differences
- [ ] **Therapeutic actionability overlap**: Compare OncoKB vs COSMIC actionability annotations for same variants

### 1.3 Cancer Genomics Analyses (TCGA + cBioPortal)
- [ ] **Mutation landscape**: Most frequently mutated genes in BRCA vs LUAD
- [ ] **Mutational signatures**: Identify signature patterns (e.g., APOBEC, smoking-related)
- [ ] **Co-occurrence analysis**: Which gene mutations co-occur more/less than expected (e.g., TP53 + PIK3CA)
- [ ] **Mutual exclusivity**: Identify mutually exclusive mutation pairs (synthetic lethality candidates)
- [ ] **Copy number burden**: Correlate total CNA load with clinical outcomes
- [ ] **Tumor mutational burden (TMB)**: Calculate TMB per sample, correlate with survival
- [ ] **Driver vs passenger mutations**: Classify mutations using OncoKB/COSMIC annotations
- [ ] **Subtype-specific mutations**: Identify mutations enriched in ER+, HER2+, triple-negative breast cancer
- [ ] **Prognostic markers**: Correlate specific mutations/CNAs with survival outcomes
- [ ] **Age-related patterns**: Mutation spectrum differences by age at diagnosis

### 1.4 Clinical Relevance & Actionability
- [ ] **Actionable variant frequency**: How many TCGA samples have OncoKB Level 1-4 actionable mutations?
- [ ] **FDA-approved therapies**: Count samples with mutations matching FDA-approved drug indications
- [ ] **Clinical trial matching**: Identify patients eligible for trials based on OncoKB Level 3-4 evidence
- [ ] **Germline-somatic concordance**: Compare ClinVar germline pathogenic variants with TCGA somatic mutations
- [ ] **Therapeutic resistance**: Analyze COSMIC resistance mutations in TCGA cohorts
- [ ] **Druggable genome coverage**: Percentage of cancer genes with known therapeutic interventions

### 1.5 Population & Epidemiology
- [ ] **Demographic stratification**: Mutation patterns by race/ethnicity in TCGA
- [ ] **Age distribution analysis**: Age at diagnosis by mutation status
- [ ] **Sex-specific patterns**: X-linked genes, sex-specific penetrance
- [ ] **Geographic variation**: If data available, compare mutation frequencies by collection site

---

## 2. Research Questions to Answer

### 2.1 Gene-Disease Relationships
1. **Which genes have the strongest evidence for causing breast cancer across all sources?**
2. **How many gene-disease associations are supported by only one source vs multiple?**
3. **What percentage of cancer genes in COSMIC have Mendelian disease associations in ClinGen/GenCC?**
4. **Which genes are haploinsufficient (ClinGen) but also show recurrent amplifications in cancer (TCGA)?**
5. **How many genes associated with autosomal recessive diseases also harbor somatic driver mutations?**

### 2.2 Variant Interpretation
6. **What percentage of TCGA somatic mutations have ClinVar germline annotations?**
7. **How many variants are classified as pathogenic in ClinVar but also occur as somatic mutations in TCGA?**
8. **Which variants have conflicting classifications between ClinVar submitters?**
9. **What is the overlap between ClinVar pathogenic variants and COSMIC oncogenic variants?**
10. **How many TCGA mutations lack any annotation in ClinVar, COSMIC, or OncoKB?**

### 2.3 Therapeutic Actionability
11. **What percentage of breast cancer patients have at least one OncoKB Level 1-2 actionable mutation?**
12. **Which genes have the most FDA-approved targeted therapies (OncoKB Level 1)?**
13. **How many TCGA patients would be eligible for investigational therapies (OncoKB Level 3-4)?**
14. **What is the distribution of therapeutic levels of evidence across cancer types?**
15. **Which mutations predict resistance to standard-of-care therapies?**

### 2.4 Cancer Biology
16. **What are the top 20 most frequently mutated genes in breast cancer vs lung adenocarcinoma?**
17. **Which gene pairs show significant co-occurrence or mutual exclusivity?**
18. **How does tumor mutational burden correlate with survival in BRCA vs LUAD?**
19. **Which copy number alterations are most associated with poor prognosis?**
20. **What percentage of tumors have actionable alterations in DNA damage repair pathways?**

### 2.5 Data Quality & Completeness
21. **Which data sources have the most comprehensive variant-level annotations?**
22. **How often do HGNC gene symbols change, and how many variants are affected?**
23. **What percentage of TCGA clinical data is complete for key fields (age, stage, grade, outcomes)?**
24. **How many TCGA samples have multi-omic data (mutations + CNA + expression)?**
25. **Which genome build (GRCh37 vs GRCh38) is most consistently used across sources?**

### 2.6 Precision Medicine
26. **Can we build a classifier to predict OncoKB therapeutic level based on mutation features?**
27. **Which biomarker combinations best predict response to immunotherapy?**
28. **How many patients have multiple actionable alterations in different genes?**
29. **What is the concordance between OncoKB and COSMIC actionability annotations?**
30. **Which rare mutations occur in >1 patient and might represent recurrent driver events?**

---

## 3. Command-Line Interface (CLI) Features

### 3.1 Query CLI
```bash
# Gene-disease associations
harmonaquery gene BRCA1 --diseases --sources all
harmonaquery gene-disease-validity --gene BRCA1 --disease "breast cancer" --min-classification Strong

# Variant lookup
harmonaquery variant "NM_007294.3:c.5266dupC" --pathogenicity --actionability --sources all
harmonaquery variant-patients --hgvs "p.Arg248Gln" --cancer-type "Breast"

# Sample/patient queries
harmonaquery patients --mutations TP53 --cancer-type BRCA --age-min 40 --age-max 60
harmonaquery sample TCGA-A2-A0T4 --mutations --cna --expression --clinical

# Therapeutic actionability
harmonaquery actionable-variants --oncokb-level 1 --cancer-type "Breast Cancer"
harmonaquery drug-matches --variant "PIK3CA p.His1047Arg" --fda-approved

# Cohort building
harmonaquery build-cohort --mutations TP53,PIK3CA --cancer-type BRCA --stage "Stage II" --output cohort.json
harmonaquery cohort-stats cohort.json --mutations --survival --demographics

# Data statistics
harmonaquery stats genes --source ClinGen
harmonaquery stats variants --pathogenic --source ClinVar
harmonaquery stats samples --cancer-type all --by-source
```

### 3.2 ETL/Import CLI
```bash
# Import data
harmonaquery import gencc --file data/sources/gencc/gencc-submissions.tsv
harmonaquery import clingen --type gene-validity --file data/sources/clingen/gene-validity.csv
harmonaquery import clinvar --vcf data/sources/clinvar/clinvar_grch38.vcf.gz
harmonaquery import tcga --project TCGA-BRCA --data-types clinical,mutations

# Identifier mapping
harmonaquery map-identifiers --source genes --from symbol --to hgnc_id --input genes.txt
harmonaquery normalize-variants --input variants.txt --output variants_normalized.json

# Data validation
harmonaquery validate --source gencc --schema
harmonaquery check-integrity --tables all --report integrity_report.txt
```

### 3.3 Export CLI
```bash
# Export to various formats
harmonaquery export gene-disease --format csv --output gene_disease.csv
harmonaquery export actionable-variants --cancer-type BRCA --format json
harmonaquery export vcf --samples cohort.json --output cohort_variants.vcf

# Generate reports
harmonaquery report summary --output summary.html
harmonaquery report cancer-genomics --project TCGA-BRCA --output brca_report.pdf
```

---

## 4. Web Frontend Features

### 4.1 Search & Browse Interface
- **Gene search**: Autocomplete gene symbols, display associations, pathways, variants
- **Variant search**: HGVS/rsID lookup, show pathogenicity, frequency, samples
- **Disease search**: Browse MONDO hierarchy, associated genes, clinical actionability
- **Sample browser**: Filter TCGA samples by mutations, demographics, outcomes
- **Cohort builder**: Interactive filters (age, sex, cancer type, mutations) → download patient list

### 4.2 Visualization Dashboards
- **Gene-disease network**: Interactive graph (D3.js/Cytoscape) showing relationships
- **Mutation lollipop plots**: Protein domains with mutation hotspots
- **Copy number heatmaps**: Samples × genes showing amplifications/deletions
- **Oncoprint**: cBioPortal-style visualization of mutations, CNAs, expression across cohort
- **Survival curves**: Kaplan-Meier plots stratified by mutation status
- **Waterfall plots**: Top mutated genes with sample annotations

### 4.3 Analysis Tools (Interactive)
- **Virtual cohort creator**: Select criteria → see matching patient count → download
- **Drug matching tool**: Enter mutation → get FDA-approved/investigational therapies
- **Variant interpreter**: Enter HGVS → aggregated pathogenicity from all sources
- **Co-occurrence matrix**: Interactive heatmap of gene pair co-occurrence
- **Mutational signature analyzer**: Upload MAF → identify COSMIC signatures

### 4.4 Data Explorer
- **Table browser**: Sortable, filterable tables for genes, variants, samples
- **SQL query interface**: Advanced users can write custom SQL queries
- **GraphQL playground**: Interactive GraphQL query builder
- **API documentation**: Interactive Swagger/OpenAPI docs

### 4.5 User Features
- **Save queries/cohorts**: User accounts to save and share cohorts
- **Export functionality**: CSV, JSON, VCF, Excel downloads
- **Bookmarking**: Save interesting genes/variants for later
- **Annotation**: Users can add notes to cohorts/variants

---

## 5. API Features

### 5.1 RESTful API Endpoints
```
# Genes
GET    /api/genes
GET    /api/genes/{hgnc_id}
GET    /api/genes/{hgnc_id}/diseases
GET    /api/genes/{hgnc_id}/variants
GET    /api/genes/{hgnc_id}/expression/{sample_id}

# Diseases
GET    /api/diseases
GET    /api/diseases/{mondo_id}
GET    /api/diseases/{mondo_id}/genes
GET    /api/diseases/{mondo_id}/variants

# Variants
GET    /api/variants
POST   /api/variants/lookup        # Body: {hgvs: "..."}
GET    /api/variants/{allele_id}
GET    /api/variants/{allele_id}/pathogenicity
GET    /api/variants/{allele_id}/actionability
GET    /api/variants/{allele_id}/samples

# Samples/Patients
GET    /api/samples
GET    /api/samples/{sample_id}
GET    /api/samples/{sample_id}/mutations
GET    /api/samples/{sample_id}/cna
GET    /api/samples/{sample_id}/expression
POST   /api/samples/search         # Body: filters

# Cohorts
POST   /api/cohorts                # Create virtual cohort
GET    /api/cohorts/{cohort_id}
GET    /api/cohorts/{cohort_id}/samples
GET    /api/cohorts/{cohort_id}/stats

# Therapeutic
GET    /api/actionable-variants
GET    /api/drugs/{drug_name}/variants
GET    /api/therapies/fda-approved
```

### 5.2 GraphQL Schema
```graphql
type Query {
  gene(hgncId: String!): Gene
  genes(symbols: [String!], limit: Int): [Gene!]!
  variant(alleId: String!): Variant
  variantByHgvs(hgvs: String!): Variant
  disease(mondoId: String!): Disease
  samples(filters: SampleFilters): [Sample!]!
  cohort(mutations: [String!], cancerType: String): Cohort!
}

type Gene {
  hgncId: String!
  symbol: String!
  diseases: [GeneDiseaseAssociation!]!
  variants: [Variant!]!
  dosageSensitivity: DosageSensitivity
}

type Variant {
  clingen AlleId: String!
  hgvs: HgvsNotation!
  pathogenicity: [PathogenicityAssertion!]!
  actionability: [ActionabilityAssertion!]!
  samples: [SampleVariant!]!
}

type Sample {
  sampleId: String!
  patient: Patient!
  mutations: [SomaticMutation!]!
  cna: [CopyNumberAlteration!]!
  expression: [GeneExpression!]!
}
```

---

## 6. Data Science & ML Features

### 6.1 Predictive Models
- [ ] **Pathogenicity predictor**: Train classifier on ClinVar data to predict variant pathogenicity
- [ ] **Survival prediction**: Cox regression / random forest for survival based on mutations + demographics
- [ ] **Therapeutic response**: Predict drug response based on mutation profile
- [ ] **Cancer subtype classifier**: Predict molecular subtype from mutation + CNA + expression
- [ ] **TMB predictor**: Estimate tumor mutational burden from limited gene panels

### 6.2 Clustering & Unsupervised Learning
- [ ] **Patient stratification**: K-means / hierarchical clustering on mutation profiles
- [ ] **Gene module discovery**: Identify co-regulated gene sets from expression data
- [ ] **Mutational signature extraction**: NMF on mutation context to discover signatures
- [ ] **Pathway enrichment**: Over-representation analysis for mutated gene sets

### 6.3 Network Analysis
- [ ] **Gene-gene interaction networks**: Build networks from co-occurrence, protein-protein interactions
- [ ] **Community detection**: Identify gene communities (e.g., DNA repair, cell cycle)
- [ ] **Centrality analysis**: Identify hub genes in disease networks
- [ ] **Shortest path analysis**: Find connections between genes and diseases

### 6.4 Jupyter Notebooks / R Markdown
- [ ] **Data exploration templates**: Pre-built notebooks for common analyses
- [ ] **Visualization gallery**: Examples of plots and charts
- [ ] **Tutorial notebooks**: Step-by-step guides for common questions
- [ ] **Reproducible research**: Parameterized notebooks for cohort analyses

---

## 7. Integration & Interoperability

### 7.1 External Data Sources
- [ ] **gnomAD**: Integrate population allele frequencies for variant filtering
- [ ] **CIViC**: Clinical Interpretations of Variants in Cancer
- [ ] **PharmGKB**: Pharmacogenomics knowledge
- [ ] **STRING**: Protein-protein interaction networks
- [ ] **Reactome**: Pathway annotations
- [ ] **GTEx**: Normal tissue expression for comparison

### 7.2 Standards Compliance
- [ ] **GA4GH**: Implement Variant Representation Specification (VRS)
- [ ] **FHIR**: Genomics reporting via HL7 FHIR
- [ ] **Beacon**: Implement Beacon v2 protocol for variant queries
- [ ] **Phenopackets**: Export patient/sample data as Phenopackets

### 7.3 Export Formats
- [ ] **VCF**: Export variant calls with annotations
- [ ] **MAF**: Export mutation annotation format
- [ ] **GFF/GTF**: Gene/transcript annotations
- [ ] **BED**: Genomic regions (CNAs, dosage sensitive regions)
- [ ] **RDF/TTL**: Semantic web export for ontology integration

---

## 8. Quality Assurance & Validation

### 8.1 Data Quality Checks
- [ ] **Identifier validation**: Verify HGNC/MONDO/dbSNP IDs against authoritative sources
- [ ] **HGVS validation**: Check HGVS syntax using external validators
- [ ] **Genome build consistency**: Ensure coordinates match declared build
- [ ] **Duplication detection**: Identify and merge duplicate records
- [ ] **Outlier detection**: Flag suspicious values (e.g., age > 120, impossible VAF)

### 8.2 Automated Testing
- [ ] **Unit tests**: Test ETL functions, identifier mapping, data transformations
- [ ] **Integration tests**: Test database queries, API endpoints
- [ ] **Data validation tests**: Ensure imported data meets schema constraints
- [ ] **Regression tests**: Verify analyses produce consistent results

### 8.3 Documentation
- [ ] **API documentation**: Auto-generated from code (Swagger/Redoc)
- [ ] **Data dictionary**: Comprehensive field descriptions
- [ ] **ETL documentation**: Data flow diagrams, transformation logic
- [ ] **User guides**: How-to guides for common tasks
- [ ] **Example queries**: Cookbook of useful queries

---

## 9. Deployment & Infrastructure

### 9.1 Containerization
- [ ] **Docker**: Containerize database, API, web frontend
- [ ] **Docker Compose**: Multi-container setup for local development
- [ ] **Kubernetes**: Production deployment with auto-scaling

### 9.2 Database Management
- [ ] **Backup strategy**: Automated daily backups with retention policy
- [ ] **Replication**: Read replicas for query performance
- [ ] **Partitioning**: Partition large tables (samples, variants) by cancer type/chromosome
- [ ] **Monitoring**: Query performance monitoring, slow query logs

### 9.3 CI/CD
- [ ] **GitHub Actions**: Automated testing on PR
- [ ] **Data refresh pipeline**: Scheduled re-downloads and re-imports
- [ ] **Version control**: Track data versions, schema migrations
- [ ] **Rollback capability**: Ability to revert to previous data version

---

## 10. Advanced Features

### 10.1 Ontology Integration
- [ ] **MONDO hierarchy**: Navigate disease ontology for related diseases
- [ ] **HPO**: Link diseases to phenotypes
- [ ] **GO**: Gene ontology for functional annotations
- [ ] **Semantic reasoning**: Infer relationships via ontology traversal

### 10.2 Batch Processing
- [ ] **Bulk variant annotation**: Upload VCF → annotated VCF with pathogenicity + actionability
- [ ] **Cohort comparison**: Compare mutation profiles of two cohorts
- [ ] **Variant prioritization**: Rank variants by pathogenicity + actionability + frequency

### 10.3 Real-Time Features
- [ ] **Live data updates**: Stream new ClinVar/COSMIC releases
- [ ] **Alerts**: Notify when new actionable variants discovered
- [ ] **Collaborative annotations**: Multi-user variant curation

### 10.4 Privacy & Security
- [ ] **Data de-identification**: Remove/hash patient identifiers for TCGA data
- [ ] **Access control**: Role-based permissions (public, researcher, admin)
- [ ] **Audit logging**: Track data access for compliance
- [ ] **HIPAA compliance**: If handling protected health information

---

## 11. Immediate Next Steps (Tonight/Tomorrow)

### High Priority (Can Start Tonight)
1. **Data profiling scripts**:
   - Count records per source
   - Identify missing/null values
   - Summary statistics (genes, variants, samples)

2. **Basic exploration queries**:
   - Top 20 mutated genes in TCGA-BRCA
   - Gene-disease overlap between ClinGen and GenCC
   - Variant count by pathogenicity classification

3. **Identifier mapping research**:
   - Test HGNC API for gene symbol → HGNC ID
   - Test ClinGen Allele Registry for variant normalization
   - Document API endpoints and rate limits

4. **ETL prototype**:
   - Write parser for GenCC TSV (simplest format)
   - Create sample database schema (1-2 tables)
   - Import subset of data and test queries

5. **CLI skeleton**:
   - Set up Click/Typer CLI framework
   - Implement `harmonaquery stats` command
   - Add basic query commands

### Medium Priority (This Week)
6. **Question answering**: Pick 5 questions from Section 2, write SQL/Python to answer
7. **Visualization prototypes**: Create mutation lollipop plot, oncoprint, survival curve
8. **API skeleton**: Flask/FastAPI setup with 2-3 basic endpoints
9. **Jupyter notebooks**: Create exploratory data analysis notebooks

### Future (After Full Data Downloaded)
10. Complete harmonization implementation
11. Web frontend development
12. ML model training
13. Production deployment

---

## 12. Success Metrics

### Data Quality
- **Identifier coverage**: >95% of genes mapped to HGNC IDs
- **Variant normalization**: >90% of variants mapped to ClinGen Allele IDs
- **Data completeness**: <10% missing values in core fields

### Performance
- **Query latency**: <1s for simple queries, <10s for complex aggregations
- **API throughput**: >100 requests/second
- **Data freshness**: Updates within 1 week of source releases

### Usability
- **API documentation coverage**: 100% of endpoints documented
- **Example coverage**: >20 example queries/use cases
- **User satisfaction**: Positive feedback from initial users

---

*Document created: 2025-10-04*
*Ready for task prioritization and implementation*
