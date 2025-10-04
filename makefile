PYTHON ?= python3
CBIOPORTAL_SCRIPT := db/sources/by_source/cbioportal/download.py
CBIOPORTAL_STUDIES := brca_tcga_pan_can_atlas_2018 luad_tcga_pan_can_atlas_2018
CLINGEN_SCRIPT := db/sources/by_source/clingen/download.py
CLINVAR_SCRIPT := db/sources/by_source/clinvar/download.py
TCGA_SCRIPT := db/sources/by_source/tcga/download.py
GDC_CLIENT := scripts/tools/gdc-client
ANALYSIS_CLI := analysis/cli.py

.PHONY: download-sources download-cbioportal download-clingen download-clinvar download-tcga install-gdc-client
.PHONY: analyze-phase1 analyze-phase2 analyze-phase3 analyze-phase4 analyze-phase5
.PHONY: preliminary-analysis analysis
.PHONY: test test-analysis

download-sources: download-cbioportal download-clingen download-clinvar download-tcga

# Download cBioPortal studies defined in CBIOPORTAL_STUDIES
download-cbioportal: $(CBIOPORTAL_STUDIES:%=data/raw/cbioportal/metadata/%/.download-complete)

# Sentinel files for cBioPortal studies
data/raw/cbioportal/metadata/%/.download-complete: $(CBIOPORTAL_SCRIPT)
	@echo "Fetching cBioPortal study $*"
	$(PYTHON) $(CBIOPORTAL_SCRIPT) --study $* --base-dir data/raw/cbioportal

download-clingen: $(CLINGEN_SCRIPT)
	@echo "Fetching ClinGen datasets"
	$(PYTHON) $(CLINGEN_SCRIPT) --base-dir data/raw/clingen

download-clinvar: $(CLINVAR_SCRIPT)
	@echo "Fetching ClinVar datasets"
	$(PYTHON) $(CLINVAR_SCRIPT) --base-dir data/raw/clinvar

# Install GDC Data Transfer Tool
install-gdc-client:
	@if [ ! -f $(GDC_CLIENT) ]; then \
		echo "Installing GDC Data Transfer Tool..."; \
		mkdir -p scripts/tools; \
		curl -LO https://gdc.cancer.gov/files/public/file/gdc-client_v1.6.1_OSX_x64.zip; \
		unzip -q gdc-client_v1.6.1_OSX_x64.zip; \
		mv gdc-client $(GDC_CLIENT); \
		rm gdc-client_v1.6.1_OSX_x64.zip; \
		echo "GDC client installed at $(GDC_CLIENT)"; \
	else \
		echo "GDC client already installed at $(GDC_CLIENT)"; \
	fi

download-tcga: $(GDC_CLIENT) $(TCGA_SCRIPT)
	@echo "Fetching TCGA open-access datasets"
	$(PYTHON) $(TCGA_SCRIPT) --base-dir data/raw/tcga

# ================================================================================
# Preliminary Data Analysis
# ================================================================================

# Phase 1: File discovery
analyze-phase1:
	@echo "📁 Phase 1: File Discovery"
	$(PYTHON) $(ANALYSIS_CLI) all --output-dir output/preliminary-analysis --fast

# Phase 2: Tabular data analysis
analyze-phase2:
	@echo "📊 Phase 2: Tabular Data Analysis"
	@echo "Analyzing GenCC..."
	$(PYTHON) $(ANALYSIS_CLI) file data/sources/gencc/gencc-submissions.tsv
	@echo "Analyzing ClinGen gene-validity..."
	$(PYTHON) $(ANALYSIS_CLI) file data/sources/clingen/gene-validity/gene-validity.csv
	@echo "Analyzing ClinGen dosage sensitivity..."
	$(PYTHON) $(ANALYSIS_CLI) file data/sources/clingen/dosage-sensitivity/dosage-sensitivity-grch38.tsv

# Phase 3: Semi-structured data (JSON/XML)
analyze-phase3:
	@echo "🌲 Phase 3: Semi-Structured Data Analysis"
	@echo "Analyzing ClinGen actionability JSON..."
	$(PYTHON) $(ANALYSIS_CLI) file data/sources/clingen/actionability/clinical-actionability-adult-flat.json
	@echo "Analyzing sample TCGA XML..."
	@if [ -f data/sources/tcga/open-access/biospecimen/TCGA-BRCA/aa06e869-8576-4428-b23e-1de81d4ebe2b/nationwidechildrens.org_biospecimen.TCGA-B6-A409.xml ]; then \
		$(PYTHON) $(ANALYSIS_CLI) file data/sources/tcga/open-access/biospecimen/TCGA-BRCA/aa06e869-8576-4428-b23e-1de81d4ebe2b/nationwidechildrens.org_biospecimen.TCGA-B6-A409.xml; \
	else \
		echo "TCGA XML files not available (still downloading)"; \
	fi

# Phase 4: Cross-source analysis
analyze-phase4:
	@echo "🔗 Phase 4: Cross-Source Analysis"
	@echo "Cross-source analysis requires multiple source analyses to compare."
	@echo "Run 'make analyze-phase2' and 'make analyze-phase3' first to generate source data."
	@echo "Phase 4 will be integrated in Phase 5 reporting."

# Phase 5: Reporting and visualization
analyze-phase5:
	@echo "📈 Phase 5: Reporting and Visualization"
	@echo "Generating aggregated TSV reports..."
	$(PYTHON) $(ANALYSIS_CLI) generate-reports

# Run all analysis phases
preliminary-analysis: analyze-phase1 analyze-phase2 analyze-phase3 analyze-phase4 analyze-phase5
	@echo "✅ Complete preliminary analysis finished"

# Alias for preliminary-analysis
analysis: preliminary-analysis

# ================================================================================
# Testing
# ================================================================================

# Run analysis tests
test-analysis:
	@echo "🧪 Running analysis tests..."
	$(PYTHON) -m pytest analysis/tests/ -v

# Run all tests
test: test-analysis
	@echo "✅ All tests complete"
