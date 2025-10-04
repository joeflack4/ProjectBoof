# Preliminary analysis updates
A good start on the preliminary analysis. However, some chagnges.

## 1. cross-source/ and reports/
I don't see any output here. Please create a new document notes/preliminary-analysis/report1.md, where you tell me if 
these are empty because the analysis has not yet been run, or because the work to do these hasn't been done, or some 
other reason.

If the analysis hasn't been run, ensure that it runs as part of `make preliminary-analysis`, and re-run the analysis to 
ensure outputs are created.

## 2. sources/ direct children dirs
The children of the sources/ dir appear to be specific files that are linked to particular sources. In some cases, the 
name of the source isn't even mentioned. This is poor design.

Let's change it so that the direct children dirs of this folder are the names of each source. Then, we can have dirs 
inside of it for the individual tables / files / artefacts from that source that we are analyzing. Make sure to move to 
move files and dirs around to adhere to this structure, and update the scripting so that it uses this structure.

## 3. TSV outputs: reports/files-metadata*-by-source.tsv
JSON outputs are not great for analysts. Let's make some TSVs. Let's make reports/files-metadata-json-by-source.tsv, where we 
grab all the metadata that we have in our json analysis files, and put it in that TSV. e.g.

```json
  "filepath": "data/sources/clingen/actionability/clinical-actionability-adult-flat.json",
  "filename": "clinical-actionability-adult-flat.json",
  "file_size_mb": 0.1309366226196289,
  "format": "json",
  "max_depth": 3,
  "node_count": 7142,
  "unique_paths": 5,
```

Do the same for source TSVs/CSVs/tabular we're analyzing. Make a reports/files-metadata-tabular-by-source.tsv. Example metadata:

```json
    "filepath": "gencc/gencc-submissions.tsv",
    "filename": "gencc-submissions.tsv",
    "file_size_mb": 14.833300590515137,
    "row_count": 24124,
    "column_count": 30,
    "delimiter": "\t",
    "encoding": "utf-8",
    "analyzed_date": "2025-10-04T22:15:39.529752",
    "sample_size": null
```

So the columns for the JSON should be e.g. filepath, filename, file_size_mb, row_count, etc. For tabular, should be 
similar. But each of these file types have distinctly different metadata.

Then make a reports/files-metadata-other-by-source.tsv. In this case, it'll have 3 columns: (i) filename, and (ii) key, and 
(iii) val. That way for any files we're analyzing that aren't JSON or TSV, we can aggregate all their metadata in one 
file, and maintain a 3 column structure. Note that I'm not sure we have any such files right now. This will just be for 
future proofing.

## 4. TSV outputs: reports/files-data*-by-source.tsv
Use the same / similar strategy as for step (3). Be creative as you need. The goal is to have report TSV where we see 
all of the different files for each of our sources. I'm guessing we'll have to split this up into tabular / json / 
other, rather than a single file. We should have a common header structure that doesn't explode. So each field in each 
file will not be a field in this TSV. There will be a 'field' header, and it will have the field names as its values. 
There will be several rows per field, showing the statistical props etc of that field.

Also for this, ignore the "top_values" statistic. We don't need to see that in this report.

## 5. TSV outputs: sources/
Do the same kind of thing as (4), representing our sources/SOURCE/FILE/FILENAME.json analysis that we currently have as 
a TSV instead, in the path: sources/SOURCE/FILE/FILENAME.tsv instead. Represent that data in tabular form

For this, also leave out the "top_values" statistic.

## 6. reports/unable-to-analyze.tsv
For any files that exist in sources which we were not able to analyze, list them here. Should have the following columns:
- filename
- path
- reason: The reason we could not analyze the file.
