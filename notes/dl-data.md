# Data Download Action Plan

This document tracks the tasks required to download data from each source, distinguishing between tasks that can be automated vs. those requiring human intervention.

**Legend:**
- ✅ Can download without human intervention
- ⚠️ Partial automation possible (some data accessible, some requires auth)
- ❌ Requires human setup/authorization
- `@human` = Human action required (see dl-data-human-tasks.md for details)

---

## 1. cBioPortal

**Download Status:** ✅ Fully automated (no human intervention needed)

**Rationale:** Public API, no authentication required, open source data

### Download Tasks

#### Data Acquisition
- [x] Identify target studies/datasets from cBioPortal
- [x] Query API for available studies list
- [x] Select datasets relevant to RWE analysis (mutation, clinical, CNA, expression)
- [x] Download mutation data (MAF format) via API
- [x] Download clinical data via API
- [x] Download copy number data via API
- [x] Download gene expression data via API
- [x] Verify downloaded files integrity
- [x] Document data provenance (study IDs, dates, versions)

#### Data Organization
- [x] Create directory structure: `data/raw/cbioportal/`
- [x] Save study metadata (study IDs, cancer types, sample counts)
- [x] Generate download manifest/log
- [x] Create README documenting downloaded datasets

**Estimated Effort:** 2-4 hours (scripting + execution)

**Notes:**
- No authentication needed
- Can start immediately
- Rate limits may apply (handle gracefully in script)

---

## 2. ClinGen

**Download Status:** ✅ Fully automated (no human intervention needed)

**Rationale:** CC0 public domain, FTP and HTTPS downloads available, no authentication

### Download Tasks

#### Data Acquisition
- [x] Download Gene-Disease Validity data (CSV)
- [x] Download Dosage Sensitivity data (TSV) - GRCh37
- [x] Download Dosage Sensitivity data (TSV) - GRCh38
- [x] Download Dosage Sensitivity regions (BED) - GRCh37
- [x] Download Dosage Sensitivity regions (BED) - GRCh38
- [x] Download Clinical Actionability data (JSON/TSV)
- [x] Download Variant Pathogenicity data (CSV)
- [x] Verify file checksums/integrity
- [x] Document data provenance (download date, file versions)

#### Data Organization
- [x] Create directory structure: `data/raw/clingen/`
- [x] Organize by data type (gene-validity, dosage, actionability, variants)
- [x] Generate download manifest
- [x] Create README with file descriptions

**Estimated Effort:** 1-2 hours

**Notes:**
- Direct HTTPS/FTP downloads
- No rate limits
- Files updated monthly/nightly

---

## 3. ClinVar

**Download Status:** ✅ Fully automated (no human intervention needed)

**Rationale:** Public domain, FTP access, E-utilities API public, no authentication

### Download Tasks

#### Data Acquisition - Monthly Release Files
- [x] Download variant_summary.txt (latest monthly release)
- [x] Download VCF file - GRCh37
- [x] Download VCF file - GRCh38
- [x] Download XML files - VCV format (variant-level)
- [x] Download XML files - RCV format (variant-condition-level)
- [x] Download var_citations.txt (variant-publication links)
- [x] Download cross_references.txt
- [x] Download submission_summary.txt

#### Data Acquisition - Via E-utilities (Optional)
- [ ] Query specific gene sets via esearch
- [ ] Fetch variant details via efetch
- [ ] Get variant summaries via esummary

#### Data Organization
- [x] Create directory structure: `data/raw/clinvar/`
- [x] Organize by genome build (GRCh37, GRCh38)
- [x] Organize by file type (VCF, XML, TSV)
- [x] Track monthly release version
- [x] Generate download manifest
- [x] Create README

**Estimated Effort:** 2-3 hours

**Notes:**
- FTP site: ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/
- Monthly releases on first Thursday
- Large files (multi-GB XML)

---

## 4. COSMIC

**Download Status:** ❌ Requires human setup before download

**Rationale:** Requires account registration and authentication (academic or commercial license)

### Prerequisites (Human Tasks)
- [ ] @human Determine if academic or commercial use
- [ ] @human Register for COSMIC account with institutional email
- [ ] @human Verify email and complete registration
- [ ] @human (If commercial) Complete license agreement and payment
- [ ] @human Test login at cancer.sanger.ac.uk/cosmic
- [ ] @human Provide credentials for automated downloads

### Download Tasks (After Human Setup)
- [ ] Set up authenticated download script (using provided credentials)
- [ ] Download CosmicCodingMuts VCF - GRCh37
- [ ] Download CosmicCodingMuts VCF - GRCh38
- [ ] Download CosmicNonCodingVariants VCF - GRCh37
- [ ] Download CosmicNonCodingVariants VCF - GRCh38
- [ ] Download Cancer Gene Census TSV
- [ ] Download Cancer Mutation Census files
- [ ] Download Actionability data
- [ ] Download Cell Lines data
- [ ] Download Resistance Mutations
- [ ] Verify file integrity
- [ ] Document data provenance (version, release date)

### Data Organization
- [ ] Create directory structure: `data/raw/cosmic/`
- [ ] Organize by data type (coding, noncoding, census, actionability)
- [ ] Organize by genome build
- [ ] Store credentials securely (not in git)
- [ ] Generate download manifest
- [ ] Create README

**Estimated Effort:**
- Human setup: 10-30 min (academic) or 1-4 weeks (commercial)
- Download automation: 2-3 hours

**Dependencies:**
1. Human completes registration (academic: ~30 min, commercial: 1-4 weeks)
2. Then automated downloads can proceed

---

## 5. GenCC

**Download Status:** ✅ Fully automated (no human intervention needed)

**Rationale:** CC0 public domain, direct file downloads, no authentication

### Download Tasks

#### Data Acquisition
- [x] Download complete GenCC dataset - TSV format
- [x] Download complete GenCC dataset - CSV format (backup)
- [x] Download complete GenCC dataset - XLSX format (for manual review)
- [x] Verify file integrity
- [x] Document data provenance (download date)

#### Data Organization
- [x] Create directory structure: `data/raw/gencc/`
- [x] Save all format versions for compatibility
- [x] Generate download manifest
- [x] Create README

**Estimated Effort:** 30 minutes

**Notes:**
- Direct downloads from search.thegencc.org/download
- Single file, regularly updated
- Very straightforward

---

## 6. OncoKB

**Download Status:** ❌ Requires human setup before download

**Rationale:** Requires account registration and API token (academic or commercial license)

### Prerequisites (Human Tasks)
- [ ] @human Determine if academic or commercial use
- [ ] @human Register for OncoKB account with institutional email
- [ ] @human Verify email address
- [ ] @human (If commercial) Complete license agreement and payment
- [ ] @human Generate API token from OncoKB account
- [ ] @human Provide API token for automated scripts

### Download Tasks (After Human Setup)
- [ ] Set up API authentication with provided token
- [ ] Test API connection
- [ ] Query all oncogenic genes list
- [ ] Query all actionable genes list
- [ ] Download Cancer Gene annotations via API
- [ ] Download therapeutic levels of evidence via API
- [ ] Download mutation effect annotations
- [ ] (Optional) Request data dump from OncoKB team
- [ ] Verify data completeness
- [ ] Document data provenance (API version, date)

### Data Organization
- [ ] Create directory structure: `data/raw/oncokb/`
- [ ] Organize by data type (genes, mutations, therapies)
- [ ] Store API token securely (environment variable, not in git)
- [ ] Generate download manifest
- [ ] Create README

**Estimated Effort:**
- Human setup: 15-30 min (academic) or 1-4 weeks (commercial)
- Download automation: 2-4 hours

**Dependencies:**
1. Human completes registration and obtains API token
2. Then automated API queries can proceed

**Notes:**
- May need to contact OncoKB for bulk data dump
- API may have rate limits

---

## 7. TCGA (via GDC)

**Download Status:** ⚠️ Partial automation (Open Access: ✅ / Controlled Access: ❌)

**Rationale:** Open access data freely available; controlled access requires dbGaP authorization

### Phase 1: Open Access Data (No Human Setup)

#### Prerequisites
- [ ] Install GDC Data Transfer Tool
- [ ] Test gdc-client installation

#### Data Acquisition - Clinical & Biospecimen
- [ ] Identify target TCGA projects (e.g., TCGA-BRCA, TCGA-LUAD)
- [ ] Download clinical data files (TSV/JSON) for selected projects
- [ ] Download biospecimen data files
- [ ] Verify file integrity

#### Data Acquisition - Molecular Data (Open Access)
- [ ] Download somatic mutation data (MAF files)
- [ ] Download gene expression data (TSV - TPM/FPKM)
- [ ] Download miRNA expression data
- [ ] Download copy number segmentation files
- [ ] Download DNA methylation data (processed beta values)
- [ ] Download protein expression data (RPPA)

#### Data Organization
- [ ] Create directory structure: `data/raw/tcga/open-access/`
- [ ] Organize by project (TCGA-BRCA, TCGA-LUAD, etc.)
- [ ] Organize by data type (clinical, mutations, expression, etc.)
- [ ] Generate download manifests
- [ ] Create README with project descriptions

**Estimated Effort:** 3-6 hours

---

### Phase 2: Controlled Access Data (Requires Human Setup)

**Only proceed if raw sequencing data (BAM/FASTQ) or germline variants needed**

#### Prerequisites (Human Tasks)
- [ ] @human Create NIH eRA Commons account (via institutional SO)
- [ ] @human Submit dbGaP Data Access Request for TCGA (phs000178)
- [ ] @human Provide research use statement
- [ ] @human Obtain institutional certification/signature
- [ ] @human Wait for DAC approval (5-10 business days)
- [ ] @human Download GDC authentication token after approval
- [ ] @human Provide authentication token for automated downloads

#### Data Acquisition - Controlled (After Human Approval)
- [ ] Set up authenticated downloads with provided token
- [ ] Test authenticated access
- [ ] Download aligned BAM files (WXS)
- [ ] Download aligned BAM files (RNA-Seq)
- [ ] Download aligned BAM files (WGS) - if needed
- [ ] Download germline VCF files
- [ ] Download raw FASTQ files - if needed
- [ ] Verify file integrity (MD5 checksums)
- [ ] Document data provenance

#### Data Organization
- [ ] Create directory structure: `data/raw/tcga/controlled-access/`
- [ ] Organize by project and data type
- [ ] Store authentication token securely
- [ ] Generate download manifests
- [ ] Create README with access documentation

**Estimated Effort:**
- Human setup: 2-6 weeks (dbGaP authorization)
- Download automation: 4-8 hours (large files)

**Dependencies:**
1. Determine if controlled access data is actually needed
2. If yes: Human completes 2-6 week dbGaP authorization process
3. Then automated downloads can proceed with token

**Notes:**
- Controlled access may not be necessary for RWE analysis
- Open access mutation/expression data may be sufficient
- Decision point: Assess if raw sequencing data is required

---

## Download Priority & Sequencing

### Immediate Start (No Blockers)
Can begin immediately without human intervention:

1. **GenCC** (quickest, 30 min)
2. **ClinGen** (1-2 hours)
3. **ClinVar** (2-3 hours)
4. **cBioPortal** (2-4 hours)
5. **TCGA - Open Access** (3-6 hours)

**Total for immediate downloads: ~9-15 hours of work**

---

### Requires Human Setup First

Must wait for human to complete registration/authorization:

6. **OncoKB**
   - **Human task**: Register, get API token (15-30 min for academic)
   - **Then**: Automated download (2-4 hours)
   - **Total timeline**: Same day

7. **COSMIC**
   - **Human task**: Register with institutional email (10-30 min for academic)
   - **Then**: Automated download (2-3 hours)
   - **Total timeline**: Same day for academic; 1-4 weeks for commercial

8. **TCGA - Controlled Access** (OPTIONAL)
   - **Human task**: dbGaP authorization (2-6 weeks)
   - **Then**: Automated download (4-8 hours)
   - **Total timeline**: 2-6 weeks
   - **Decision**: Only pursue if raw sequencing data actually needed

---

## Recommended Execution Order

### Week 1 - Immediate Downloads
**Day 1-2:**
- Start all "no human intervention" downloads in parallel
- GenCC, ClinGen, ClinVar, cBioPortal, TCGA open access
- Set up automated scripts for each
- Monitor and verify downloads

**Day 3:**
- Human: Register for OncoKB (15-30 min)
- Human: Register for COSMIC (10-30 min)

**Day 4-5:**
- Automated: Download OncoKB data via API
- Automated: Download COSMIC data via authenticated HTTPS
- Verify all downloads complete

### Week 2-6 (Optional) - Controlled Access
**Only if raw sequencing/germline data needed:**
- Human: Initiate dbGaP authorization process
- Human: Submit all required documentation
- Wait for DAC approval
- Upon approval: Automated download of controlled data

---

## Data Storage Estimates

Estimated disk space requirements:

| Data Source | Size Estimate | Notes |
|-------------|---------------|-------|
| cBioPortal | 1-5 GB | Depends on number of studies |
| ClinGen | 50-200 MB | All datasets |
| ClinVar | 5-20 GB | Full XML releases are large |
| COSMIC | 2-10 GB | Multiple file types |
| GenCC | 5-20 MB | Single file |
| OncoKB | 100-500 MB | API responses |
| TCGA (Open) | 10-50 GB | Per cancer type |
| TCGA (Controlled) | 100GB-10TB | BAM files are huge |

**Total (excluding TCGA controlled):** ~20-90 GB
**Total (including TCGA controlled):** 120GB-10TB+

**Recommendation:** Start with open access data only; controlled access only if truly needed

---

## Success Criteria

For each data source, download is complete when:
- [ ] All planned files downloaded successfully
- [ ] File integrity verified (checksums, file sizes)
- [ ] Data organized in logical directory structure
- [ ] Download manifest/log created
- [ ] README documentation created
- [ ] Data provenance recorded (versions, dates, sources)
- [ ] Sample data spot-checked for validity

---

## Next Steps After Downloads

Once downloads complete:
1. **Data validation**: Verify file formats, check for completeness
2. **Data exploration**: Sample records, understand structure
3. **Schema mapping**: Map fields across sources for harmonization
4. **Integration planning**: Design unified data model
5. **Pipeline development**: Build preprocessing and harmonization workflows

---

*Last Updated: 2025*
*See dl-data-human-tasks.md for detailed human task instructions*
