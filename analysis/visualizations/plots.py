"""Visualization generation using matplotlib."""

from pathlib import Path
from typing import Dict, Any, List
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np


def plot_null_percentages(analysis_data: Dict[str, Any], output_path: Path) -> None:
    """
    Generate bar chart of null percentages for all fields.

    Args:
        analysis_data: Analysis results with field_analyses
        output_path: Path to save plot image
    """
    if 'field_analyses' not in analysis_data:
        return

    fields = analysis_data['field_analyses']
    if not fields:
        return

    # Extract data
    field_names = [f.get('field_name', '')[:30] for f in fields]  # Truncate long names
    null_pcts = [f.get('null_percentage', 0) for f in fields]

    # Create plot
    fig, ax = plt.subplots(figsize=(12, max(6, len(fields) * 0.3)))

    y_pos = np.arange(len(field_names))
    ax.barh(y_pos, null_pcts, color='steelblue')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(field_names)
    ax.set_xlabel('Null Percentage (%)')
    ax.set_title('Field Null Percentages')
    ax.set_xlim(0, 100)

    # Add grid
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close()


def plot_cardinality_distribution(analysis_data: Dict[str, Any],
                                  output_path: Path) -> None:
    """
    Generate pie chart of cardinality distribution.

    Args:
        analysis_data: Analysis results with field_analyses
        output_path: Path to save plot image
    """
    if 'field_analyses' not in analysis_data:
        return

    fields = analysis_data['field_analyses']
    if not fields:
        return

    # Count cardinality types
    cardinality_counts = {}
    for field in fields:
        card = field.get('cardinality', 'unknown')
        cardinality_counts[card] = cardinality_counts.get(card, 0) + 1

    # Create plot
    fig, ax = plt.subplots(figsize=(8, 6))

    labels = list(cardinality_counts.keys())
    sizes = list(cardinality_counts.values())
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']

    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)],
           startangle=90)
    ax.set_title('Field Cardinality Distribution')

    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close()


def plot_data_type_distribution(analysis_data: Dict[str, Any],
                                output_path: Path) -> None:
    """
    Generate bar chart of data type distribution.

    Args:
        analysis_data: Analysis results with field_analyses
        output_path: Path to save plot image
    """
    if 'field_analyses' not in analysis_data:
        return

    fields = analysis_data['field_analyses']
    if not fields:
        return

    # Count data types
    type_counts = {}
    for field in fields:
        dtype = field.get('data_type', 'unknown')
        type_counts[dtype] = type_counts.get(dtype, 0) + 1

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))

    types = list(type_counts.keys())
    counts = list(type_counts.values())

    ax.bar(types, counts, color='coral')
    ax.set_xlabel('Data Type')
    ax.set_ylabel('Count')
    ax.set_title('Field Data Type Distribution')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close()


def plot_numeric_histogram(field_data: Dict[str, Any], output_path: Path) -> None:
    """
    Generate histogram for a numeric field.

    Args:
        field_data: Field analysis data with numeric stats
        output_path: Path to save plot image
    """
    # Note: This is a placeholder - actual histogram would need raw data
    # For now, just show summary stats as a text plot

    if 'min' not in field_data:
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    stats_text = f"""
    Field: {field_data.get('field_name', 'Unknown')}

    Min: {field_data.get('min', 0):.2f}
    Max: {field_data.get('max', 0):.2f}
    Mean: {field_data.get('mean', 0):.2f}
    Median: {field_data.get('median', 0):.2f}
    Std Dev: {field_data.get('std', 0):.2f}
    Q1: {field_data.get('q1', 0):.2f}
    Q3: {field_data.get('q3', 0):.2f}
    """

    ax.text(0.5, 0.5, stats_text, ha='center', va='center',
           fontsize=12, fontfamily='monospace')
    ax.set_title(f"Numeric Summary: {field_data.get('field_name', 'Unknown')}")
    ax.axis('off')

    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close()


def generate_all_plots(analysis_data: Dict[str, Any], output_dir: Path) -> None:
    """
    Generate all standard plots for an analysis.

    Args:
        analysis_data: Analysis results
        output_dir: Directory to save plots
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate plots
    plot_null_percentages(analysis_data, output_dir / 'null_percentages.png')
    plot_cardinality_distribution(analysis_data, output_dir / 'cardinality_distribution.png')
    plot_data_type_distribution(analysis_data, output_dir / 'data_type_distribution.png')
