# Questions for Data Source Documentation Research
## Answered
1. **Output Format**: Should I create individual documentation files for each data source (e.g., `clingen-docs.md`, 
`clinvar-docs.md`, etc.) or compile everything into a single master document?

A: That is correct! Except, let's call each file just SOURCE.md, e.g. clingen.md. Put them in docs/data-sources/ 
actually. The master document can be docs/data-sources.md.

2. **Level of Detail**: For the data structure documentation (files, tables, fields), how deep should I go? Should I document:
   - a.Just high-level structure (e.g., "VCF files with variant annotations")?
   - b. Moderate detail (major tables/files and their key fields)?
   - c. Comprehensive detail (all fields with descriptions)?

A: Good question. Let's go with 'b', moderate detail. FYI I created a new document as well, docs-start2.md, where I list
things that we may want to consider for later phases. I put 'c' in that document. 

3. **API Documentation**: If a data source has an API, should I:
   - a. Just note that an API exists and link to docs?
   - b. Document key endpoints and example queries?
   - c. Create example code snippets for common operations?

A: All of the above. Link to the docs, list the key endpoints, show example queries, and create example code snippets 
for common ops.

4. **Priority Order**: Should I research and document these data sources in any particular order, or just work through 
them alphabetically?

A: Start with cBioPortal, but then otherwise go through them linearly / alphabeticlaly.

5. **Harmonization Notes**: Should I include preliminary thoughts on how these data sources might be harmonized with 
each other (common fields, overlapping data, etc.), or save that for a later phase?

A: Later phase.

6. **Version Information**: Should I document specific versions of these data sources or focus on the current/latest 
available version?

A: Current/latest version.

## Unanswered

