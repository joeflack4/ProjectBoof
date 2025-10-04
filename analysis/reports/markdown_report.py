"""Markdown report generation for analysis results."""

from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


def generate_markdown_report(analysis_data: Dict[str, Any], output_path: Path) -> None:
    """
    Generate markdown report from analysis data.

    Args:
        analysis_data: Analysis results dictionary
        output_path: Path to save markdown report
    """
    lines = []

    # Header
    filename = analysis_data.get('filename', 'Unknown')
    lines.append(f"# Data Analysis Report: {filename}\n")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("---\n")

    # File metadata
    lines.append("## File Information\n")
    lines.append(f"- **File**: {analysis_data.get('filepath', 'N/A')}")
    lines.append(f"- **Size**: {analysis_data.get('file_size_mb', 0):.2f} MB")

    if 'row_count' in analysis_data:
        # Tabular data
        lines.append(f"- **Rows**: {analysis_data.get('row_count', 0):,}")
        lines.append(f"- **Columns**: {analysis_data.get('column_count', 0)}")
        lines.append(f"- **Delimiter**: `{analysis_data.get('delimiter', 'N/A')}`")
        lines.append(f"- **Encoding**: {analysis_data.get('encoding', 'N/A')}")
    elif 'format' in analysis_data:
        # Semi-structured data
        lines.append(f"- **Format**: {analysis_data.get('format', 'N/A')}")
        lines.append(f"- **Max Depth**: {analysis_data.get('max_depth', 0)}")
        lines.append(f"- **Node Count**: {analysis_data.get('node_count', 0):,}")
        lines.append(f"- **Unique Paths**: {analysis_data.get('unique_paths', 0)}")

    lines.append("")

    # Field-level analysis for tabular data
    if 'field_analyses' in analysis_data:
        lines.append("## Field Analysis\n")
        lines.append(f"Total fields: **{len(analysis_data['field_analyses'])}**\n")

        for field in analysis_data['field_analyses']:
            field_name = field.get('field_name', 'Unknown')
            lines.append(f"### {field_name}\n")
            lines.append(f"- **Type**: {field.get('data_type', 'unknown')}")
            lines.append(f"- **Non-null**: {field.get('non_null_count', 0):,} / {field.get('total_count', 0):,} ({100 - field.get('null_percentage', 0):.1f}%)")
            lines.append(f"- **Unique values**: {field.get('unique_count', 0):,}")
            lines.append(f"- **Cardinality**: {field.get('cardinality', 'N/A')}")

            if field.get('pattern'):
                lines.append(f"- **Pattern**: {field['pattern']}")

            # String stats
            if 'min_length' in field:
                lines.append(f"- **Length**: {field['min_length']}-{field['max_length']} chars (avg: {field.get('mean_length', 0):.1f})")

            # Numeric stats
            if 'min' in field:
                lines.append(f"- **Range**: {field['min']:.2f} - {field['max']:.2f}")
                lines.append(f"- **Mean**: {field.get('mean', 0):.2f} (±{field.get('std', 0):.2f})")
                lines.append(f"- **Median**: {field.get('median', 0):.2f}")

            # Top values
            if 'top_values' in field and field['top_values']:
                lines.append("- **Top values**:")
                for val in field['top_values'][:5]:
                    lines.append(f"  - `{val['value']}`: {val['count']:,} ({val['percentage']:.1f}%)")

            lines.append("")

    # Structure analysis for semi-structured data
    if 'paths' in analysis_data:
        lines.append("## Structure Analysis\n")
        paths = analysis_data['paths'][:20]  # Top 20 paths
        lines.append("### Top Paths\n")
        for path in paths:
            lines.append(f"- `{path}`")
        lines.append("")

        if len(analysis_data['paths']) > 20:
            lines.append(f"*...and {len(analysis_data['paths']) - 20} more paths*\n")

    # Write report
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def generate_summary_markdown(all_analyses: Dict[str, Dict[str, Any]],
                              output_path: Path) -> None:
    """
    Generate summary markdown report combining multiple analyses.

    Args:
        all_analyses: Dictionary mapping source names to analysis results
        output_path: Path to save summary markdown
    """
    lines = []

    lines.append("# Data Analysis Summary\n")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Sources analyzed**: {len(all_analyses)}\n")
    lines.append("---\n")

    # Overview table
    lines.append("## Overview\n")
    lines.append("| Source | Type | Size (MB) | Rows/Nodes | Columns/Paths |")
    lines.append("|--------|------|-----------|------------|---------------|")

    for source_name, analysis_data in sorted(all_analyses.items()):
        file_type = 'Tabular' if 'row_count' in analysis_data else 'Semi-structured'
        size = analysis_data.get('file_size_mb', 0)

        if 'row_count' in analysis_data:
            rows = f"{analysis_data.get('row_count', 0):,}"
            cols = f"{analysis_data.get('column_count', 0)}"
        else:
            rows = f"{analysis_data.get('node_count', 0):,}"
            cols = f"{analysis_data.get('unique_paths', 0)}"

        lines.append(f"| {source_name} | {file_type} | {size:.1f} | {rows} | {cols} |")

    lines.append("")

    # Individual summaries
    lines.append("## Source Details\n")
    for source_name, analysis_data in sorted(all_analyses.items()):
        lines.append(f"### {source_name}\n")
        lines.append(f"- **File**: `{analysis_data.get('filepath', 'N/A')}`")
        lines.append(f"- **Size**: {analysis_data.get('file_size_mb', 0):.2f} MB")

        if 'row_count' in analysis_data:
            lines.append(f"- **Rows**: {analysis_data.get('row_count', 0):,}")
            lines.append(f"- **Columns**: {analysis_data.get('column_count', 0)}")
        elif 'format' in analysis_data:
            lines.append(f"- **Format**: {analysis_data.get('format', 'N/A')}")
            lines.append(f"- **Max Depth**: {analysis_data.get('max_depth', 0)}")

        lines.append("")

    # Write report
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
