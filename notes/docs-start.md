# Data Source Documentation Research - Planning

## Objective
Research and document 7 genomic/clinical data sources for RWE analysis and virtual cohort aggregation. Each data source needs comprehensive documentation covering data types, acquisition methods, costs, and structure.

## Output Structure
- Individual files: `docs/data-sources/SOURCE.md` (e.g., `clingen.md`, `clinvar.md`)
- Master document: `docs/data-sources.md` (overview/index of all sources)

## Research Approach
For each data source, I will:
1. Research the official website and documentation
2. Identify what types of data are available (variants, clinical annotations, cancer genomics, etc.)
3. Determine access methods (Web API, FTP, file download, etc.)
4. Check for costs/subscriptions/registration requirements
5. Document the data structure at moderate detail level (major tables/files and key fields)
6. For APIs: Link to docs, list key endpoints, show example queries, create code snippets
7. Focus on current/latest version
8. Compile findings into structured markdown document

## Documentation Template per Source
Each source document will include:
- **Overview**: What kind of data, scope, purpose
- **Data Types**: Specific data categories available
- **Access Methods**:
  - Web API (if available): link to docs, key endpoints, example queries, code snippets
  - FTP/Download options
  - Other methods
- **Cost/Requirements**: Subscription, registration, licensing
- **Data Structure**: Moderate detail on files/tables and key fields
- **Version**: Current/latest documented

## Tasks per Data Source (done)
For each of the 7 sources, complete:
- Review official documentation and website
- Document data types and scope
- Document access methods (with full API details if applicable)
- Document cost/subscription requirements
- Document data structure (moderate detail: major files/tables and key fields)
- Create final documentation file in `docs/data-sources/`

## Research Priority Order
1. **cBioPortal** (priority)
2. ClinGen
3. ClinVar
4. COSMIC
5. GenCC
6. OncoKB
7. TCGA

## Data Sources Progress

### cBioPortal (PRIORITY)
- [x] Review official documentation
- [x] Document data types
- [x] Document access methods (full API details)
- [x] Document costs/requirements
- [x] Document data structure
- [x] Create `docs/data-sources/cbioportal.md`

### ClinGen
- [x] Review official documentation
- [x] Document data types
- [x] Document access methods (full API details)
- [x] Document costs/requirements
- [x] Document data structure
- [x] Create `docs/data-sources/clingen.md`

### ClinVar
- [x] Review official documentation
- [x] Document data types
- [x] Document access methods (full API details)
- [x] Document costs/requirements
- [x] Document data structure
- [x] Create `docs/data-sources/clinvar.md`

### COSMIC
- [x] Review official documentation
- [x] Document data types
- [x] Document access methods (full API details)
- [x] Document costs/requirements
- [x] Document data structure
- [x] Create `docs/data-sources/cosmic.md`

### GenCC
- [x] Review official documentation
- [x] Document data types
- [x] Document access methods (full API details)
- [x] Document costs/requirements
- [x] Document data structure
- [x] Create `docs/data-sources/gencc.md`

### OncoKB
- [x] Review official documentation
- [x] Document data types
- [x] Document access methods (full API details)
- [x] Document costs/requirements
- [x] Document data structure
- [x] Create `docs/data-sources/oncokb.md`

### TCGA
- [x] Review official documentation
- [x] Document data types
- [x] Document access methods (full API details)
- [x] Document costs/requirements
- [x] Document data structure
- [x] Create `docs/data-sources/tcga.md`

### Master Document
- [x] Create `docs/data-sources.md` with overview/index of all sources

## Notes
- Harmonization considerations deferred to Phase 2 (see `docs-start2.md`)
- Comprehensive field-level detail deferred to Phase 2
