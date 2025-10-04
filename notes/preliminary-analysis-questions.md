# Preliminary Analysis - Questions

## Questions for User

### 1. Large File Processing Strategy
**Question**: The ClinVar `variant_summary.txt.gz` file is >1GB uncompressed with millions of rows. Should we:
- A) Analyze the full file (may take 5-10 minutes, use significant memory)
- B) Sample the file (e.g., first 100K rows or random sample)
- C) Add a `--sample` flag to let you choose at runtime

**Recommendation**: Option C - analyze full file by default, but add `--sample N` flag for quick testing.

---

### 2. Visualization Formats
**Question**: What image format(s) for visualizations?
- PNG (good for reports, larger files)
- SVG (vector, scalable, smaller for simple plots)
- Both?

**Recommendation**: PNG for now (widely compatible), can add SVG later.

---

### 3. Statistical Thresholds
**Question**: What thresholds should we use for flagging data quality issues?
- Null percentage threshold for "high missingness": 50%? 75%?
- Cardinality threshold for "low" vs "medium": 10? 20?
- Outlier detection: 1.5×IQR (standard) or 3×IQR (conservative)?

**Recommendation**: Use standard thresholds (50% nulls, 10/1000 for cardinality, 1.5×IQR for outliers), but make configurable via config file.

---

### 4. Field Relationship Depth
**Question**: For detecting field relationships (correlations, dependencies), how deep should we go?
- Just pairwise correlations?
- Multi-field functional dependencies (e.g., gene_symbol + transcript → protein)?
- Complex patterns (e.g., conditional dependencies)?

**Recommendation**: Start with pairwise correlations and co-null analysis. Add functional dependencies if straightforward. Skip complex patterns for now.

---

### 5. Cross-Source Field Mapping Confidence
**Question**: For suggesting field mappings across sources, what matching strategies?
- Exact name match (case-insensitive)
- Fuzzy name match (e.g., "gene_symbol" → "hgnc_symbol", threshold 80%?)
- Value overlap (sample 100 values, check overlap >50%?)
- Manual mapping file (you provide known equivalences)?

**Recommendation**: Use all four: exact match (high confidence), fuzzy match >80% (medium), value overlap >50% (medium), plus manual override file.

---

### 6. XML/JSON Depth Limit
**Question**: Some TCGA clinical XML files are deeply nested. Should we:
- Analyze all levels (may be hundreds of paths)
- Limit to top N levels (e.g., 5 levels deep)
- Flatten to unique terminal nodes only

**Recommendation**: Analyze all levels but summarize by depth. Report depth distribution and top 50 most common paths.

---

### 7. Performance vs Completeness Trade-off
**Question**: For very large sources (ClinVar, TCGA), should we:
- Prioritize speed (sampling, approximations)
- Prioritize completeness (full scans, exact statistics)
- Make it configurable

**Recommendation**: Default to completeness for accuracy, add `--fast` flag for sampling-based quick analysis.

---

### 8. External API Calls
**Question**: Should the analysis make external API calls to validate identifiers (e.g., check if HGNC IDs are valid via HGNC API)?
- Yes, validate identifiers (more accurate, but slower and requires internet)
- No, just check format/patterns (faster, offline-capable)

**Recommendation**: No external calls for preliminary analysis (keep it fast and offline). Add separate validation command later if needed.

---

## Non-Blocking Decisions (Proceeding with Defaults)

The following I'm proceeding with defaults, but flagging for your awareness:

9. **Date Format Detection**: Will attempt common formats (YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY, ISO 8601). If ambiguous, will flag.

10. **Character Encoding**: Will use `chardet` to detect encoding. Default to UTF-8 if detection fails.

11. **Missing Value Representations**: Will treat as null: empty string, "NA", "N/A", "NULL", "None", "NaN", "-", ".", "?"

12. **Numeric Outlier Reporting**: Will report outliers but not filter them (data as-is). Flag extreme outliers separately.

13. **Report Verbosity**: Will generate detailed reports. Summary report will be concise, individual source reports will be comprehensive.

---

*Questions document created: 2025-10-04*
*Proceeding with implementation using recommendations above*
