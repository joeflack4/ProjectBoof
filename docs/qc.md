# Quality Control & Testing

## Overview

The HarmonaQuery analysis system includes comprehensive testing to ensure data analysis reliability and correctness. The testing philosophy emphasizes:

- **Unit testing**: Individual functions tested with known inputs and expected outputs
- **Integration testing**: End-to-end workflows tested with real data samples
- **Defensive coding**: Robust handling of edge cases like null values, encoding issues, and malformed data
- **Continuous validation**: Tests run on every change to catch regressions early

## Running Tests

```bash
# Run all analysis tests
make test-analysis

# Run all project tests (when more test suites are added)
make test

# Run tests with verbose output
python3 -m pytest analysis/tests/ -v

# Run specific test file
python3 -m pytest analysis/tests/test_tabular.py -v

# Run specific test class or function
python3 -m pytest analysis/tests/test_tabular.py::TestInferDataType::test_integer_type -v
```

## Test Coverage

### Phase 1-2: Tabular Data Analysis Tests

#### Data Type Inference (`test_tabular.py::TestInferDataType`)
Tests the `infer_data_type()` function's ability to correctly identify field types:

- **Integer detection**: Validates recognition of whole numbers
- **Float detection**: Handles decimal values and scientific notation
- **String detection**: Correctly identifies text fields
- **Boolean detection**: Recognizes true/false, yes/no, 1/0, t/f variations
- **Date detection**: Supports multiple date formats (YYYY-MM-DD, MM/DD/YYYY, ISO 8601, etc.)
- **Empty fields**: Handles all-null columns gracefully
- **Mixed types with nulls**: Correctly infers type even when NaN values are present

**Why it matters**: Accurate type detection drives all downstream statistics calculation. Wrong type inference leads to incorrect analysis.

#### Identifier Pattern Detection (`test_tabular.py::TestDetectIdentifierPattern`)
Tests the `detect_identifier_pattern()` function for recognizing common biomedical identifiers:

- **HGNC IDs**: Gene identifiers (e.g., HGNC:1234)
- **MONDO IDs**: Disease ontology IDs (e.g., MONDO:0000001)
- **dbSNP rs IDs**: Variant identifiers (e.g., rs123456)
- **URLs**: Web links in data fields
- **Pattern threshold**: Ensures 80%+ match rate before flagging as identifier

**Why it matters**: Identifying fields that contain standardized identifiers enables cross-source linking and entity extraction.

#### Basic Statistics (`test_tabular.py::TestCalculateBasicStats`)
Tests the `calculate_basic_stats()` function:

- **Count statistics**: Total, non-null, null counts and percentages
- **Uniqueness**: Counts distinct values
- **Cardinality classification**: Low (<10 unique), medium (10-1000), high (>1000), or unique (all distinct)

**Why it matters**: These fundamental statistics inform data quality assessment and schema design decisions.

#### String Field Statistics (`test_tabular.py::TestCalculateStringStats`)
Tests string-specific analysis:

- **Length statistics**: Min, max, mean string lengths
- **Top values**: Most frequent values with counts and percentages
- **Pattern detection integration**: Links to identifier pattern detection

**Why it matters**: String length distributions help design database schemas. Top values reveal categorical structure.

#### Numeric Field Statistics (`test_tabular.py::TestCalculateNumericStats`)
Tests numeric analysis:

- **Central tendency**: Mean, median
- **Spread**: Standard deviation, quartiles (Q1, Q3)
- **Range**: Min and max values
- **Null handling**: Correctly excludes NaN values from calculations

**Why it matters**: Numeric summaries reveal data distributions and potential outliers.

#### File Utilities (`test_tabular.py::TestFileUtilities`)
Tests file handling capabilities:

- **Encoding detection**: Identifies UTF-8, ASCII, and other encodings
- **Delimiter inference**: Detects tab, comma, pipe, and semicolon delimiters
- **Comment handling**: Skips comment lines starting with `#`
- **Bad line handling**: Warns about malformed rows instead of failing

**Why it matters**: Real-world data files have inconsistent formatting. Robust parsing prevents analysis failures.

#### File Discovery (`test_file_discovery.py::TestDiscoverFiles`)
Tests the file discovery system:

- **Multiple file types**: Finds CSV, TSV, TXT, JSON, XML files
- **Gzipped files**: Correctly identifies .txt.gz, .csv.gz by looking at the stem
- **Hidden files**: Skips files starting with `.`
- **Manifest filtering**: Excludes manifest.json files from analysis
- **Recursive search**: Finds files in nested directories
- **Multi-source**: Correctly labels files by source directory

**Why it matters**: Automated file discovery enables "analyze all sources" functionality without manual file lists.

## Analysis Output Validation

### Expected Output Structure

Phase 2 (Tabular Analysis) creates:
```
output/preliminary-analysis/sources/<filename>/
```

Output files (to be implemented in Phase 5):
- JSON profile with complete field statistics
- Markdown report for human review
- CSV data dictionary
- Visualizations (null percentages, cardinality, distributions)

### Validation Checks

When running analyses, verify:
1. **No errors**: Analysis completes without exceptions
2. **Output directories created**: One per analyzed file
3. **Encoding handled**: Files with special characters load correctly
4. **Comment lines skipped**: Files with `#` headers parse correctly
5. **Bad lines logged**: Malformed rows generate warnings, not crashes

## Phase 3: Semi-Structured Data Tests

### JSON and XML Parsing (`test_semistructured.py`)

Tests the semi-structured data analysis engine for JSON and XML files.

#### JSON Parsing Tests (`TestParseJSON`)
- **Simple JSON**: Parses basic key-value objects
- **Nested JSON**: Handles deeply nested structures
- **Array handling**: Correctly processes arrays and lists

**Why it matters**: Clinical genomics data often uses JSON for complex actionability reports (ClinGen) and API responses.

#### XML Parsing Tests (`TestParseXML`)
- **Basic XML**: Parses simple XML documents
- **Namespace handling**: Strips namespace prefixes for cleaner paths
- **Element extraction**: Correctly extracts tags and text content

**Why it matters**: TCGA biospecimen and clinical data are distributed as XML. Robust parsing is essential for analysis.

#### Path Extraction Tests
- **JSON paths** (`TestExtractJSONPaths`): Extracts dot-notation paths (e.g., `person.address.city`)
- **XML paths** (`TestExtractXMLPaths`): Extracts XPath-like paths (e.g., `root/person/name`)
- **Array notation**: Correctly represents arrays with `[]` notation

**Why it matters**: Path extraction enables automated discovery of all fields in complex nested structures.

#### Structure Analysis Tests
- **Depth calculation** (`TestCalculateDepth`): Computes maximum nesting depth for both JSON and XML
- **Node counting** (`TestCountNodes`): Counts total elements in structures
- **Schema inference** (`TestInferJSONSchema`): Infers JSON Schema-like type descriptions

**Why it matters**: Understanding structure complexity helps design appropriate storage and query strategies.

#### End-to-End File Analysis (`TestAnalyzeSemistructuredFile`)
- **JSON file analysis**: Complete analysis workflow for `.json` files
- **XML file analysis**: Complete analysis workflow for `.xml` files
- **Error handling**: Gracefully handles unsupported file types

**Why it matters**: Ensures the full analysis pipeline works with real files.

## Phase 4: Cross-Source Analysis Tests

### Entity Extraction (`test_cross_source.py`)

Tests extraction of biomedical entities from analysis data.

#### Gene Extraction Tests (`TestExtractGenes`)
- **HGNC ID extraction**: Identifies fields containing HGNC gene identifiers
- **Gene symbol extraction**: Extracts gene symbols (uppercase, alphanumeric)
- **Empty data handling**: Returns empty sets when no gene data present

**Why it matters**: Gene extraction enables cross-source gene coverage comparison and harmonization.

#### Disease Extraction Tests (`TestExtractDiseases`)
- **MONDO ID extraction**: Identifies disease ontology identifiers
- **OMIM ID extraction**: Extracts OMIM disease identifiers
- **Disease name extraction**: Captures disease name strings

**Why it matters**: Disease extraction enables cross-source disease coverage analysis.

#### Variant Extraction Tests (`TestExtractVariants`)
- **dbSNP ID extraction**: Identifies rs IDs from variant fields
- **ClinVar ID extraction**: Extracts VCV identifiers
- **HGVS extraction**: Captures HGVS variant notation

**Why it matters**: Variant extraction enables variant-level cross-source comparison.

### Overlap Analysis (`TestCalculateOverlap`)
- **Two-set overlap**: Calculates intersection, union, Jaccard similarity
- **No intersection case**: Handles completely disjoint sets
- **Complete intersection**: Handles identical sets
- **Overlap percentages**: Computes percentage overlap from each source's perspective

**Why it matters**: Overlap analysis quantifies data redundancy and complementarity across sources.

### Field Mapping (`TestFieldNameSimilarity`, `TestSuggestFieldMappings`)
- **Name similarity**: Fuzzy matching with normalization (case, underscores, dashes)
- **Threshold filtering**: Only suggests mappings above similarity threshold
- **Type compatibility**: Checks data type agreement
- **Confidence scoring**: High/medium/low based on similarity + type match

**Why it matters**: Automated field mapping suggestions accelerate harmonization schema design.

### Identifier Coverage (`TestAnalyzeIdentifierCoverage`)
- **Coverage matrix**: Tracks which sources have which identifier types
- **Multi-source comparison**: Shows HGNC/MONDO/OMIM/dbSNP/ClinVar coverage

**Why it matters**: Identifier coverage informs which sources can be linked on which identifiers.

### End-to-End Cross-Source Analysis (`TestAnalyzeCrossSource`)
- **Complete workflow**: Tests full cross-source analysis pipeline
- **Gene overlap**: Validates entity overlap calculation
- **Field mappings**: Confirms mapping suggestions generated
- **Identifier coverage**: Verifies coverage matrix creation

**Why it matters**: Ensures all cross-source components work together correctly.

## Phase 5 Testing (To Be Implemented)

### Phase 5: Reporting & Visualization
- JSON report generation
- Markdown report formatting
- Data dictionary export
- Matplotlib visualization rendering

## Continuous Testing

Currently, tests are run manually with `make test-analysis`. Future enhancements may include:

- **Pre-commit hooks**: Run tests before commits
- **CI/CD integration**: Automated testing on GitHub Actions
- **Coverage reports**: Track test coverage percentage
- **Performance benchmarks**: Ensure analysis speed doesn't degrade

## Test Development Guidelines

When adding new functionality:

1. **Write tests first** (TDD approach) or alongside implementation
2. **Test edge cases**: Empty data, all nulls, extreme values
3. **Use realistic data**: Sample from actual data sources when possible
4. **Assert specific values**: Not just "doesn't crash"
5. **Document why**: Explain what the test validates and why it matters

## Known Limitations

Current test suite does not cover:
- Large file handling (>1GB files tested manually)
- Parallel processing correctness
- Memory usage under load
- Cross-platform compatibility (only tested on macOS)

These may be addressed in future test iterations as needed.

---

*Documentation created: 2025-10-04*
*Last updated: 2025-10-04*
