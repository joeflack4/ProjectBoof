"""File discovery utilities for finding data files."""

from pathlib import Path
from typing import List, Dict


def discover_files(base_path: str = "data/sources") -> List[Dict[str, str]]:
    """
    Discover all analyzable files in the data sources directory.

    Returns list of dicts with:
    - source: Source name (gencc, clingen, etc.)
    - filepath: Full path to file
    - filetype: tsv, csv, json, xml, etc.
    """
    base = Path(base_path)
    files = []

    # File extensions to analyze
    tabular_exts = {'.tsv', '.csv', '.txt'}
    json_exts = {'.json'}
    xml_exts = {'.xml'}

    for source_dir in base.iterdir():
        if not source_dir.is_dir():
            continue

        source_name = source_dir.name

        # Recursively find files
        for filepath in source_dir.rglob('*'):
            if not filepath.is_file():
                continue

            # Skip hidden files and manifests
            if filepath.name.startswith('.') or filepath.name == 'manifest.json':
                continue

            # Determine file type
            suffix = filepath.suffix.lower()
            if suffix == '.gz':
                # Check the extension before .gz
                suffix = '.' + filepath.stem.split('.')[-1] if '.' in filepath.stem else suffix

            filetype = None
            if suffix in tabular_exts:
                filetype = 'tabular'
            elif suffix in json_exts:
                filetype = 'json'
            elif suffix in xml_exts:
                filetype = 'xml'

            if filetype:
                files.append({
                    'source': source_name,
                    'filepath': str(filepath),
                    'filetype': filetype,
                    'extension': filepath.suffix,
                })

    return files
