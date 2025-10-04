"""
Generate aggregated TSV reports from all analysis JSON files.
"""

import csv
import json
from pathlib import Path
from typing import Dict, Any, List


def collect_analysis_files(sources_dir: Path) -> Dict[str, List[Path]]:
    """
    Collect all analysis JSON files organized by source.

    Args:
        sources_dir: Path to sources directory (e.g., output/preliminary-analysis/sources)

    Returns:
        Dictionary mapping source names to lists of JSON file paths
    """
    sources = {}

    for source_dir in sources_dir.iterdir():
        if not source_dir.is_dir():
            continue

        source_name = source_dir.name
        json_files = []

        # Find all profile JSON files
        for json_file in source_dir.rglob("*_profile.json"):
            json_files.append(json_file)

        if json_files:
            sources[source_name] = json_files

    return sources


def generate_files_metadata_tabular_tsv(sources_dir: Path, output_path: Path) -> None:
    """
    Generate TSV with metadata for all tabular files analyzed.

    Columns: source, filepath, filename, file_size_mb, row_count, column_count,
             delimiter, encoding, analyzed_date, sample_size
    """
    sources = collect_analysis_files(sources_dir)

    rows = []
    for source_name, json_files in sources.items():
        for json_file in json_files:
            with open(json_file, 'r') as f:
                data = json.load(f)

            # Check for tabular files - either by format or by presence of field_analyses
            file_metadata = data.get('file_metadata', {})
            is_tabular = (data.get('format') in ['csv', 'tsv', 'txt'] or
                         'field_analyses' in data)

            if is_tabular:
                row = {
                    'source': source_name,
                    'filepath': data.get('filepath', file_metadata.get('filepath', '')),
                    'filename': data.get('filename', file_metadata.get('filename', '')),
                    'file_size_mb': data.get('file_size_mb', file_metadata.get('file_size_mb', '')),
                    'row_count': data.get('row_count', file_metadata.get('row_count', '')),
                    'column_count': data.get('column_count', file_metadata.get('column_count', '')),
                    'delimiter': data.get('delimiter', file_metadata.get('delimiter', '')),
                    'encoding': data.get('encoding', file_metadata.get('encoding', '')),
                    'analyzed_date': data.get('analyzed_date', file_metadata.get('analyzed_date', '')),
                    'sample_size': data.get('sample_size', file_metadata.get('sample_size', ''))
                }
                rows.append(row)

    # Write TSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter='\t')
            writer.writeheader()
            writer.writerows(rows)


def generate_files_metadata_json_tsv(sources_dir: Path, output_path: Path) -> None:
    """
    Generate TSV with metadata for all JSON files analyzed.

    Columns: source, filepath, filename, file_size_mb, format, max_depth,
             node_count, unique_paths, analyzed_date
    """
    sources = collect_analysis_files(sources_dir)

    rows = []
    for source_name, json_files in sources.items():
        for json_file in json_files:
            with open(json_file, 'r') as f:
                data = json.load(f)

            # Only include JSON/XML files
            if data.get('format') in ['json', 'xml']:
                row = {
                    'source': source_name,
                    'filepath': data.get('filepath', ''),
                    'filename': data.get('filename', ''),
                    'file_size_mb': data.get('file_size_mb', ''),
                    'format': data.get('format', ''),
                    'max_depth': data.get('max_depth', ''),
                    'node_count': data.get('node_count', ''),
                    'unique_paths': data.get('unique_paths', ''),
                    'analyzed_date': data.get('analyzed_date', '')
                }
                rows.append(row)

    # Write TSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter='\t')
            writer.writeheader()
            writer.writerows(rows)


def generate_files_metadata_other_tsv(sources_dir: Path, output_path: Path) -> None:
    """
    Generate TSV with metadata for other file types.

    Columns: source, filename, key, val
    """
    sources = collect_analysis_files(sources_dir)

    rows = []
    for source_name, json_files in sources.items():
        for json_file in json_files:
            with open(json_file, 'r') as f:
                data = json.load(f)

            # Only include other file types (not tabular or json/xml)
            if data.get('format') not in ['csv', 'tsv', 'txt', 'json', 'xml']:
                filename = data.get('filename', '')
                for key, val in data.items():
                    if key not in ['filepath', 'filename']:  # Don't duplicate filename
                        rows.append({
                            'source': source_name,
                            'filename': filename,
                            'key': key,
                            'val': str(val)
                        })

    # Write TSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['source', 'filename', 'key', 'val'], delimiter='\t')
            writer.writeheader()
            writer.writerows(rows)


def generate_files_data_tabular_tsv(sources_dir: Path, output_path: Path) -> None:
    """
    Generate TSV with field-level data for all tabular files.

    Columns: source, filename, field_name, data_type, null_count, null_percentage,
             cardinality, min_value, max_value, mean_value, unique_count
    """
    sources = collect_analysis_files(sources_dir)

    rows = []
    for source_name, json_files in sources.items():
        for json_file in json_files:
            with open(json_file, 'r') as f:
                data = json.load(f)

            # Check for tabular files
            file_metadata = data.get('file_metadata', {})
            field_analyses = data.get('field_analyses', [])

            if field_analyses:  # Has field analyses = tabular
                filename = data.get('filename', file_metadata.get('filename', ''))

                for field in field_analyses:
                    # Stats are directly on field object, not nested
                    row = {
                        'source': source_name,
                        'filename': filename,
                        'field_name': field.get('field_name', ''),
                        'data_type': field.get('data_type', ''),
                        'null_count': field.get('null_count', ''),
                        'null_percentage': field.get('null_percentage', ''),
                        'cardinality': field.get('cardinality', ''),
                        'unique_count': field.get('unique_count', ''),
                        'min_value': field.get('min_value', ''),
                        'max_value': field.get('max_value', ''),
                        'mean_value': field.get('mean_value', ''),
                        'min_length': field.get('min_length', ''),
                        'max_length': field.get('max_length', ''),
                        'mean_length': field.get('mean_length', '')
                    }
                    rows.append(row)

    # Write TSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter='\t')
            writer.writeheader()
            writer.writerows(rows)


def generate_files_data_json_tsv(sources_dir: Path, output_path: Path) -> None:
    """
    Generate TSV with field-level data for all JSON files.

    Columns: source, filename, path, max_depth, node_count
    """
    sources = collect_analysis_files(sources_dir)

    rows = []
    for source_name, json_files in sources.items():
        for json_file in json_files:
            with open(json_file, 'r') as f:
                data = json.load(f)

            # Only include JSON/XML files
            if data.get('format') in ['json', 'xml']:
                filename = data.get('filename', '')
                paths = data.get('paths', [])

                for path in paths:
                    row = {
                        'source': source_name,
                        'filename': filename,
                        'path': path,
                        'max_depth': data.get('max_depth', ''),
                        'node_count': data.get('node_count', '')
                    }
                    rows.append(row)

    # Write TSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter='\t')
            writer.writeheader()
            writer.writerows(rows)


def generate_individual_field_tsv(json_path: Path, output_path: Path) -> None:
    """
    Generate TSV representation of a single file's analysis (for sources/SOURCE/FILE/FILENAME.tsv).

    For tabular files: field_name, data_type, null_count, null_percentage, cardinality, etc.
    For JSON files: path
    """
    with open(json_path, 'r') as f:
        data = json.load(f)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Check for tabular files (has field_analyses)
    field_analyses = data.get('field_analyses', [])

    if field_analyses:
        # Tabular format
        rows = []

        for field in field_analyses:
            # Stats are directly on field object, not nested
            row = {
                'field_name': field.get('field_name', ''),
                'data_type': field.get('data_type', ''),
                'null_count': field.get('null_count', ''),
                'null_percentage': field.get('null_percentage', ''),
                'cardinality': field.get('cardinality', ''),
                'unique_count': field.get('unique_count', ''),
                'min_value': field.get('min_value', ''),
                'max_value': field.get('max_value', ''),
                'mean_value': field.get('mean_value', ''),
                'min_length': field.get('min_length', ''),
                'max_length': field.get('max_length', ''),
                'mean_length': field.get('mean_length', ''),
                'identifiers': ', '.join(field.get('identifiers', []))
            }
            rows.append(row)

        if rows:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter='\t')
                writer.writeheader()
                writer.writerows(rows)

    elif data.get('format') in ['json', 'xml']:
        # Semi-structured format
        paths = data.get('paths', [])
        rows = []

        for path in paths:
            row = {
                'path': path
            }
            rows.append(row)

        if rows:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['path'], delimiter='\t')
                writer.writeheader()
                writer.writerows(rows)


def generate_unable_to_analyze_tsv(data_dir: Path, sources_dir: Path, output_path: Path) -> None:
    """
    Generate TSV listing files that could not be analyzed.

    Columns: filename, path, reason
    """
    # Find all files in data/sources
    all_data_files = set()
    for filepath in data_dir.rglob('*'):
        if filepath.is_file() and filepath.suffix in ['.tsv', '.csv', '.txt', '.json', '.xml']:
            all_data_files.add(filepath)

    # Find all analyzed files
    analyzed_files = set()
    for json_file in sources_dir.rglob('*_profile.json'):
        with open(json_file, 'r') as f:
            data = json.load(f)
            if 'filepath' in data:
                analyzed_files.add(Path(data['filepath']))

    # Find unanalyzed files
    unanalyzed = all_data_files - analyzed_files

    rows = []
    for filepath in sorted(unanalyzed):
        rows.append({
            'filename': filepath.name,
            'path': str(filepath),
            'reason': 'Not analyzed - may be unsupported format or error during analysis'
        })

    # Write TSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['filename', 'path', 'reason'], delimiter='\t')
            writer.writeheader()
            writer.writerows(rows)
    else:
        # Create empty file with headers
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['filename', 'path', 'reason'], delimiter='\t')
            writer.writeheader()


def generate_all_tsv_reports(sources_dir: Path, data_dir: Path, reports_dir: Path) -> None:
    """
    Generate all aggregated TSV reports.

    Args:
        sources_dir: Path to sources directory (e.g., output/preliminary-analysis/sources)
        data_dir: Path to data directory (e.g., data/sources)
        reports_dir: Path to reports directory (e.g., output/preliminary-analysis/reports)
    """
    print("📊 Generating TSV reports...")

    # Metadata reports
    generate_files_metadata_tabular_tsv(sources_dir, reports_dir / "files-metadata-tabular-by-source.tsv")
    print("  ✓ files-metadata-tabular-by-source.tsv")

    generate_files_metadata_json_tsv(sources_dir, reports_dir / "files-metadata-json-by-source.tsv")
    print("  ✓ files-metadata-json-by-source.tsv")

    generate_files_metadata_other_tsv(sources_dir, reports_dir / "files-metadata-other-by-source.tsv")
    print("  ✓ files-metadata-other-by-source.tsv")

    # Field data reports
    generate_files_data_tabular_tsv(sources_dir, reports_dir / "files-data-tabular-by-source.tsv")
    print("  ✓ files-data-tabular-by-source.tsv")

    generate_files_data_json_tsv(sources_dir, reports_dir / "files-data-json-by-source.tsv")
    print("  ✓ files-data-json-by-source.tsv")

    # Unable to analyze report
    generate_unable_to_analyze_tsv(data_dir, sources_dir, reports_dir / "unable-to-analyze.tsv")
    print("  ✓ unable-to-analyze.tsv")

    # Individual TSV files for each analysis
    print("  Generating individual TSV files...")
    for json_file in sources_dir.rglob('*_profile.json'):
        tsv_path = json_file.parent / f"{json_file.stem.replace('_profile', '')}_fields.tsv"
        generate_individual_field_tsv(json_file, tsv_path)
    print("  ✓ Individual field TSVs created")

    print(f"✅ All TSV reports generated in {reports_dir}/")
