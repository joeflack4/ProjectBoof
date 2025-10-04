"""Tabular data analysis engine for CSV/TSV files."""

from pathlib import Path
from typing import Dict, Any, Optional, List
import re
from datetime import datetime

import pandas as pd
import numpy as np
import chardet


def detect_encoding(filepath: Path) -> str:
    """Detect file encoding using chardet."""
    with open(filepath, 'rb') as f:
        result = chardet.detect(f.read(100000))  # Read first 100KB

    # Map ASCII to UTF-8 (ASCII is a subset of UTF-8)
    encoding = result['encoding'] or 'utf-8'
    if encoding.lower() in ['ascii', 'us-ascii']:
        encoding = 'utf-8'

    return encoding


def infer_delimiter(filepath: Path, encoding: str = 'utf-8') -> str:
    """Infer delimiter from file (tab, comma, pipe, etc.)."""
    with open(filepath, 'r', encoding=encoding) as f:
        first_line = f.readline()

    # Count common delimiters
    delimiters = {
        '\t': first_line.count('\t'),
        ',': first_line.count(','),
        '|': first_line.count('|'),
        ';': first_line.count(';'),
    }

    # Return delimiter with highest count
    return max(delimiters, key=delimiters.get)


def detect_null_values() -> List[str]:
    """Return list of strings that should be treated as null."""
    return ['', 'NA', 'N/A', 'NULL', 'None', 'NaN', '-', '.', '?', 'na', 'n/a', 'null']


def infer_data_type(series: pd.Series) -> str:
    """
    Infer data type of a pandas Series.

    Returns: 'integer', 'float', 'date', 'boolean', 'string', or 'mixed'
    """
    # Remove null values for type inference
    non_null = series.dropna()

    if len(non_null) == 0:
        return 'empty'

    # Try boolean first (simple check)
    unique_vals = non_null.unique()
    if len(unique_vals) <= 2:
        bool_values = {'true', 'false', '1', '0', 'yes', 'no', 't', 'f', 'y', 'n'}
        if all(str(v).lower() in bool_values for v in unique_vals):
            return 'boolean'

    # Try integer
    try:
        pd.to_numeric(non_null, downcast='integer')
        if all(non_null.astype(str).str.match(r'^-?\d+$')):
            return 'integer'
    except (ValueError, TypeError):
        pass

    # Try float
    try:
        pd.to_numeric(non_null)
        return 'float'
    except (ValueError, TypeError):
        pass

    # Try date
    date_formats = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
    ]

    for fmt in date_formats:
        try:
            pd.to_datetime(non_null, format=fmt)
            return 'date'
        except (ValueError, TypeError):
            continue

    # Default to string
    return 'string'


def detect_identifier_pattern(series: pd.Series) -> Optional[str]:
    """Detect if field appears to be an identifier based on patterns."""
    non_null = series.dropna().astype(str)

    if len(non_null) == 0:
        return None

    # Sample up to 100 values
    sample = non_null.head(100)

    patterns = {
        'HGNC ID': r'^HGNC:\d+$',
        'MONDO ID': r'^MONDO:\d{7}$',
        'OMIM ID': r'^\d{6}$',
        'dbSNP rsID': r'^rs\d+$',
        'ClinVar ID': r'^VCV\d+$',
        'HGVS': r'^[A-Z]{2,3}_\d+\.\d+:',
        'Email': r'^[\w\.-]+@[\w\.-]+\.\w+$',
        'URL': r'^https?://',
        'UUID': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    }

    for pattern_name, regex in patterns.items():
        matches = sample.str.match(regex, case=False).sum()
        if matches / len(sample) > 0.8:  # 80% match threshold
            return pattern_name

    return None


def calculate_basic_stats(series: pd.Series) -> Dict[str, Any]:
    """Calculate basic statistics for any field."""
    total_count = len(series)
    null_count = series.isna().sum()
    non_null_count = total_count - null_count
    unique_count = series.nunique(dropna=True)

    return {
        'total_count': total_count,
        'non_null_count': non_null_count,
        'null_count': null_count,
        'null_percentage': (null_count / total_count * 100) if total_count > 0 else 0,
        'unique_count': unique_count,
        'cardinality': classify_cardinality(unique_count, non_null_count),
    }


def classify_cardinality(unique_count: int, non_null_count: int) -> str:
    """Classify cardinality as low, medium, high, or unique."""
    if unique_count == non_null_count:
        return 'unique'
    elif unique_count < 10:
        return 'low'
    elif unique_count < 1000:
        return 'medium'
    else:
        return 'high'


def calculate_string_stats(series: pd.Series) -> Dict[str, Any]:
    """Calculate statistics for string fields."""
    non_null = series.dropna().astype(str)

    if len(non_null) == 0:
        return {}

    lengths = non_null.str.len()

    # Top values
    value_counts = series.value_counts(dropna=True).head(10)
    top_values = [
        {
            'value': str(val),
            'count': int(count),
            'percentage': float(count / len(series) * 100)
        }
        for val, count in value_counts.items()
    ]

    return {
        'min_length': int(lengths.min()),
        'max_length': int(lengths.max()),
        'mean_length': float(lengths.mean()),
        'top_values': top_values,
        'pattern': detect_identifier_pattern(series),
    }


def calculate_numeric_stats(series: pd.Series) -> Dict[str, Any]:
    """Calculate statistics for numeric fields."""
    non_null = series.dropna()

    if len(non_null) == 0:
        return {}

    # Basic statistics
    stats = {
        'min': float(non_null.min()),
        'max': float(non_null.max()),
        'mean': float(non_null.mean()),
        'median': float(non_null.median()),
        'std': float(non_null.std()) if len(non_null) > 1 else 0,
        'q1': float(non_null.quantile(0.25)),
        'q3': float(non_null.quantile(0.75)),
    }

    # IQR and outliers
    iqr = stats['q3'] - stats['q1']
    lower_bound = stats['q1'] - 1.5 * iqr
    upper_bound = stats['q3'] + 1.5 * iqr

    outliers = non_null[(non_null < lower_bound) | (non_null > upper_bound)]

    stats['iqr'] = float(iqr)
    stats['outlier_count'] = len(outliers)
    stats['outlier_percentage'] = float(len(outliers) / len(non_null) * 100) if len(non_null) > 0 else 0

    # Distribution type (simple heuristic)
    skewness = float(non_null.skew()) if len(non_null) > 2 else 0
    if abs(skewness) < 0.5:
        distribution = 'normal'
    elif skewness > 0:
        distribution = 'skewed_right'
    else:
        distribution = 'skewed_left'

    stats['skewness'] = skewness
    stats['distribution_type'] = distribution

    return stats


def calculate_date_stats(series: pd.Series) -> Dict[str, Any]:
    """Calculate statistics for date fields."""
    # Try to convert to datetime
    try:
        dates = pd.to_datetime(series, errors='coerce').dropna()

        if len(dates) == 0:
            return {}

        return {
            'min_date': dates.min().isoformat(),
            'max_date': dates.max().isoformat(),
            'range_days': (dates.max() - dates.min()).days,
            'range_years': (dates.max() - dates.min()).days / 365.25,
        }
    except Exception:
        return {}


def calculate_boolean_stats(series: pd.Series) -> Dict[str, Any]:
    """Calculate statistics for boolean fields."""
    non_null = series.dropna()

    if len(non_null) == 0:
        return {}

    # Normalize to boolean
    true_values = {'true', '1', 'yes', 't', 'y'}
    bool_series = non_null.astype(str).str.lower().isin(true_values)

    true_count = bool_series.sum()
    false_count = len(bool_series) - true_count

    return {
        'true_count': int(true_count),
        'false_count': int(false_count),
        'true_percentage': float(true_count / len(bool_series) * 100) if len(bool_series) > 0 else 0,
    }


def analyze_field(series: pd.Series, field_name: str) -> Dict[str, Any]:
    """Comprehensive analysis of a single field."""
    # Basic stats
    stats = {
        'field_name': field_name,
        **calculate_basic_stats(series),
    }

    # Infer type
    data_type = infer_data_type(series)
    stats['data_type'] = data_type

    # Type-specific stats
    if data_type == 'string':
        stats.update(calculate_string_stats(series))
    elif data_type in ['integer', 'float']:
        stats.update(calculate_numeric_stats(series))
    elif data_type == 'date':
        stats.update(calculate_date_stats(series))
    elif data_type == 'boolean':
        stats.update(calculate_boolean_stats(series))

    return stats


def analyze_tabular_file(
    filepath: Path,
    sample_size: Optional[int] = None
) -> Dict[str, Any]:
    """
    Comprehensive analysis of a tabular file (CSV/TSV).

    Args:
        filepath: Path to the file
        sample_size: Optional number of rows to sample

    Returns:
        Dictionary containing analysis results
    """
    # Detect encoding and delimiter
    encoding = detect_encoding(filepath)
    delimiter = infer_delimiter(filepath, encoding)

    # Read file
    na_values = detect_null_values()

    if sample_size:
        df = pd.read_csv(
            filepath,
            sep=delimiter,
            encoding=encoding,
            na_values=na_values,
            nrows=sample_size,
            low_memory=False,
            on_bad_lines='warn',
            comment='#',
        )
    else:
        df = pd.read_csv(
            filepath,
            sep=delimiter,
            encoding=encoding,
            na_values=na_values,
            low_memory=False,
            on_bad_lines='warn',
            comment='#',
        )

    # File-level metadata
    file_stats = pd.DataFrame({
        'source': filepath.parent.parent.name,  # e.g., 'gencc' from 'data/sources/gencc'
        'filepath': str(filepath.relative_to(Path('data/sources'))),
        'filename': filepath.name,
        'file_size_mb': filepath.stat().st_size / (1024 * 1024),
        'row_count': len(df),
        'column_count': len(df.columns),
        'delimiter': delimiter,
        'encoding': encoding,
        'analyzed_date': datetime.now().isoformat(),
        'sample_size': sample_size,
    }, index=[0])

    # Analyze each field
    field_analyses = []
    for col in df.columns:
        field_stats = analyze_field(df[col], col)
        field_analyses.append(field_stats)

    return {
        'file_metadata': file_stats.to_dict('records')[0],
        'field_analyses': field_analyses,
    }
