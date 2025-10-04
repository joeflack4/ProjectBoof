"""Data dictionary export for all analyzed fields."""

from pathlib import Path
from typing import Dict, Any, List
import csv


def generate_data_dictionary(all_analyses: Dict[str, Dict[str, Any]],
                            output_path: Path) -> None:
    """
    Generate CSV data dictionary from all analyses.

    Args:
        all_analyses: Dictionary mapping source names to analysis results
        output_path: Path to save data dictionary CSV
    """
    rows = []

    for source_name, analysis_data in all_analyses.items():
        if 'field_analyses' not in analysis_data:
            continue

        for field in analysis_data['field_analyses']:
            row = {
                'source': source_name,
                'field_name': field.get('field_name', ''),
                'data_type': field.get('data_type', ''),
                'total_count': field.get('total_count', 0),
                'non_null_count': field.get('non_null_count', 0),
                'null_count': field.get('null_count', 0),
                'null_percentage': round(field.get('null_percentage', 0), 2),
                'unique_count': field.get('unique_count', 0),
                'cardinality': field.get('cardinality', ''),
                'pattern': field.get('pattern', ''),
            }

            # Add type-specific stats
            if 'min_length' in field:
                row['min_length'] = field['min_length']
                row['max_length'] = field['max_length']
                row['mean_length'] = round(field.get('mean_length', 0), 2)

            if 'min' in field:
                row['min_value'] = field['min']
                row['max_value'] = field['max']
                row['mean_value'] = round(field.get('mean', 0), 2)
                row['median_value'] = round(field.get('median', 0), 2)
                row['std_value'] = round(field.get('std', 0), 2)

            rows.append(row)

    # Determine all unique column names
    if not rows:
        return

    all_columns = set()
    for row in rows:
        all_columns.update(row.keys())

    columns = ['source', 'field_name', 'data_type', 'total_count', 'non_null_count',
               'null_count', 'null_percentage', 'unique_count', 'cardinality', 'pattern']

    # Add optional columns
    optional_cols = ['min_length', 'max_length', 'mean_length',
                    'min_value', 'max_value', 'mean_value', 'median_value', 'std_value']
    for col in optional_cols:
        if col in all_columns:
            columns.append(col)

    # Write CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
