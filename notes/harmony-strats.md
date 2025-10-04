# Harmonization and Schema Mapping Strategies

## Overview

We have successfully downloaded data from 5 open-access genomic/clinical sources:
- **GenCC**: Gene-disease validity (24,151 submissions, CC0)
- **ClinGen**: Gene-disease validity, dosage sensitivity, actionability, variant pathogenicity
- **ClinVar**: Variant-disease relationships (3M+ variants)
- **cBioPortal**: Cancer genomics (BRCA & LUAD studies, multi-omic)
- **TCGA**: Cancer genomics via GDC (clinical, mutations, copy-number data)

The goal is to harmonize these disparate sources into a unified queryable system for Real World Evidence (RWE) analysis and virtual cohort aggregation.

---

## Strategy 1: Entity-Centric Relational Schema (Normalized Database)

### Concept
Create a traditional normalized relational database with separate tables for core biomedical entities (genes, variants, diseases, samples, evidence) linked by foreign keys. This follows standard biomedical data warehouse patterns.

### Core Entities

1. **Genes**
   - Primary identifier: HGNC ID
   - Additional identifiers: HGNC symbol, Entrez Gene ID, Ensembl Gene ID
   - Attributes: chromosome, start, end, strand, biotype

2. **Diseases**
   - Primary identifier: MONDO ID
   - Additional identifiers: OMIM ID, MedGen CUI, Oncotree code
   - Attributes: name, synonyms, category

3. **Variants**
   - Primary identifier: ClinGen Allele ID (canonical)
   - Additional identifiers: dbSNP rs ID, ClinVar Variation ID
   - Attributes: HGVS (genomic, coding, protein), genomic coordinates (GRCh37, GRCh38), variant type

4. **Samples/Patients**
   - Primary identifier: Source-specific ID (e.g., TCGA barcode)
   - Attributes: demographics, diagnosis, treatment, outcomes
   - Source: TCGA, cBioPortal studies

5. **Evidence/Assertions**
   - Links entities with classification/interpretation
   - Attributes: assertion type, classification, evidence level, submitter, date

### Schema Structure

```sql
-- Core entities
CREATE TABLE genes (
    hgnc_id VARCHAR(20) PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,
    entrez_id INTEGER,
    ensembl_id VARCHAR(20),
    chromosome VARCHAR(10),
    start_grch38 BIGINT,
    end_grch38 BIGINT,
    strand CHAR(1)
);

CREATE TABLE diseases (
    mondo_id VARCHAR(20) PRIMARY KEY,
    name TEXT NOT NULL,
    omim_id VARCHAR(20),
    medgen_cui VARCHAR(20),
    oncotree_code VARCHAR(20),
    category VARCHAR(100)
);

CREATE TABLE variants (
    clingen_allele_id VARCHAR(20) PRIMARY KEY,
    dbsnp_rs_id VARCHAR(20),
    clinvar_variation_id VARCHAR(20),
    hgvs_genomic_grch38 TEXT,
    hgvs_coding TEXT,
    hgvs_protein TEXT,
    chromosome VARCHAR(10),
    position_grch38 BIGINT,
    ref_allele TEXT,
    alt_allele TEXT,
    variant_type VARCHAR(50)
);

CREATE TABLE samples (
    sample_id VARCHAR(100) PRIMARY KEY,
    source VARCHAR(50) NOT NULL,  -- 'TCGA', 'cBioPortal-BRCA', etc.
    patient_id VARCHAR(100),
    sample_type VARCHAR(50),  -- 'primary tumor', 'normal', etc.
    cancer_type VARCHAR(100),
    age_at_diagnosis INTEGER,
    sex VARCHAR(10),
    race VARCHAR(50),
    ethnicity VARCHAR(50)
);

-- Relationship tables
CREATE TABLE gene_disease_validity (
    id SERIAL PRIMARY KEY,
    hgnc_id VARCHAR(20) REFERENCES genes(hgnc_id),
    mondo_id VARCHAR(20) REFERENCES diseases(mondo_id),
    classification VARCHAR(50) NOT NULL,  -- 'Definitive', 'Strong', etc.
    mode_of_inheritance VARCHAR(100),
    source VARCHAR(50) NOT NULL,  -- 'ClinGen', 'GenCC', etc.
    submitter VARCHAR(200),
    evidence_pmids TEXT[],
    assertion_date DATE,
    UNIQUE(hgnc_id, mondo_id, source, submitter)
);

CREATE TABLE variant_pathogenicity (
    id SERIAL PRIMARY KEY,
    clingen_allele_id VARCHAR(20) REFERENCES variants(clingen_allele_id),
    mondo_id VARCHAR(20) REFERENCES diseases(mondo_id),
    clinical_significance VARCHAR(50) NOT NULL,  -- 'Pathogenic', 'Benign', etc.
    review_status VARCHAR(100),
    source VARCHAR(50) NOT NULL,  -- 'ClinVar', 'ClinGen'
    submitter VARCHAR(200),
    evidence_pmids TEXT[],
    assertion_date DATE
);

CREATE TABLE sample_variants (
    id SERIAL PRIMARY KEY,
    sample_id VARCHAR(100) REFERENCES samples(sample_id),
    clingen_allele_id VARCHAR(20) REFERENCES variants(clingen_allele_id),
    variant_source VARCHAR(50),  -- 'somatic', 'germline'
    variant_allele_fraction FLOAT,
    read_depth INTEGER,
    source_file VARCHAR(200)
);

CREATE TABLE gene_dosage_sensitivity (
    id SERIAL PRIMARY KEY,
    hgnc_id VARCHAR(20) REFERENCES genes(hgnc_id),
    haploinsufficiency_score INTEGER,  -- 0-3, 30, 40
    triplosensitivity_score INTEGER,
    source VARCHAR(50) DEFAULT 'ClinGen',
    assertion_date DATE
);

-- Expression/molecular data
CREATE TABLE gene_expression (
    id SERIAL PRIMARY KEY,
    sample_id VARCHAR(100) REFERENCES samples(sample_id),
    hgnc_id VARCHAR(20) REFERENCES genes(hgnc_id),
    expression_value FLOAT NOT NULL,
    expression_unit VARCHAR(20),  -- 'TPM', 'FPKM', 'counts'
    data_type VARCHAR(50),  -- 'RNA-Seq', 'microarray'
    source_file VARCHAR(200)
);

CREATE TABLE copy_number_alterations (
    id SERIAL PRIMARY KEY,
    sample_id VARCHAR(100) REFERENCES samples(sample_id),
    chromosome VARCHAR(10) NOT NULL,
    start_position BIGINT NOT NULL,
    end_position BIGINT NOT NULL,
    segment_mean FLOAT,  -- log2 ratio
    num_probes INTEGER,
    source_file VARCHAR(200)
);
```

### Data Flow

1. **Extract & Transform**:
   - Parse GenCC TSV → extract HGNC symbols, MONDO IDs → insert into `gene_disease_validity`
   - Parse ClinGen CSVs → normalize gene/disease identifiers → insert into `gene_disease_validity`, `gene_dosage_sensitivity`
   - Parse ClinVar VCF/XML → variant normalization (via ClinGen Allele Registry API) → insert into `variants`, `variant_pathogenicity`
   - Parse TCGA clinical XML → extract patient demographics → insert into `samples`
   - Parse TCGA MAF files → variant normalization → insert into `variants`, `sample_variants`
   - Parse cBioPortal mutation files → similar to TCGA MAF

2. **Load**:
   - Bulk insert via PostgreSQL COPY or batch inserts
   - Create indexes on foreign keys and commonly queried fields
   - Materialize summary views for common queries

### Expected Results

**Database Size**: ~10-50 GB (depending on variant deduplication)

**Query Examples**:
```sql
-- Find all pathogenic variants in BRCA1 associated with breast cancer
SELECT v.hgvs_protein, vp.clinical_significance, vp.review_status
FROM variants v
JOIN variant_pathogenicity vp ON v.clingen_allele_id = vp.clingen_allele_id
JOIN diseases d ON vp.mondo_id = d.mondo_id
JOIN genes g ON v.hgvs_coding LIKE CONCAT('%', g.symbol, '%')
WHERE g.symbol = 'BRCA1'
  AND d.name LIKE '%breast%'
  AND vp.clinical_significance IN ('Pathogenic', 'Likely pathogenic');

-- Virtual cohort: TCGA breast cancer patients with TP53 mutations
SELECT s.sample_id, s.age_at_diagnosis, v.hgvs_protein
FROM samples s
JOIN sample_variants sv ON s.sample_id = sv.sample_id
JOIN variants v ON sv.clingen_allele_id = v.clingen_allele_id
WHERE s.cancer_type = 'Breast Invasive Carcinoma'
  AND v.hgvs_coding LIKE '%TP53%';
```

### Advantages
- ✅ Standard SQL queries, mature tooling
- ✅ ACID compliance, data integrity
- ✅ Easy to understand and maintain
- ✅ Efficient joins and aggregations
- ✅ Works well with BI tools (Tableau, Looker, etc.)

### Disadvantages
- ❌ Rigid schema - requires migrations for new data types
- ❌ Identifier normalization bottleneck (variant/gene/disease mapping)
- ❌ Complex queries for graph-like relationships (gene networks, pathways)
- ❌ Denormalization needed for performance on large aggregations

---

## Strategy 2: Document-Oriented Schema (JSON/NoSQL with Search Index)

### Concept
Store harmonized data as JSON documents in a document database (MongoDB, Elasticsearch) or JSONB in PostgreSQL. Each document represents a high-level entity with nested/embedded related data. Optimized for flexible schema evolution and full-text search.

### Document Types

1. **Gene Document**
```json
{
  "_id": "HGNC:1100",
  "identifiers": {
    "hgnc_id": "HGNC:1100",
    "symbol": "BRCA1",
    "entrez_id": 672,
    "ensembl_id": "ENSG00000012048"
  },
  "location": {
    "chromosome": "17",
    "grch38": {"start": 43044295, "end": 43125483, "strand": "-"}
  },
  "disease_associations": [
    {
      "disease": {"mondo_id": "MONDO:0007254", "name": "Breast-ovarian cancer, familial, susceptibility to, 1"},
      "validity": "Definitive",
      "mode_of_inheritance": "Autosomal dominant",
      "source": "ClinGen",
      "submitter": "ClinGen Hereditary Cancer Clinical Domain Working Group",
      "evidence": {"pmids": ["7545954", "8589730"], "date": "2020-01-15"}
    },
    {
      "disease": {"mondo_id": "MONDO:0007254", "name": "Familial breast-ovarian cancer"},
      "validity": "Definitive",
      "source": "GenCC",
      "submitter": "Orphanet",
      "evidence": {"date": "2023-05-10"}
    }
  ],
  "dosage_sensitivity": {
    "haploinsufficiency": 3,
    "triplosensitivity": 0,
    "source": "ClinGen",
    "date": "2021-03-20"
  },
  "oncogenicity": {
    "classification": "Tumor suppressor",
    "cancer_types": ["Breast cancer", "Ovarian cancer"],
    "source": "OncoKB"
  }
}
```

2. **Variant Document**
```json
{
  "_id": "CA123456",
  "identifiers": {
    "clingen_allele_id": "CA123456",
    "dbsnp_rs_id": "rs80357906",
    "clinvar_variation_id": "43054"
  },
  "hgvs": {
    "genomic_grch38": "NC_000017.11:g.43094464C>T",
    "coding": "NM_007294.3:c.5266dupC",
    "protein": "NP_009225.1:p.Gln1756ProfsTer74"
  },
  "location": {
    "chromosome": "17",
    "grch38_position": 43094464,
    "ref": "C",
    "alt": "T"
  },
  "variant_type": "frameshift",
  "gene": {"hgnc_id": "HGNC:1100", "symbol": "BRCA1"},
  "pathogenicity_assertions": [
    {
      "disease": {"mondo_id": "MONDO:0007254", "name": "Familial breast-ovarian cancer"},
      "classification": "Pathogenic",
      "review_status": "criteria provided, multiple submitters, no conflicts",
      "source": "ClinVar",
      "submitters": ["CSER _CC_", "GeneDx", "Ambry Genetics"],
      "evidence": {"pmids": ["15889792"], "date": "2024-01-10"}
    }
  ],
  "population_frequency": {
    "gnomad_v3": {"af": 0.0001234, "ac": 15, "an": 121456}
  },
  "sample_observations": [
    {
      "sample_id": "TCGA-A2-A0T4-01A",
      "cancer_type": "Breast Invasive Carcinoma",
      "variant_allele_fraction": 0.42,
      "read_depth": 150,
      "source": "TCGA"
    }
  ]
}
```

3. **Sample/Patient Document**
```json
{
  "_id": "TCGA-A2-A0T4",
  "source": "TCGA-BRCA",
  "demographics": {
    "age_at_diagnosis": 52,
    "sex": "Female",
    "race": "White",
    "ethnicity": "Not Hispanic or Latino"
  },
  "diagnosis": {
    "cancer_type": "Breast Invasive Carcinoma",
    "histology": "Infiltrating Ductal Carcinoma",
    "stage": "Stage IIA",
    "grade": "G3",
    "diagnosis_date": "2010-05-12"
  },
  "samples": [
    {
      "sample_id": "TCGA-A2-A0T4-01A",
      "sample_type": "Primary Tumor",
      "barcode": "TCGA-A2-A0T4-01A-11D-A096-01"
    }
  ],
  "somatic_mutations": [
    {
      "gene": "TP53",
      "hgvs_protein": "p.Arg248Gln",
      "variant_allele_fraction": 0.38,
      "classification": "Likely Oncogenic"
    },
    {
      "gene": "PIK3CA",
      "hgvs_protein": "p.His1047Arg",
      "variant_allele_fraction": 0.45,
      "classification": "Oncogenic"
    }
  ],
  "copy_number_alterations": [
    {
      "gene": "ERBB2",
      "alteration": "Amplification",
      "log2_ratio": 1.8
    }
  ],
  "gene_expression": {
    "ESR1": {"tpm": 450.2, "fpkm": 380.5},
    "PGR": {"tpm": 120.8, "fpkm": 102.3},
    "ERBB2": {"tpm": 850.6, "fpkm": 720.1}
  },
  "treatment": [
    {
      "drug": "Tamoxifen",
      "start_date": "2010-06-15",
      "end_date": "2015-06-15"
    }
  ],
  "outcomes": {
    "vital_status": "Alive",
    "days_to_last_followup": 1825,
    "progression_free_survival_days": 1500
  }
}
```

### Data Flow

1. **Extract & Transform**:
   - Parse each source file
   - Create entity documents with embedded relationships
   - Denormalize frequently accessed data (e.g., gene symbol embedded in variant docs)
   - Resolve identifiers via mapping tables/APIs

2. **Load**:
   - Bulk insert into Elasticsearch/MongoDB
   - Create full-text search indexes on key fields (gene symbols, disease names, HGVS)
   - Create aggregation pipelines for common analytics

### Expected Results

**Storage**: ~15-100 GB (more overhead due to denormalization, but flexible)

**Query Examples** (Elasticsearch Query DSL):
```json
// Find all pathogenic BRCA1 variants
{
  "query": {
    "bool": {
      "must": [
        {"term": {"gene.symbol": "BRCA1"}},
        {"terms": {"pathogenicity_assertions.classification": ["Pathogenic", "Likely pathogenic"]}}
      ]
    }
  }
}

// Full-text search for "Lynch syndrome" patients
{
  "query": {
    "multi_match": {
      "query": "Lynch syndrome",
      "fields": ["diagnosis.cancer_type", "somatic_mutations.gene"]
    }
  }
}

// Aggregate: Count patients by cancer type and TP53 mutation status
{
  "aggs": {
    "by_cancer_type": {
      "terms": {"field": "diagnosis.cancer_type"},
      "aggs": {
        "has_tp53_mutation": {
          "filter": {"term": {"somatic_mutations.gene": "TP53"}}
        }
      }
    }
  }
}
```

### Advantages
- ✅ Flexible schema - easy to add new fields/sources
- ✅ Fast full-text search and aggregations
- ✅ Natural representation of nested/hierarchical data
- ✅ Horizontal scalability (sharding)
- ✅ No complex joins needed for most queries

### Disadvantages
- ❌ Data duplication (denormalization)
- ❌ Harder to maintain referential integrity
- ❌ Complex updates (e.g., updating gene symbol requires updating all variant docs)
- ❌ Steeper learning curve (Query DSL vs SQL)
- ❌ Less mature analytics tooling compared to SQL

---

## Strategy 3: Knowledge Graph (RDF/Property Graph)

### Concept
Model data as a graph with nodes (genes, variants, diseases, samples) and edges (relationships, assertions). Use RDF/SPARQL (semantic web) or property graph databases like Neo4j. Optimized for complex relationship queries and reasoning.

### Graph Schema (Property Graph Model - Neo4j)

**Node Types**:
- `Gene` (properties: hgnc_id, symbol, entrez_id, chromosome, start, end)
- `Variant` (properties: clingen_allele_id, hgvs_genomic, hgvs_protein, chromosome, position)
- `Disease` (properties: mondo_id, name, omim_id, category)
- `Sample` (properties: sample_id, source, age, sex, cancer_type)
- `Patient` (properties: patient_id, demographics)
- `Evidence` (properties: pmids, assertion_date, submitter)
- `Assertion` (properties: classification, review_status, date)

**Relationship Types**:
- `(Gene)-[:ASSOCIATED_WITH]->(Disease)` (properties: validity, mode_of_inheritance, source)
- `(Variant)-[:PATHOGENIC_FOR]->(Disease)` (properties: classification, review_status, source)
- `(Variant)-[:LOCATED_IN]->(Gene)` (properties: consequence_type)
- `(Sample)-[:HAS_VARIANT]->(Variant)` (properties: vaf, read_depth, variant_source)
- `(Sample)-[:BELONGS_TO]->(Patient)`
- `(Sample)-[:DIAGNOSED_WITH]->(Disease)`
- `(Gene)-[:HAPLOINSUFFICIENT]->()` (properties: score)
- `(Assertion)-[:SUPPORTS]->(:Gene)-[:ASSOCIATED_WITH]->(:Disease)`
- `(Evidence)-[:SUPPORTS]->(Assertion)`

### Cypher Example Queries (Neo4j)

```cypher
// Find all pathogenic variants in genes associated with breast cancer
MATCH (g:Gene)-[assoc:ASSOCIATED_WITH]->(d:Disease)<-[path:PATHOGENIC_FOR]-(v:Variant)-[:LOCATED_IN]->(g)
WHERE d.name CONTAINS 'breast'
  AND assoc.validity IN ['Definitive', 'Strong']
  AND path.classification IN ['Pathogenic', 'Likely pathogenic']
RETURN g.symbol, v.hgvs_protein, path.classification, d.name

// Find patients with TP53 mutations who also have BRCA1/2 variants
MATCH (p:Patient)<-[:BELONGS_TO]-(s:Sample)-[:HAS_VARIANT]->(v1:Variant)-[:LOCATED_IN]->(g1:Gene {symbol: 'TP53'})
MATCH (s)-[:HAS_VARIANT]->(v2:Variant)-[:LOCATED_IN]->(g2:Gene)
WHERE g2.symbol IN ['BRCA1', 'BRCA2']
RETURN p.patient_id, s.sample_id,
       v1.hgvs_protein AS tp53_variant,
       v2.hgvs_protein AS brca_variant

// Find genes with shared disease associations (gene co-occurrence network)
MATCH (g1:Gene)-[:ASSOCIATED_WITH]->(d:Disease)<-[:ASSOCIATED_WITH]-(g2:Gene)
WHERE g1.symbol < g2.symbol  // avoid duplicates
WITH g1, g2, count(d) AS shared_diseases
WHERE shared_diseases >= 2
RETURN g1.symbol, g2.symbol, shared_diseases
ORDER BY shared_diseases DESC

// Multi-hop: Find variants in genes associated with diseases similar to Lynch syndrome
MATCH (d1:Disease {name: 'Lynch syndrome'})-[:SIMILAR_TO*1..2]-(d2:Disease)<-[:ASSOCIATED_WITH]-(g:Gene)<-[:LOCATED_IN]-(v:Variant)
WHERE EXISTS((v)-[:PATHOGENIC_FOR]->())
RETURN DISTINCT v.hgvs_protein, g.symbol, d2.name
```

### SPARQL Example (RDF/Semantic Web Model)

```sparql
PREFIX hgnc: <http://identifiers.org/hgnc/>
PREFIX mondo: <http://purl.obolibrary.org/obo/MONDO_>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# Find genes associated with breast cancer subtypes via MONDO hierarchy
SELECT ?gene ?geneLabel ?disease ?diseaseLabel ?validity
WHERE {
  ?disease rdfs:subClassOf* mondo:0007254 .  # Familial breast cancer
  ?gene obo:RO_0003304 ?disease .  # causally associated with
  ?gene rdfs:label ?geneLabel .
  ?disease rdfs:label ?diseaseLabel .

  ?assertion a :GeneDiseaseAssertion ;
             :subject ?gene ;
             :object ?disease ;
             :validity ?validity .

  FILTER(?validity IN ("Definitive", "Strong"))
}
```

### Data Flow

1. **Extract & Transform**:
   - Parse source files
   - Create nodes for each entity (with properties)
   - Create relationships based on assertions/associations
   - Link to external ontologies (MONDO, HPO, GO) for reasoning

2. **Load**:
   - Batch import via Neo4j LOAD CSV or Python driver
   - Create indexes on node properties (hgnc_id, mondo_id, sample_id)
   - Optionally add ontology hierarchies for semantic reasoning

### Expected Results

**Storage**: ~5-30 GB (efficient storage of relationships)

**Performance**: Excellent for graph traversal queries (multi-hop, shortest path, network analysis)

### Advantages
- ✅ Natural representation of relationships and networks
- ✅ Excellent for complex graph queries (co-occurrence, pathways, multi-hop)
- ✅ Can integrate with biomedical ontologies (MONDO, HPO, GO)
- ✅ Visual graph exploration tools (Neo4j Browser, Bloom)
- ✅ Supports reasoning and inference (especially RDF/SPARQL)
- ✅ Performance doesn't degrade with deeply nested relationships

### Disadvantages
- ❌ Steeper learning curve (Cypher, SPARQL)
- ❌ Less mature analytics/BI tooling
- ❌ Aggregations can be slower than columnar databases
- ❌ Requires different mindset from SQL
- ❌ Scaling horizontally can be complex

---

## Comparison Matrix

| Aspect | Relational DB | Document Store | Knowledge Graph |
|--------|---------------|----------------|-----------------|
| **Query Language** | SQL (familiar) | Query DSL / MongoDB query | Cypher / SPARQL (graph-specific) |
| **Schema Flexibility** | Rigid, requires migrations | Flexible, schema-on-read | Flexible, easy to add relationships |
| **Best For** | Structured queries, aggregations, reporting | Full-text search, flexible data, rapid iteration | Complex relationships, graph analysis, reasoning |
| **Performance (Simple Queries)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Performance (Graph Queries)** | ⭐⭐ (complex joins) | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Performance (Full-Text Search)** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Data Integrity** | ⭐⭐⭐⭐⭐ (ACID, FKs) | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Scalability** | ⭐⭐⭐ (vertical) | ⭐⭐⭐⭐⭐ (horizontal) | ⭐⭐⭐⭐ |
| **Learning Curve** | ⭐⭐ (familiar SQL) | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **BI Tool Integration** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Ontology Integration** | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## Hybrid Recommendation

**Recommended Approach**: **Multi-Model Database Strategy**

Use PostgreSQL with both relational tables and JSONB columns, plus optional Elasticsearch for search.

### Architecture

1. **PostgreSQL (Primary)**:
   - Core entities in normalized tables (genes, diseases, variants, samples)
   - Foreign keys for referential integrity
   - JSONB columns for flexible/nested data (e.g., evidence, clinical attributes)
   - Full-text search indexes (GIN) on JSONB
   - Materialized views for common aggregations

2. **Elasticsearch (Optional - Search Layer)**:
   - Synchronized subset of data for full-text search
   - Document-oriented representation for fast lookups
   - Aggregation pipelines for dashboards

3. **Neo4j (Optional - Graph Layer)**:
   - Synchronized subset for complex relationship queries
   - Gene-disease-variant network analysis
   - Pathway and interaction exploration

### Benefits
- ✅ Start with familiar SQL/PostgreSQL
- ✅ Add flexibility with JSONB for evolving schema
- ✅ Optionally add search/graph layers as needed
- ✅ ACID guarantees for core data
- ✅ Scalable with read replicas and partitioning

### Implementation Path
1. **Phase 1**: Build normalized PostgreSQL schema with JSONB for extensions
2. **Phase 2**: Add full-text search indexes, create API layer
3. **Phase 3**: (Optional) Sync to Elasticsearch for advanced search
4. **Phase 4**: (Optional) Sync to Neo4j for network analysis

---

## Next Steps

1. **Identifier Normalization**:
   - Map all gene symbols to HGNC IDs (via HGNC API)
   - Map all disease terms to MONDO IDs (via MONDO ontology)
   - Normalize variants to ClinGen Allele IDs (via Allele Registry API)

2. **Schema Implementation**:
   - Create database schema (recommend PostgreSQL + JSONB)
   - Write ETL scripts for each data source
   - Implement deduplication and conflict resolution logic

3. **Data Quality**:
   - Validate identifier mappings
   - Check for duplicate records
   - Implement data versioning/provenance tracking

4. **Query Optimization**:
   - Create indexes on frequently queried fields
   - Build materialized views for dashboards
   - Implement caching layer for common queries

5. **API Development**:
   - RESTful API for CRUD operations
   - GraphQL for flexible querying
   - Query templates for common RWE use cases

---

*Document created: 2025-10-04*
*Ready for implementation planning and prototyping*
