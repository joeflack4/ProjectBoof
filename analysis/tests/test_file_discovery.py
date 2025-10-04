"""Tests for file discovery utilities."""

import pytest
import tempfile
import os
from pathlib import Path

from analysis.core.file_discovery import discover_files


class TestDiscoverFiles:
    """Test file discovery functionality."""

    def test_discover_tabular_files(self):
        """Test discovering tabular files (CSV, TSV, TXT)."""
        # Create temporary directory structure
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            source_dir = base / 'test_source'
            source_dir.mkdir()

            # Create test files
            (source_dir / 'data.csv').write_text('col1,col2\nval1,val2\n')
            (source_dir / 'data.tsv').write_text('col1\tcol2\nval1\tval2\n')
            (source_dir / 'data.txt').write_text('col1\tcol2\nval1\tval2\n')

            files = discover_files(str(base))

            # Should find all 3 tabular files
            assert len(files) == 3
            assert all(f['filetype'] == 'tabular' for f in files)
            assert all(f['source'] == 'test_source' for f in files)

    def test_discover_json_files(self):
        """Test discovering JSON files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            source_dir = base / 'json_source'
            source_dir.mkdir()

            # Create JSON file
            (source_dir / 'data.json').write_text('{"key": "value"}')

            files = discover_files(str(base))

            assert len(files) == 1
            assert files[0]['filetype'] == 'json'
            assert files[0]['source'] == 'json_source'

    def test_discover_xml_files(self):
        """Test discovering XML files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            source_dir = base / 'xml_source'
            source_dir.mkdir()

            # Create XML file
            (source_dir / 'data.xml').write_text('<root><item>value</item></root>')

            files = discover_files(str(base))

            assert len(files) == 1
            assert files[0]['filetype'] == 'xml'
            assert files[0]['source'] == 'xml_source'

    def test_discover_gzipped_files(self):
        """Test discovering gzipped files (e.g., .txt.gz, .csv.gz)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            source_dir = base / 'gz_source'
            source_dir.mkdir()

            # Create gzipped tabular file
            (source_dir / 'data.txt.gz').write_text('compressed')
            (source_dir / 'data.csv.gz').write_text('compressed')

            files = discover_files(str(base))

            # Should identify as tabular based on extension before .gz
            assert len(files) == 2
            assert all(f['filetype'] == 'tabular' for f in files)

    def test_skip_hidden_files(self):
        """Test that hidden files are skipped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            source_dir = base / 'test_source'
            source_dir.mkdir()

            # Create visible and hidden files
            (source_dir / 'data.csv').write_text('col1,col2\n')
            (source_dir / '.hidden.csv').write_text('col1,col2\n')

            files = discover_files(str(base))

            # Should only find the non-hidden file
            assert len(files) == 1
            assert not files[0]['filepath'].endswith('.hidden.csv')

    def test_skip_manifest_files(self):
        """Test that manifest.json files are skipped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            source_dir = base / 'test_source'
            source_dir.mkdir()

            # Create data and manifest files
            (source_dir / 'data.json').write_text('{"data": "value"}')
            (source_dir / 'manifest.json').write_text('{"manifest": "metadata"}')

            files = discover_files(str(base))

            # Should only find data.json, not manifest.json
            assert len(files) == 1
            assert 'data.json' in files[0]['filepath']

    def test_recursive_discovery(self):
        """Test recursive file discovery in nested directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            source_dir = base / 'test_source'
            nested_dir = source_dir / 'subdir' / 'nested'
            nested_dir.mkdir(parents=True)

            # Create files at different levels
            (source_dir / 'top.csv').write_text('col1,col2\n')
            (source_dir / 'subdir' / 'mid.csv').write_text('col1,col2\n')
            (nested_dir / 'deep.csv').write_text('col1,col2\n')

            files = discover_files(str(base))

            # Should find all 3 files
            assert len(files) == 3
            assert all(f['source'] == 'test_source' for f in files)

    def test_multiple_sources(self):
        """Test discovering files from multiple source directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)

            # Create multiple source directories
            source1 = base / 'source1'
            source2 = base / 'source2'
            source1.mkdir()
            source2.mkdir()

            (source1 / 'data1.csv').write_text('col1,col2\n')
            (source2 / 'data2.json').write_text('{"key": "value"}')

            files = discover_files(str(base))

            # Should find both files
            assert len(files) == 2
            sources = {f['source'] for f in files}
            assert sources == {'source1', 'source2'}

    def test_ignore_non_analyzable_extensions(self):
        """Test that non-analyzable file extensions are ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            source_dir = base / 'test_source'
            source_dir.mkdir()

            # Create various files
            (source_dir / 'data.csv').write_text('col1,col2\n')
            (source_dir / 'image.png').write_bytes(b'fake_image')
            (source_dir / 'doc.pdf').write_bytes(b'fake_pdf')
            (source_dir / 'readme.md').write_text('# README')

            files = discover_files(str(base))

            # Should only find CSV
            assert len(files) == 1
            assert files[0]['filepath'].endswith('data.csv')

    def test_extension_field(self):
        """Test that extension field is correctly populated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            source_dir = base / 'test_source'
            source_dir.mkdir()

            (source_dir / 'data.csv').write_text('col1,col2\n')
            (source_dir / 'data.txt.gz').write_text('compressed')

            files = discover_files(str(base))

            # Check extensions
            csv_file = next(f for f in files if 'data.csv' in f['filepath'])
            assert csv_file['extension'] == '.csv'

            gz_file = next(f for f in files if 'data.txt.gz' in f['filepath'])
            assert gz_file['extension'] == '.gz'
