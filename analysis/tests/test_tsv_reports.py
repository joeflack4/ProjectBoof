"""
Tests for TSV report generation functionality.
"""

import csv
import json
import pytest
import tempfile
from pathlib import Path
from analysis.reports.tsv_reports import (
    collect_analysis_files,
    generate_files_metadata_tabular_tsv,
    generate_files_metadata_json_tsv,
    generate_files_metadata_other_tsv,
    generate_files_data_tabular_tsv,
    generate_files_data_json_tsv,
    generate_individual_field_tsv,
    generate_unable_to_analyze_tsv,
    generate_all_tsv_reports
)


@pytest.fixture
def temp_sources_dir(tmp_path):
    """Create a temporary sources directory with sample analysis files."""
    sources_dir = tmp_path / "sources"

    # Create gencc source
    gencc_dir = sources_dir / "gencc" / "gencc-submissions"
    gencc_dir.mkdir(parents=True)

    gencc_analysis = {
        "file_metadata": {
            "filepath": "gencc/gencc-submissions.tsv",
            "filename": "gencc-submissions.tsv",
            "file_size_mb": 14.83,
            "row_count": 24124,
            "column_count": 30,
            "delimiter": "\t",
            "encoding": "utf-8",
            "analyzed_date": "2025-10-04T22:15:39.529752",
            "sample_size": None
        },
        "field_analyses": [
            {
                "field_name": "uuid",
                "data_type": "string",
                "null_count": 0,
                "null_percentage": 0.0,
                "cardinality": "unique",
                "unique_count": 24124,
                "min_length": 55,
                "max_length": 64,
                "mean_length": 59.43,
                "identifiers": ["GENCC"]
            },
            {
                "field_name": "gene_symbol",
                "data_type": "string",
                "null_count": 0,
                "null_percentage": 0.0,
                "cardinality": "high",
                "unique_count": 5533,
                "min_length": 2,
                "max_length": 10,
                "mean_length": 5.01,
                "identifiers": []
            }
        ]
    }

    with open(gencc_dir / "gencc-submissions_profile.json", "w") as f:
        json.dump(gencc_analysis, f)

    # Create clingen JSON source
    clingen_dir = sources_dir / "clingen" / "clinical-actionability"
    clingen_dir.mkdir(parents=True)

    clingen_analysis = {
        "filepath": "data/sources/clingen/actionability/clinical-actionability-adult-flat.json",
        "filename": "clinical-actionability-adult-flat.json",
        "file_size_mb": 0.13,
        "format": "json",
        "max_depth": 3,
        "node_count": 7142,
        "unique_paths": 5,
        "paths": [
            "columns",
            "columns[]",
            "rows",
            "rows[]",
            "rows[][]"
        ]
    }

    with open(clingen_dir / "clinical-actionability-adult-flat_profile.json", "w") as f:
        json.dump(clingen_analysis, f)

    return sources_dir


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary data directory with sample files."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    # Create some sample files
    (data_dir / "file1.tsv").write_text("col1\tcol2\nval1\tval2\n")
    (data_dir / "file2.json").write_text('{"key": "value"}')
    (data_dir / "file3.csv").write_text("col1,col2\nval1,val2\n")

    return data_dir


class TestCollectAnalysisFiles:
    """Tests for collect_analysis_files function."""

    def test_collect_from_organized_sources(self, temp_sources_dir):
        """Test collecting analysis files from organized source directories."""
        sources = collect_analysis_files(temp_sources_dir)

        assert "gencc" in sources
        assert "clingen" in sources
        assert len(sources["gencc"]) == 1
        assert len(sources["clingen"]) == 1
        assert sources["gencc"][0].name == "gencc-submissions_profile.json"
        assert sources["clingen"][0].name == "clinical-actionability-adult-flat_profile.json"

    def test_collect_empty_directory(self, tmp_path):
        """Test collecting from empty directory returns empty dict."""
        sources = collect_analysis_files(tmp_path)
        assert sources == {}


class TestGenerateFilesMetadataTabularTSV:
    """Tests for generate_files_metadata_tabular_tsv function."""

    def test_generates_correct_columns(self, temp_sources_dir, tmp_path):
        """Test that TSV has correct column headers."""
        output_path = tmp_path / "metadata.tsv"
        generate_files_metadata_tabular_tsv(temp_sources_dir, output_path)

        assert output_path.exists()

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            headers = reader.fieldnames

            assert 'source' in headers
            assert 'filepath' in headers
            assert 'filename' in headers
            assert 'file_size_mb' in headers
            assert 'row_count' in headers
            assert 'column_count' in headers
            assert 'delimiter' in headers
            assert 'encoding' in headers

    def test_includes_tabular_files_only(self, temp_sources_dir, tmp_path):
        """Test that only tabular files are included."""
        output_path = tmp_path / "metadata.tsv"
        generate_files_metadata_tabular_tsv(temp_sources_dir, output_path)

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            rows = list(reader)

            # Should only have gencc (tabular), not clingen (json)
            assert len(rows) == 1
            assert rows[0]['source'] == 'gencc'
            assert rows[0]['filename'] == 'gencc-submissions.tsv'

    def test_correct_metadata_values(self, temp_sources_dir, tmp_path):
        """Test that metadata values are correctly extracted."""
        output_path = tmp_path / "metadata.tsv"
        generate_files_metadata_tabular_tsv(temp_sources_dir, output_path)

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            row = next(reader)

            assert row['row_count'] == '24124'
            assert row['column_count'] == '30'
            assert row['delimiter'] == '\t'
            assert row['encoding'] == 'utf-8'


class TestGenerateFilesMetadataJSONTSV:
    """Tests for generate_files_metadata_json_tsv function."""

    def test_generates_correct_columns(self, temp_sources_dir, tmp_path):
        """Test that TSV has correct column headers."""
        output_path = tmp_path / "metadata_json.tsv"
        generate_files_metadata_json_tsv(temp_sources_dir, output_path)

        assert output_path.exists()

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            headers = reader.fieldnames

            assert 'source' in headers
            assert 'format' in headers
            assert 'max_depth' in headers
            assert 'node_count' in headers
            assert 'unique_paths' in headers

    def test_includes_json_files_only(self, temp_sources_dir, tmp_path):
        """Test that only JSON/XML files are included."""
        output_path = tmp_path / "metadata_json.tsv"
        generate_files_metadata_json_tsv(temp_sources_dir, output_path)

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            rows = list(reader)

            # Should only have clingen (json), not gencc (tabular)
            assert len(rows) == 1
            assert rows[0]['source'] == 'clingen'
            assert rows[0]['format'] == 'json'


class TestGenerateFilesDataTabularTSV:
    """Tests for generate_files_data_tabular_tsv function."""

    def test_generates_correct_columns(self, temp_sources_dir, tmp_path):
        """Test that TSV has correct field-level columns."""
        output_path = tmp_path / "data_tabular.tsv"
        generate_files_data_tabular_tsv(temp_sources_dir, output_path)

        assert output_path.exists()

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            headers = reader.fieldnames

            assert 'source' in headers
            assert 'filename' in headers
            assert 'field_name' in headers
            assert 'data_type' in headers
            assert 'null_count' in headers
            assert 'null_percentage' in headers
            assert 'cardinality' in headers
            assert 'unique_count' in headers
            assert 'min_length' in headers
            assert 'max_length' in headers
            assert 'mean_length' in headers

    def test_includes_all_fields(self, temp_sources_dir, tmp_path):
        """Test that all fields from analysis are included."""
        output_path = tmp_path / "data_tabular.tsv"
        generate_files_data_tabular_tsv(temp_sources_dir, output_path)

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            rows = list(reader)

            # Should have 2 fields from gencc
            assert len(rows) == 2
            assert rows[0]['field_name'] == 'uuid'
            assert rows[1]['field_name'] == 'gene_symbol'

    def test_correct_field_statistics(self, temp_sources_dir, tmp_path):
        """Test that field statistics are correctly extracted."""
        output_path = tmp_path / "data_tabular.tsv"
        generate_files_data_tabular_tsv(temp_sources_dir, output_path)

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            rows = list(reader)

            # Check uuid field
            assert rows[0]['data_type'] == 'string'
            assert rows[0]['null_count'] == '0'
            assert rows[0]['null_percentage'] == '0.0'
            assert rows[0]['cardinality'] == 'unique'
            assert rows[0]['unique_count'] == '24124'
            assert rows[0]['min_length'] == '55'
            assert rows[0]['max_length'] == '64'

            # Check gene_symbol field
            assert rows[1]['field_name'] == 'gene_symbol'
            assert rows[1]['cardinality'] == 'high'
            assert rows[1]['unique_count'] == '5533'


class TestGenerateFilesDataJSONTSV:
    """Tests for generate_files_data_json_tsv function."""

    def test_generates_correct_columns(self, temp_sources_dir, tmp_path):
        """Test that TSV has correct columns for JSON data."""
        output_path = tmp_path / "data_json.tsv"
        generate_files_data_json_tsv(temp_sources_dir, output_path)

        assert output_path.exists()

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            headers = reader.fieldnames

            assert 'source' in headers
            assert 'filename' in headers
            assert 'path' in headers
            assert 'max_depth' in headers
            assert 'node_count' in headers

    def test_includes_all_paths(self, temp_sources_dir, tmp_path):
        """Test that all JSON paths are included."""
        output_path = tmp_path / "data_json.tsv"
        generate_files_data_json_tsv(temp_sources_dir, output_path)

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            rows = list(reader)

            # Should have 5 paths from clingen
            assert len(rows) == 5
            paths = [row['path'] for row in rows]
            assert 'columns' in paths
            assert 'rows[][]' in paths


class TestGenerateIndividualFieldTSV:
    """Tests for generate_individual_field_tsv function."""

    def test_tabular_field_tsv(self, temp_sources_dir, tmp_path):
        """Test generating individual TSV for tabular file."""
        json_path = temp_sources_dir / "gencc" / "gencc-submissions" / "gencc-submissions_profile.json"
        output_path = tmp_path / "gencc_fields.tsv"

        generate_individual_field_tsv(json_path, output_path)

        assert output_path.exists()

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            rows = list(reader)

            assert len(rows) == 2
            assert rows[0]['field_name'] == 'uuid'
            assert rows[0]['identifiers'] == 'GENCC'
            assert 'null_count' in reader.fieldnames
            assert 'cardinality' in reader.fieldnames

    def test_json_field_tsv(self, temp_sources_dir, tmp_path):
        """Test generating individual TSV for JSON file."""
        json_path = temp_sources_dir / "clingen" / "clinical-actionability" / "clinical-actionability-adult-flat_profile.json"
        output_path = tmp_path / "clingen_paths.tsv"

        generate_individual_field_tsv(json_path, output_path)

        assert output_path.exists()

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            rows = list(reader)

            assert len(rows) == 5
            assert rows[0]['path'] == 'columns'


class TestGenerateUnableToAnalyzeTSV:
    """Tests for generate_unable_to_analyze_tsv function."""

    def test_identifies_unanalyzed_files(self, temp_data_dir, temp_sources_dir, tmp_path):
        """Test that unanalyzed files are identified."""
        output_path = tmp_path / "unable.tsv"

        # temp_data_dir has 3 files, temp_sources_dir has 2 analyzed
        # So there should be unanalyzed files
        generate_unable_to_analyze_tsv(temp_data_dir, temp_sources_dir, output_path)

        assert output_path.exists()

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            headers = reader.fieldnames

            assert 'filename' in headers
            assert 'path' in headers
            assert 'reason' in headers

    def test_empty_when_all_analyzed(self, temp_data_dir, tmp_path):
        """Test that TSV is empty (headers only) when all files analyzed."""
        # Create sources dir with all files analyzed
        sources_dir = tmp_path / "sources_complete"
        sources_dir.mkdir()

        for filepath in temp_data_dir.glob('*'):
            source_dir = sources_dir / "test" / filepath.stem
            source_dir.mkdir(parents=True)

            analysis = {
                "filepath": str(filepath),
                "filename": filepath.name
            }

            with open(source_dir / f"{filepath.stem}_profile.json", "w") as f:
                json.dump(analysis, f)

        output_path = tmp_path / "unable_empty.tsv"
        generate_unable_to_analyze_tsv(temp_data_dir, sources_dir, output_path)

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            rows = list(reader)

            # Should have headers but no data rows
            assert len(rows) == 0


class TestGenerateAllTSVReports:
    """Tests for generate_all_tsv_reports function."""

    def test_generates_all_report_files(self, temp_sources_dir, temp_data_dir, tmp_path):
        """Test that all report files are created."""
        reports_dir = tmp_path / "reports"

        generate_all_tsv_reports(temp_sources_dir, temp_data_dir, reports_dir)

        # Check all expected files exist
        assert (reports_dir / "files-metadata-tabular-by-source.tsv").exists()
        assert (reports_dir / "files-metadata-json-by-source.tsv").exists()
        assert (reports_dir / "files-metadata-other-by-source.tsv").exists()
        assert (reports_dir / "files-data-tabular-by-source.tsv").exists()
        assert (reports_dir / "files-data-json-by-source.tsv").exists()
        assert (reports_dir / "unable-to-analyze.tsv").exists()

    def test_creates_individual_tsvs(self, temp_sources_dir, temp_data_dir, tmp_path):
        """Test that individual field TSVs are created."""
        reports_dir = tmp_path / "reports"

        generate_all_tsv_reports(temp_sources_dir, temp_data_dir, reports_dir)

        # Check individual TSVs were created
        gencc_tsv = temp_sources_dir / "gencc" / "gencc-submissions" / "gencc-submissions_fields.tsv"
        clingen_tsv = temp_sources_dir / "clingen" / "clinical-actionability" / "clinical-actionability-adult-flat_fields.tsv"

        assert gencc_tsv.exists()
        assert clingen_tsv.exists()


class TestDataQuality:
    """Tests for data quality and correctness."""

    def test_no_empty_required_fields(self, temp_sources_dir, tmp_path):
        """Test that required fields are not empty."""
        output_path = tmp_path / "data_tabular.tsv"
        generate_files_data_tabular_tsv(temp_sources_dir, output_path)

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')

            for row in reader:
                # These fields should never be empty
                assert row['source'], "Source field is empty"
                assert row['filename'], "Filename field is empty"
                assert row['field_name'], "Field name is empty"
                assert row['data_type'], "Data type is empty"

    def test_numeric_fields_are_numeric(self, temp_sources_dir, tmp_path):
        """Test that numeric fields contain valid numbers or are empty."""
        output_path = tmp_path / "data_tabular.tsv"
        generate_files_data_tabular_tsv(temp_sources_dir, output_path)

        with open(output_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')

            for row in reader:
                # Check numeric fields
                if row['null_count']:
                    assert row['null_count'].isdigit(), f"null_count is not numeric: {row['null_count']}"

                if row['unique_count']:
                    assert row['unique_count'].isdigit(), f"unique_count is not numeric: {row['unique_count']}"

                if row['null_percentage']:
                    try:
                        float(row['null_percentage'])
                    except ValueError:
                        pytest.fail(f"null_percentage is not a valid float: {row['null_percentage']}")

    def test_tsv_format_valid(self, temp_sources_dir, tmp_path):
        """Test that TSV files have consistent column counts."""
        output_path = tmp_path / "data_tabular.tsv"
        generate_files_data_tabular_tsv(temp_sources_dir, output_path)

        with open(output_path, 'r') as f:
            lines = f.readlines()

            # Count tabs in header
            header_tabs = lines[0].count('\t')

            # All lines should have same number of tabs
            for i, line in enumerate(lines[1:], start=2):
                line_tabs = line.count('\t')
                assert line_tabs == header_tabs, f"Line {i} has {line_tabs} tabs, expected {header_tabs}"
