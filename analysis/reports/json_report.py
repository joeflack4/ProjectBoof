"""JSON report generation for analysis results."""

from pathlib import Path
from typing import Dict, Any
import json
from datetime import datetime


def generate_json_report(analysis_data: Dict[str, Any], output_path: Path) -> None:
    """
    Generate JSON report from analysis data.

    Args:
        analysis_data: Analysis results dictionary
        output_path: Path to save JSON report
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, default=str)


def generate_summary_json(all_analyses: Dict[str, Dict[str, Any]],
                         output_path: Path) -> None:
    """
    Generate summary JSON report combining multiple analyses.

    Args:
        all_analyses: Dictionary mapping source names to analysis results
        output_path: Path to save summary JSON
    """
    summary = {
        'generated_at': datetime.now().isoformat(),
        'total_sources': len(all_analyses),
        'sources': {}
    }

    for source_name, analysis_data in all_analyses.items():
        source_summary = {
            'filepath': analysis_data.get('filepath', ''),
            'file_size_mb': analysis_data.get('file_size_mb', 0),
        }

        # Tabular data summary
        if 'row_count' in analysis_data:
            source_summary['row_count'] = analysis_data['row_count']
            source_summary['column_count'] = analysis_data['column_count']
            source_summary['encoding'] = analysis_data.get('encoding', '')

        # Semi-structured summary
        if 'format' in analysis_data:
            source_summary['format'] = analysis_data['format']
            source_summary['max_depth'] = analysis_data.get('max_depth', 0)
            source_summary['node_count'] = analysis_data.get('node_count', 0)

        summary['sources'][source_name] = source_summary

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
