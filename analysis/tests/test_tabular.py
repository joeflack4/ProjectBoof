"""Tests for tabular data analysis engine."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os

from analysis.core.tabular import (
    infer_data_type,
    calculate_basic_stats,
    detect_identifier_pattern,
    calculate_string_stats,
    calculate_numeric_stats,
    detect_encoding,
    infer_delimiter,
    classify_cardinality,
)


class TestInferDataType:
    """Test data type inference."""

    def test_integer_type(self):
        """Test integer type detection."""
        series = pd.Series([1, 2, 3, 4, 5])
        assert infer_data_type(series) == 'integer'

    def test_float_type(self):
        """Test float type detection."""
        series = pd.Series([1.5, 2.3, 3.7, 4.2])
        assert infer_data_type(series) == 'float'

    def test_string_type(self):
        """Test string type detection."""
        series = pd.Series(['apple', 'banana', 'cherry'])
        assert infer_data_type(series) == 'string'

    def test_boolean_type(self):
        """Test boolean type detection."""
        series = pd.Series(['true', 'false', 'true', 'false'])
        assert infer_data_type(series) == 'boolean'

        series = pd.Series([1, 0, 1, 0])
        assert infer_data_type(series) == 'boolean'

        series = pd.Series(['yes', 'no', 'yes'])
        assert infer_data_type(series) == 'boolean'

    def test_date_type(self):
        """Test date type detection."""
        series = pd.Series(['2024-01-01', '2024-02-15', '2024-03-20'])
        assert infer_data_type(series) == 'date'

        series = pd.Series(['01/15/2024', '02/20/2024'])
        assert infer_data_type(series) == 'date'

    def test_empty_series(self):
        """Test empty series returns 'empty'."""
        series = pd.Series([np.nan, np.nan, np.nan])
        assert infer_data_type(series) == 'empty'

    def test_mixed_with_nulls(self):
        """Test type inference with null values."""
        # Note: Series with integers and NaN becomes float type in pandas
        series = pd.Series([1, 2, np.nan, 3, np.nan, 4])
        assert infer_data_type(series) == 'float'


class TestDetectIdentifierPattern:
    """Test identifier pattern detection."""

    def test_hgnc_id_pattern(self):
        """Test HGNC ID pattern detection."""
        series = pd.Series(['HGNC:1234', 'HGNC:5678', 'HGNC:91011'])
        assert detect_identifier_pattern(series) == 'HGNC ID'

    def test_mondo_id_pattern(self):
        """Test MONDO ID pattern detection."""
        series = pd.Series(['MONDO:0000001', 'MONDO:0000002', 'MONDO:0000003'])
        assert detect_identifier_pattern(series) == 'MONDO ID'

    def test_dbsnp_pattern(self):
        """Test dbSNP rs ID pattern detection."""
        series = pd.Series(['rs123456', 'rs789012', 'rs345678'])
        assert detect_identifier_pattern(series) == 'dbSNP rsID'

    def test_url_pattern(self):
        """Test URL pattern detection."""
        series = pd.Series(['https://example.com', 'http://test.org', 'https://api.service.com'])
        assert detect_identifier_pattern(series) == 'URL'

    def test_no_pattern(self):
        """Test when no pattern matches."""
        series = pd.Series(['random', 'text', 'values'])
        assert detect_identifier_pattern(series) is None

    def test_pattern_below_threshold(self):
        """Test pattern not detected when below 80% threshold."""
        # Mix of HGNC and non-HGNC (only 60% match)
        series = pd.Series(['HGNC:1234', 'HGNC:5678', 'not_hgnc', 'also_not', 'neither'])
        pattern = detect_identifier_pattern(series)
        # Should not detect HGNC pattern with only 40% matches
        assert pattern != 'HGNC ID' or pattern is None


class TestCalculateBasicStats:
    """Test basic statistics calculation."""

    def test_basic_stats_complete(self):
        """Test basic stats with complete data."""
        series = pd.Series([1, 2, 3, 4, 5])
        stats = calculate_basic_stats(series)

        assert stats['total_count'] == 5
        assert stats['non_null_count'] == 5
        assert stats['null_count'] == 0
        assert stats['null_percentage'] == 0
        assert stats['unique_count'] == 5

    def test_basic_stats_with_nulls(self):
        """Test basic stats with null values."""
        series = pd.Series([1, 2, np.nan, 3, np.nan])
        stats = calculate_basic_stats(series)

        assert stats['total_count'] == 5
        assert stats['non_null_count'] == 3
        assert stats['null_count'] == 2
        assert stats['null_percentage'] == 40.0

    def test_basic_stats_duplicates(self):
        """Test unique count with duplicates."""
        series = pd.Series([1, 1, 2, 2, 2, 3])
        stats = calculate_basic_stats(series)

        assert stats['unique_count'] == 3


class TestClassifyCardinality:
    """Test cardinality classification."""

    def test_unique_cardinality(self):
        """Test unique cardinality (all values unique)."""
        assert classify_cardinality(5, 5) == 'unique'

    def test_low_cardinality(self):
        """Test low cardinality (<10 unique)."""
        assert classify_cardinality(5, 100) == 'low'
        assert classify_cardinality(9, 1000) == 'low'

    def test_medium_cardinality(self):
        """Test medium cardinality (10-999 unique)."""
        assert classify_cardinality(10, 100) == 'medium'
        assert classify_cardinality(500, 1000) == 'medium'
        assert classify_cardinality(999, 10000) == 'medium'

    def test_high_cardinality(self):
        """Test high cardinality (>=1000 unique)."""
        assert classify_cardinality(1000, 10000) == 'high'
        assert classify_cardinality(5000, 10000) == 'high'


class TestCalculateStringStats:
    """Test string statistics calculation."""

    def test_string_length_stats(self):
        """Test string length statistics."""
        series = pd.Series(['a', 'ab', 'abc', 'abcd'])
        stats = calculate_string_stats(series)

        assert stats['min_length'] == 1
        assert stats['max_length'] == 4
        assert stats['mean_length'] == 2.5

    def test_top_values(self):
        """Test top values extraction."""
        series = pd.Series(['apple', 'banana', 'apple', 'cherry', 'apple'])
        stats = calculate_string_stats(series)

        assert len(stats['top_values']) > 0
        assert stats['top_values'][0]['value'] == 'apple'
        assert stats['top_values'][0]['count'] == 3
        assert stats['top_values'][0]['percentage'] == 60.0


class TestCalculateNumericStats:
    """Test numeric statistics calculation."""

    def test_numeric_stats_basic(self):
        """Test basic numeric statistics."""
        series = pd.Series([1, 2, 3, 4, 5])
        stats = calculate_numeric_stats(series)

        assert stats['min'] == 1.0
        assert stats['max'] == 5.0
        assert stats['mean'] == 3.0
        assert stats['median'] == 3.0

    def test_numeric_stats_quartiles(self):
        """Test quartile calculations."""
        series = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        stats = calculate_numeric_stats(series)

        assert stats['q1'] == 3.25
        assert stats['q3'] == 7.75

    def test_numeric_stats_with_nulls(self):
        """Test numeric stats ignore nulls."""
        series = pd.Series([1, 2, np.nan, 3, np.nan, 4, 5])
        stats = calculate_numeric_stats(series)

        assert stats['mean'] == 3.0  # (1+2+3+4+5)/5
        assert stats['min'] == 1.0
        assert stats['max'] == 5.0


class TestFileUtilities:
    """Test file handling utilities."""

    def test_detect_encoding_utf8(self):
        """Test UTF-8 encoding detection."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.txt') as f:
            f.write('Test content with UTF-8')
            temp_path = f.name

        try:
            encoding = detect_encoding(Path(temp_path))
            assert encoding in ['utf-8', 'UTF-8', 'ascii', 'ASCII']
        finally:
            os.unlink(temp_path)

    def test_infer_delimiter_tab(self):
        """Test tab delimiter detection."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.tsv') as f:
            f.write('col1\tcol2\tcol3\n')
            temp_path = f.name

        try:
            delimiter = infer_delimiter(Path(temp_path))
            assert delimiter == '\t'
        finally:
            os.unlink(temp_path)

    def test_infer_delimiter_comma(self):
        """Test comma delimiter detection."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.csv') as f:
            f.write('col1,col2,col3\n')
            temp_path = f.name

        try:
            delimiter = infer_delimiter(Path(temp_path))
            assert delimiter == ','
        finally:
            os.unlink(temp_path)
