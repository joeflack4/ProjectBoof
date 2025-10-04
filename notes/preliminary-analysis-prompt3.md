# Preliminary Analysis - Agent Handoff Prompt (Session 3)

## Your Task

Complete the preliminary data analysis system for HarmonaQuery, following the iteration routine documented in `notes/routines/iteration.md`.

## Context - What You're Picking Up

The previous agent session implemented the foundation for analyzing genomic/clinical data sources. You're continuing from Phase 2.5 onwards.

### What's Already Done

1. **Infrastructure**:
   - CLI framework at `analysis/cli.py` (fully functional)
   - Tabular analyzer at `analysis/core/tabular.py` (450+ lines, complete)
   - File discovery at `analysis/core/file_discovery.py`
   - Directory structure: `analysis/{core,utils,reports,visualizations,tests}`
   - Output structure: `output/preliminary-analysis/{sources,cross-source,reports}`

2. **Makefile Commands** (in root `makefile`):
   - `make analyze-phase1` through `make analyze-phase5` (phases 3-5 are placeholders)
   - `make preliminary-analysis` (runs all phases)
   - `make analysis` (alias)
   - `make test-analysis` and `make test` (defined but tests not written yet)

3. **Tested & Working**:
   - Successfully analyzed GenCC sample data: `python3 analysis/cli.py file data/sources/gencc/gencc-submissions.tsv --sample 1000`
   - Dependencies installed: click, pandas, numpy, chardet, pytest

### What's NOT Done

- Tests haven't been written yet
- Documentation (QC section in README, docs/qc.md) not created
- Phases 3-5 implementation (semi-structured, cross-source, reporting)
- Full analysis hasn't been run on all sources

## Instructions

### Step 1: Read These Files First

1. `notes/preliminary-analysis.md` - Complete specification with checklist (START HERE)
2. `notes/preliminary-analysis-questions.md` - Design decisions already made
3. `notes/routines/iteration.md` - **Critical**: Follow this routine for each minor section
4. `notes/harmony-strats.md` - Context on why this analysis matters
5. `makefile` - See what's already wired up

### Step 2: Complete Phase 2.5 (Makefile, Testing & Documentation)

Following the checklist in `notes/preliminary-analysis.md` Phase 2.5:

#### 2.5.1: Makefile Commands (Already Done ✅)
- [x] Makefile commands added
- You can skip this subsection

#### 2.5.2: Testing Infrastructure

Create `analysis/tests/` with:

1. **`test_tabular.py`**:
   - Test `infer_data_type()` with sample data (strings, integers, floats, dates, booleans)
   - Test `calculate_basic_stats()` with known inputs
   - Test `detect_identifier_pattern()` with HGNC, MONDO, dbSNP samples
   - Test `analyze_tabular_file()` end-to-end with a small test CSV

2. **`test_file_discovery.py`**:
   - Test `discover_files()` finds expected file types
   - Test it correctly identifies source names
   - Test it filters by extension

3. **Verify tests pass**: Run `make test-analysis`

4. **Verify analyses run**: Run `make analyze-phase2` and check that:
   - No errors occur
   - Output files created in `output/preliminary-analysis/sources/`
   - Files contain expected structure (even if incomplete)

#### 2.5.3: Documentation

1. **Update `README.md`**:
   - Add "## QC" section after the existing content
   - 1-3 sentence summary: "Analysis and data quality tests ensure reliability. Tests cover data type inference, field statistics calculation, and end-to-end analysis workflows. See [docs/qc.md](docs/qc.md) for details."

2. **Create `docs/qc.md`**:
   ```markdown
   # Quality Control & Testing

   ## Overview
   (Explain testing philosophy and coverage)

   ## Running Tests
   `make test` or `make test-analysis`

   ## Test Coverage

   ### Analysis Tests
   - Data type inference
   - Field statistics
   - File discovery
   - (List what's tested and why)

   ## Analysis Output Validation
   (Describe expected output format and structure)

   ## Continuous Testing
   (If applicable, CI/CD info)
   ```

#### 2.5.4: Close Out Phase 2.5

**Follow `notes/routines/iteration.md` exactly**:

1. ✅ Ensure all tests passing or skipped (document skips in `notes/preliminary-analysis-skipped-tests.md`)
2. ✅ Check off completed checkboxes in `notes/preliminary-analysis.md` Phase 2.5
3. ✅ Add `@skipped-until-TAG` for incomplete tasks, explain tags in document
4. ✅ Add questions to `notes/preliminary-analysis-questions.md` if needed
5. ✅ Mark `@dev` for anything requiring user attention
6. ✅ Ensure README.md updated

### Step 3: Phase 3 - Semi-Structured Engine

Implement `analysis/core/semistructured.py`:

**Functions needed**:
- `parse_xml(filepath)` - Parse XML, extract paths and values
- `parse_json(filepath)` - Parse JSON, extract paths and values
- `infer_schema(data)` - Infer JSON Schema or XSD-like structure
- `analyze_structure(data)` - Max depth, node count, unique paths
- `analyze_semistructured_file(filepath)` - Main entry point

**Test files**:
- ClinGen actionability: `data/sources/clingen/actionability/*.json`
- TCGA clinical XML: `data/sources/tcga/open-access/clinical/TCGA-BRCA/*.xml`

**Testing**: Write `analysis/tests/test_semistructured.py`

**Makefile**: Update `analyze-phase3` to actually run (remove "Not yet implemented")

**Docs**: Update `docs/qc.md` with Phase 3 testing details

**Close out Phase 3** following the iteration routine.

### Step 4: Phase 4 - Cross-Source Analysis

Implement `analysis/core/cross_source.py`:

**Functions needed**:
- `extract_genes(source_analysis)` - Extract unique gene identifiers
- `extract_diseases(source_analysis)` - Extract disease identifiers
- `extract_variants(source_analysis)` - Extract variant identifiers
- `calculate_overlap(entity_sets)` - Venn diagram data
- `suggest_field_mappings(sources)` - Fuzzy match field names, check value overlap
- `analyze_identifiers(sources)` - HGNC/MONDO/dbSNP coverage matrix

**Output**: JSON files in `output/preliminary-analysis/cross-source/`

**Testing**: `analysis/tests/test_cross_source.py`

**Makefile**: Update `analyze-phase4`

**Docs**: Update `docs/qc.md`

**Close out Phase 4** following the iteration routine.

### Step 5: Phase 5 - Reporting & Visualization

Implement:

1. **`analysis/reports/json_report.py`** - Export analysis as structured JSON
2. **`analysis/reports/markdown_report.py`** - Generate human-readable markdown
3. **`analysis/reports/data_dictionary.py`** - CSV with all fields + statistics
4. **`analysis/visualizations/plots.py`** - Matplotlib charts:
   - Null percentage bar charts
   - Field cardinality distributions
   - Numeric field histograms
   - Entity overlap Venn diagrams

**Testing**: `analysis/tests/test_reports.py`, `test_visualizations.py`

**Makefile**: Update `analyze-phase5`

**Docs**: Update `docs/qc.md`

**Close out Phase 5** following the iteration routine.

### Step 6: Final Integration

1. Run `make preliminary-analysis` end-to-end
2. Verify all outputs generated correctly
3. Run `make test` - all tests should pass
4. Update `notes/preliminary-analysis.md` with final status
5. Create summary in `notes/preliminary-analysis-session3-summary.md`

## Important Constraints

- **Follow iteration routine strictly**: Complete each minor section (e.g., 2.5, 3.0, 4.0) before moving on
- **Test everything**: Every phase needs tests that actually run
- **Document as you go**: Don't batch documentation at the end
- **Check off tasks**: Keep `notes/preliminary-analysis.md` up to date
- **Ask questions**: Use `notes/preliminary-analysis-questions.md` for anything unclear

## Success Criteria

When you're done:
- ✅ All Phase 2.5-5 checkboxes complete or annotated with `@skipped-until-TAG`
- ✅ `make test` passes (or skips documented)
- ✅ `make preliminary-analysis` runs without errors
- ✅ Output files in expected locations with correct structure
- ✅ README.md has QC section
- ✅ `docs/qc.md` exists and documents all testing
- ✅ Can answer: "Which fields map across sources?" and "What's the data quality?"

## Key Files Reference

**Implementation**:
- `analysis/cli.py` - CLI commands
- `analysis/core/tabular.py` - Tabular analyzer (DONE)
- `analysis/core/semistructured.py` - JSON/XML analyzer (TO DO)
- `analysis/core/cross_source.py` - Cross-source analysis (TO DO)
- `analysis/reports/*.py` - Report generators (TO DO)
- `analysis/visualizations/plots.py` - Visualizations (TO DO)

**Testing**:
- `analysis/tests/test_*.py` - All test files (TO DO)

**Documentation**:
- `notes/preliminary-analysis.md` - Task checklist (KEEP UPDATED)
- `notes/preliminary-analysis-questions.md` - Q&A (ADD TO IF NEEDED)
- `notes/preliminary-analysis-skipped-tests.md` - Skipped test documentation (CREATE IF NEEDED)
- `docs/qc.md` - QC documentation (TO CREATE)
- `README.md` - Add QC section (TO UPDATE)

**Execution**:
- `makefile` - All commands defined

## Notes from Previous Agent

- GenCC analysis worked perfectly with 1000-row sample
- The tabular analyzer is robust and handles encoding detection, delimiter inference, and type inference well
- Pattern detection successfully identifies HGNC, MONDO, dbSNP, and HGVS identifiers
- pytest and all dependencies are installed
- Background TCGA downloads still running (check status: d2e514)

## Final Advice

Start by reading the iteration routine carefully. It's your guide for making steady progress without getting blocked. For each subsection, complete the 6 steps (tests pass, checkboxes updated, tags explained, questions documented, @dev flags, README updated) before moving to the next.

Good luck! 🚀
