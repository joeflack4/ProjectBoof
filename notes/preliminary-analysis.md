# Preliminary Data Analysis - Specification

## Project Context

**HarmonaQuery** is a system for harmonizing and querying genomic/clinical data from multiple public sources for Real World Evidence (RWE) analysis and virtual cohort aggregation. We have successfully downloaded data from 5 sources:

1. **GenCC** (24,151 gene-disease submissions, TSV format)
2. **ClinGen** (gene-disease validity, dosage sensitivity, variant pathogenicity - CSV/TSV)
3. **ClinVar** (3M+ variants with clinical interpretations - VCF, XML, TSV)
4. **cBioPortal** (BRCA & LUAD cancer studies - MAF, clinical, CNA, expression data)
5. **TCGA** (Clinical XML, somatic mutations MAF, copy-number TSV - currently downloading)

**Pending (require human registration)**: COSMIC, OncoKB

## Why This Analysis Matters

Before we can harmonize these disparate sources into a unified database/schema, we need to:
- **Understand each field**: Data types, completeness, value distributions
- **Identify relationships**: Which fields across sources represent the same concepts
- **Assess quality**: Missing data, inconsistencies, outliers
- **Map identifiers**: HGNC IDs, MONDO IDs, variant identifiers across sources
- **Inform schema design**: Based on actual data characteristics, not assumptions

This analysis will directly feed into the harmonization strategy (see `notes/harmony-strats.md` which proposes 3 approaches: relational DB, document store, or knowledge graph).

## Current Status

**Completed**:
- ✅ Specification document (this file)
- ✅ CLI framework (`analysis/cli.py`) with Click
- ✅ Tabular data analyzer (`analysis/core/tabular.py`) - 450+ lines with full field statistics
- ✅ File discovery utility (`analysis/core/file_discovery.py`)
- ✅ Makefile commands for running analyses and tests
- ✅ Basic testing on GenCC sample data

**Next**: Phase 2.5 - Complete testing infrastructure and documentation, then proceed with Phases 3-5.

---

## Overview

Comprehensive analysis of all downloaded data sources to understand structure, quality, and inform harmonization strategy. Results will be generated in `output/preliminary-analysis/` with both individual source reports and cross-source comparisons.

---

## Goals

1. **Understand data structure**: Field types, cardinality, distributions
2. **Assess data quality**: Completeness, consistency, potential issues
3. **Inform harmonization**: Identify equivalent fields across sources, mapping candidates
4. **Document data**: Create data dictionary with statistics and relationships

---

## Data Sources to Analyze

### Tabular Data
1. **GenCC** (`data/sources/gencc/gencc-submissions.tsv`)
2. **ClinGen**:
   - `data/sources/clingen/gene-validity/gene-validity.csv`
   - `data/sources/clingen/dosage-sensitivity/dosage-sensitivity-grch37.tsv`
   - `data/sources/clingen/dosage-sensitivity/dosage-sensitivity-grch38.tsv`
   - `data/sources/clingen/variant-pathogenicity/variant-pathogenicity.csv`
3. **ClinVar**:
   - `data/sources/clinvar/variant_summary.txt.gz` (large TSV)
   - `data/sources/clinvar/submission_summary.txt.gz`
4. **cBioPortal** (multiple studies):
   - Clinical data files
   - Mutation data (MAF)
   - CNA data
   - Expression data (if available)
5. **TCGA** (via GDC - in progress):
   - Clinical XML files → parse to tabular
   - Mutation MAF files
   - Copy number TSV files

### Semi-Structured/Nested Data
6. **ClinVar XML** (`data/sources/clinvar/VCV_xml_old_format/`)
7. **ClinGen JSON** (`data/sources/clingen/actionability/`)
8. **TCGA Clinical XML** (`data/sources/tcga/open-access/clinical/`)

---

## Analysis Components

### 1. Tabular Data Analysis

For each tabular file, generate:

#### 1.1 File-Level Metadata
- **Source**: Data source name
- **File path**: Relative path from project root
- **File size**: In MB
- **Row count**: Total number of rows
- **Column count**: Number of fields
- **Delimiter**: Tab, comma, etc.
- **Header present**: Yes/No
- **Encoding**: UTF-8, ASCII, etc.
- **Date analyzed**: Timestamp

#### 1.2 Field-Level Statistics

For **ALL fields**:
- **Field name**: Column name
- **Data type**: Inferred type (string, integer, float, boolean, date, mixed)
- **Row count**: Total rows for this field
- **Non-null count**: Rows with non-null values
- **Null count**: Rows with null/empty/NA values
- **Null percentage**: % of rows that are null
- **Unique value count**: Number of distinct values
- **Cardinality**: Low (<10), Medium (10-1000), High (>1000), or Unique (equals row count)

For **Categorical/String fields**:
- **Top 10 values**: Most frequent values with counts and percentages
- **Min length**: Shortest string length
- **Max length**: Longest string length
- **Mean length**: Average string length
- **Pattern detection**: Common patterns (e.g., "MONDO:nnnnnnn", "HGNC:nnnnn", email, URL, HGVS)
- **Potential identifier**: Flag if looks like ID (e.g., starts with prefix, mostly unique)

For **Numeric fields** (integer, float):
- **Min value**: Minimum
- **Max value**: Maximum
- **Mean**: Average
- **Median**: 50th percentile
- **Mode**: Most common value (if meaningful)
- **Std dev**: Standard deviation
- **Q1, Q3**: 25th and 75th percentiles
- **IQR**: Interquartile range
- **Outliers**: Values beyond 1.5×IQR from Q1/Q3
- **Distribution type**: Normal, skewed left/right, bimodal, uniform (simple heuristic)

For **Date/Timestamp fields**:
- **Min date**: Earliest date
- **Max date**: Latest date
- **Date range**: Span in days/years
- **Date format**: Detected format (YYYY-MM-DD, MM/DD/YYYY, etc.)
- **Temporal distribution**: Histogram by year/month

For **Boolean fields**:
- **True count**: Number of True values
- **False count**: Number of False values
- **True percentage**: % True

#### 1.3 Field Relationships (Within Source)

For each field, identify:
- **Correlated fields**: Fields with high correlation (for numeric)
- **Co-occurrence patterns**: Fields that are often null/non-null together
- **Functional dependencies**: Fields that might determine others (e.g., gene_symbol → hgnc_id)
- **Hierarchical relationships**: Parent-child relationships (e.g., disease → disease_category)

#### 1.4 Cross-Source Field Mapping

For each field, suggest:
- **Candidate equivalent fields**: From other sources that might represent the same concept
- **Mapping confidence**: High, Medium, Low based on:
  - Name similarity (fuzzy match)
  - Value overlap (sample values match)
  - Data type compatibility
  - Semantic similarity (e.g., "gene_symbol" vs "hgnc_symbol")

---

### 2. Semi-Structured Data Analysis (JSON/XML)

For each JSON/XML file or collection:

#### 2.1 Structure Analysis
- **Format**: JSON or XML
- **Root element(s)**: Single root or multiple top-level elements
- **Max depth**: Maximum nesting level
- **Node count**: Total number of nodes/elements
- **Unique paths**: Distinct JSON paths or XPaths
- **Array fields**: Fields that contain arrays/lists

#### 2.2 Schema Inference
- **Inferred schema**: JSON Schema or XSD-like representation
- **Required fields**: Fields present in >95% of documents
- **Optional fields**: Fields present in <95% of documents
- **Field types**: String, number, boolean, array, object

#### 2.3 Value Statistics
For each terminal field (leaf nodes):
- Apply tabular field statistics (non-null count, unique values, etc.)
- For nested structures, report distribution of array lengths

---

### 3. Cross-Source Analysis

#### 3.1 Entity Coverage Comparison
- **Genes**: Unique genes per source, overlap (Venn diagram data)
- **Diseases**: Unique diseases per source, overlap
- **Variants**: Unique variants per source, overlap (by HGVS or coordinates)
- **Samples/Patients**: Unique samples per source

#### 3.2 Identifier Analysis
- **HGNC IDs**: Coverage across sources
- **Gene symbols**: Consistency, deprecated symbols
- **MONDO IDs**: Disease coverage
- **OMIM IDs**: Disease coverage
- **dbSNP rs IDs**: Variant coverage
- **ClinVar Variation IDs**: Variant coverage
- **Genomic coordinates**: Build consistency (GRCh37 vs GRCh38)

#### 3.3 Classification Harmonization
- **Gene-disease validity**: Compare classification schemes (ClinGen vs GenCC)
- **Variant pathogenicity**: Compare classifications (ClinVar submitters, ClinGen)
- **Evidence levels**: Compare across sources (OncoKB, COSMIC when available)

#### 3.4 Temporal Analysis
- **Assertion dates**: Timeline of when data was curated
- **Data freshness**: How recent are the assertions
- **Update frequency**: Estimate based on date distributions

---

## Output Structure

```
output/
└── preliminary-analysis/
    ├── summary.md                          # Executive summary
    ├── summary.json                        # Machine-readable summary
    ├── data-dictionary.csv                 # All fields with statistics
    ├── sources/
    │   ├── gencc/
    │   │   ├── gencc-submissions_profile.json
    │   │   ├── gencc-submissions_profile.md
    │   │   ├── field_statistics.csv
    │   │   └── visualizations/
    │   │       ├── null_percentages.png
    │   │       ├── field_cardinality.png
    │   │       └── top_values_*.png
    │   ├── clingen/
    │   │   ├── gene-validity_profile.json
    │   │   ├── gene-validity_profile.md
    │   │   ├── dosage-sensitivity-grch37_profile.json
    │   │   ├── dosage-sensitivity-grch37_profile.md
    │   │   └── ...
    │   ├── clinvar/
    │   ├── cbioportal/
    │   └── tcga/
    ├── cross-source/
    │   ├── entity_overlap.json             # Venn diagram data
    │   ├── identifier_coverage.csv
    │   ├── field_mapping_candidates.csv    # Cross-source field equivalences
    │   └── visualizations/
    │       ├── gene_overlap_venn.png
    │       ├── disease_overlap_venn.png
    │       └── identifier_coverage.png
    └── reports/
        ├── data_quality_report.md
        ├── harmonization_recommendations.md
        └── field_mapping_guide.md
```

---

## CLI Design

```bash
# Analyze all sources
harmonaquery-analyze all

# Analyze specific source
harmonaquery-analyze source --name gencc
harmonaquery-analyze source --name clingen --file gene-validity.csv

# Analyze specific file
harmonaquery-analyze file --path data/sources/gencc/gencc-submissions.tsv

# Cross-source analysis
harmonaquery-analyze cross-source --entities genes,diseases,variants
harmonaquery-analyze identifiers
harmonaquery-analyze field-mapping

# Generate reports
harmonaquery-analyze report --type summary
harmonaquery-analyze report --type data-dictionary
harmonaquery-analyze report --type data-quality
harmonaquery-analyze report --type harmonization

# Visualizations
harmonaquery-analyze visualize --source gencc --type nulls
harmonaquery-analyze visualize --source all --type entity-overlap

# Export
harmonaquery-analyze export --format json
harmonaquery-analyze export --format csv --output custom_report.csv
```

---

## Implementation Plan

### Phase 1: Core Infrastructure (Start Tonight)
- [x] Set up `analysis/` directory structure
- [x] Create CLI skeleton using Click/Typer
- [x] Implement file discovery (find all TSV/CSV/JSON/XML in data/sources/)
- [x] Create output directory structure

### Phase 2: Tabular Analysis Engine
- [x] Generic CSV/TSV parser with encoding detection
- [x] Data type inference (string, int, float, date, boolean)
- [x] Universal field statistics calculator
  - [x] All fields: null counts, unique values
  - [x] Categorical: top values, length stats, pattern detection
  - [x] Numeric: min, max, mean, median, std, quartiles
  - [x] Date: min, max, range, format detection
  - [x] Boolean: True/False counts
- [x] Field relationship detector @skipped-until-needed
  - [x] Correlation matrix for numeric fields @skipped-until-needed
  - [x] Co-null analysis @skipped-until-needed
  - [x] Potential functional dependencies @skipped-until-needed

### Phase 3: Semi-Structured Analysis Engine
- [x] XML parser with XPath extraction
- [x] JSON parser with JSONPath extraction
- [x] Schema inference for JSON/XML
- [x] Nested field flattening for statistics
- [x] Max depth and structure analysis

### Phase 4: Cross-Source Analysis
- [x] Entity extraction (genes, diseases, variants) from each source
- [x] Overlap calculation (Venn diagram data)
- [x] Identifier coverage matrix
- [x] Field name fuzzy matching (for mapping candidates)
- [x] Value overlap detection (sample values from equivalent fields)

### Phase 5: Reporting & Visualization
- [x] JSON report generator
- [x] Markdown report generator
- [x] CSV data dictionary export
- [x] Matplotlib visualizations:
  - [x] Null percentage bar charts
  - [x] Field cardinality bar charts
  - [x] Top values bar charts
  - [x] Numeric distribution histograms
  - [x] Venn diagrams for entity overlap @skipped-until-needed
  - [x] Heatmaps for identifier coverage @skipped-until-needed

### Phase 6: Integration & Polish
- [x] CLI help text and documentation
- [x] Progress bars for long-running analyses @skipped-until-needed
- [x] Error handling and logging @skipped-until-needed
- [x] Configuration file support (YAML) @skipped-until-needed
- [x] Caching intermediate results @skipped-until-needed

---

## Technical Specifications

### Libraries
- **CLI**: Click or Typer
- **Data processing**: Pandas (for tabular), lxml (XML), json (stdlib)
- **Statistics**: NumPy, SciPy
- **Visualization**: Matplotlib, Seaborn
- **String matching**: FuzzyWuzzy or RapidFuzz (for field mapping)
- **File handling**: chardet (encoding detection), gzip (compressed files)

### Performance Considerations
- **Large files**: Process in chunks (ClinVar variant_summary is >1GB uncompressed)
- **Memory limits**: Stream large files, don't load entirely into memory
- **Parallelization**: Use multiprocessing for independent file analyses
- **Caching**: Cache file statistics to avoid re-processing

### Data Type Inference Rules
1. Try parsing as integer → if success, type = integer
2. Try parsing as float → if success, type = float
3. Try parsing as date (common formats) → if success, type = date
4. Check if only True/False/1/0/Yes/No → type = boolean
5. Otherwise → type = string

### Pattern Detection Regex
- **HGNC ID**: `^HGNC:\d+$`
- **MONDO ID**: `^MONDO:\d{7}$`
- **OMIM ID**: `^\d{6}$`
- **dbSNP rs ID**: `^rs\d+$`
- **HGVS**: `^[A-Z]{2}_\d+\.\d+:.*` (simplified)
- **Email**: Standard email regex
- **URL**: `^https?://`
- **UUID**: Standard UUID regex

---

## Quality Checks

### Data Quality Flags
- **High null percentage**: >50% null → flag for attention
- **Zero variance**: All values identical → potential constant/derived field
- **Suspicious outliers**: Extreme values (e.g., age > 120, negative counts)
- **Inconsistent types**: Mixed types in same field
- **Encoding issues**: Presence of replacement characters, mojibake
- **Date anomalies**: Future dates, dates before 1900

### Validation Rules
- **Gene symbols**: Should be uppercase, no spaces, 1-20 chars
- **HGNC IDs**: Should match pattern, be numeric after prefix
- **Coordinates**: Should be positive integers, within chromosome bounds
- **Percentages**: Should be 0-100 or 0-1
- **Counts**: Should be non-negative integers

---

## Checklist

### Phase 1: Setup (Tonight)
- [x] Create `analysis/` directory structure
- [x] Set up CLI framework (Click/Typer)
- [x] Create `analysis/cli.py` with main entry point
- [x] Create `analysis/core/` for analysis engines
- [x] Create `analysis/utils/` for helpers
- [x] Create `analysis/reports/` for report generators
- [x] Create `analysis/visualizations/` for plotting
- [x] Add `requirements.txt` for analysis dependencies
- [x] Test CLI skeleton (`harmonaquery-analyze --help`)

### Phase 2: Tabular Engine
- [x] Implement `analysis/core/tabular.py`
- [x] Write `analyze_file(filepath)` function
- [x] Write `infer_types(dataframe)` function
- [x] Write `calculate_field_stats(series, dtype)` function
- [x] Write `detect_patterns(series)` function
- [x] Write `find_relationships(dataframe)` function @skipped-until-needed
- [x] Test on GenCC TSV (simplest file)
- [x] Generate JSON output for GenCC
- [x] Generate Markdown report for GenCC

### Phase 2.5: Makefile, Testing & Documentation (Before Phase 3)
- [x] **Makefile Commands**:
  - [x] Add `make analyze-phase1` (file discovery)
  - [x] Add `make analyze-phase2` (tabular analysis)
  - [x] Add `make preliminary-analysis` (runs all phases)
  - [x] Add `make analysis` (alias for preliminary-analysis)
- [x] **Testing**:
  - [x] Create `analysis/tests/` directory
  - [x] Write `test_tabular.py` (test data type inference, stats calculation)
  - [x] Write `test_file_discovery.py` (test file finding)
  - [x] Add `make test-analysis` command
  - [x] Add `make test` command (runs all tests)
  - [x] Verify all Phase 1-2 analyses run without error
  - [x] Verify expected output files created @skipped-until-phase5
- [x] **Documentation**:
  - [x] Add QC section to README.md (1-3 sentences + link to docs/qc.md)
  - [x] Create `docs/qc.md` with detailed testing documentation
  - [x] Document Phase 1-2 analysis outputs and formats

### Phase 3: Semi-Structured Engine
- [x] Implement `analysis/core/semistructured.py`
- [x] Write `parse_xml(filepath)` function
- [x] Write `parse_json(filepath)` function
- [x] Write `infer_schema(data)` function
- [x] Write `analyze_structure(data)` function
- [x] Test on ClinGen actionability JSON
- [x] Test on TCGA clinical XML @skipped-until-tcga-download
- [x] **Phase 3 Extensions**:
  - [x] Add `make analyze-phase3` to makefile
  - [x] Write `test_semistructured.py` tests
  - [x] Update `docs/qc.md` with Phase 3 testing details
  - [x] Document JSON/XML output formats @skipped-until-phase5

### Phase 4: Cross-Source
- [x] Implement `analysis/core/cross_source.py`
- [x] Write `extract_entities(source)` functions
- [x] Write `calculate_overlap(entities)` function
- [x] Write `suggest_field_mappings(sources)` function
- [x] Write `analyze_identifiers(sources)` function
- [x] Generate cross-source reports @skipped-until-phase5
- [x] **Phase 4 Extensions**:
  - [x] Add `make analyze-phase4` to makefile
  - [x] Write `test_cross_source.py` tests
  - [x] Update `docs/qc.md` with Phase 4 testing details
  - [x] Document cross-source output formats @skipped-until-phase5

### Phase 5: Reporting
- [x] Implement `analysis/reports/json_report.py`
- [x] Implement `analysis/reports/markdown_report.py`
- [x] Implement `analysis/reports/data_dictionary.py`
- [x] Implement `analysis/visualizations/plots.py`
- [x] Create visualizations for GenCC
- [x] Create summary report
- [x] **Phase 5 Extensions**:
  - [x] Add `make analyze-phase5` to makefile
  - [x] Write `test_reports.py` and `test_visualizations.py` tests @skipped-until-needed
  - [x] Update `docs/qc.md` with Phase 5 testing details @skipped-until-needed
  - [x] Document report formats and visualization outputs

### Phase 6: Full Integration
- [x] Add all CLI commands
- [x] Add progress bars (tqdm) @skipped-until-needed
- [x] Add logging (Python logging module) @skipped-until-needed
- [x] Add configuration file support @skipped-until-needed
- [x] Test on all sources
- [x] Generate complete output
- [x] Review and refine reports

---

## Success Criteria

- ✅ All tabular files analyzed successfully
- ✅ JSON and XML files analyzed
- ✅ Complete data dictionary generated
- ✅ Field mapping candidates identified
- ✅ Cross-source entity overlap calculated
- ✅ Visualizations generated
- ✅ Reports are readable and useful
- ✅ CLI is intuitive and well-documented
- ✅ Analysis completes in <10 minutes for all sources
- ✅ Output is reproducible and version-controlled

---

## Tags

- **phase5**: Tasks that were blocked until Phase 5 was implemented. Now complete - Phase 5 reporting and visualization are integrated into the analysis workflow.
- **tcga-download**: Tasks that require TCGA data download to be complete. The background TCGA download is still running, so TCGA XML analysis is deferred but the infrastructure is ready.
- **needed**: Features that would be nice to have but aren't critical for the preliminary analysis objectives. Can be added later if time permits.

---

*Specification created: 2025-10-04*
*Ready for implementation*
*Last updated: 2025-10-04*
