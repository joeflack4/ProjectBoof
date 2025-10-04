"""Cross-source analysis for entity extraction and field mapping."""

from pathlib import Path
from typing import Dict, Any, List, Set, Optional
import re
from collections import defaultdict, Counter
from difflib import SequenceMatcher


def extract_genes(analysis_data: Dict[str, Any]) -> Dict[str, Set[str]]:
    """
    Extract gene identifiers from analysis data.

    Args:
        analysis_data: Dictionary with field-level statistics

    Returns:
        Dictionary with 'symbols' and 'hgnc_ids' sets
    """
    genes = {
        'symbols': set(),
        'hgnc_ids': set()
    }

    if 'field_analyses' not in analysis_data:
        return genes

    for field_analysis in analysis_data['field_analyses']:
        field_name = field_analysis.get('field_name', '').lower()
        pattern = field_analysis.get('pattern')

        # Look for HGNC ID fields
        if pattern == 'HGNC ID':
            # Get top values if available
            if 'top_values' in field_analysis:
                for val_info in field_analysis['top_values']:
                    value = val_info['value']
                    if value and value.startswith('HGNC:'):
                        genes['hgnc_ids'].add(value)

        # Look for gene symbol fields
        if any(term in field_name for term in ['gene', 'symbol', 'hgnc']):
            if 'top_values' in field_analysis:
                for val_info in field_analysis['top_values']:
                    value = val_info['value']
                    # Simple heuristic: gene symbols are uppercase, 1-20 chars, alphanumeric
                    if value and value.isupper() and 1 <= len(value) <= 20:
                        if re.match(r'^[A-Z0-9-]+$', value):
                            genes['symbols'].add(value)

    return genes


def extract_diseases(analysis_data: Dict[str, Any]) -> Dict[str, Set[str]]:
    """
    Extract disease identifiers from analysis data.

    Args:
        analysis_data: Dictionary with field-level statistics

    Returns:
        Dictionary with 'names', 'mondo_ids', and 'omim_ids' sets
    """
    diseases = {
        'names': set(),
        'mondo_ids': set(),
        'omim_ids': set()
    }

    if 'field_analyses' not in analysis_data:
        return diseases

    for field_analysis in analysis_data['field_analyses']:
        field_name = field_analysis.get('field_name', '').lower()
        pattern = field_analysis.get('pattern')

        # Look for MONDO ID fields
        if pattern == 'MONDO ID':
            if 'top_values' in field_analysis:
                for val_info in field_analysis['top_values']:
                    value = val_info['value']
                    if value and value.startswith('MONDO:'):
                        diseases['mondo_ids'].add(value)

        # Look for OMIM ID fields
        if pattern == 'OMIM ID':
            if 'top_values' in field_analysis:
                for val_info in field_analysis['top_values']:
                    value = val_info['value']
                    if value and re.match(r'^\d{6}$', value):
                        diseases['omim_ids'].add(value)

        # Look for disease name fields
        if any(term in field_name for term in ['disease', 'phenotype', 'condition', 'diagnosis']):
            if 'top_values' in field_analysis:
                for val_info in field_analysis['top_values']:
                    value = val_info['value']
                    # Disease names are typically longer phrases
                    if value and len(value) > 3 and not value.startswith(('MONDO:', 'OMIM:')):
                        diseases['names'].add(value)

    return diseases


def extract_variants(analysis_data: Dict[str, Any]) -> Dict[str, Set[str]]:
    """
    Extract variant identifiers from analysis data.

    Args:
        analysis_data: Dictionary with field-level statistics

    Returns:
        Dictionary with 'dbsnp_ids', 'clinvar_ids', and 'hgvs' sets
    """
    variants = {
        'dbsnp_ids': set(),
        'clinvar_ids': set(),
        'hgvs': set()
    }

    if 'field_analyses' not in analysis_data:
        return variants

    for field_analysis in analysis_data['field_analyses']:
        pattern = field_analysis.get('pattern')

        # Look for dbSNP rs IDs
        if pattern == 'dbSNP rsID':
            if 'top_values' in field_analysis:
                for val_info in field_analysis['top_values']:
                    value = val_info['value']
                    if value and value.startswith('rs'):
                        variants['dbsnp_ids'].add(value)

        # Look for ClinVar IDs
        if pattern == 'ClinVar ID':
            if 'top_values' in field_analysis:
                for val_info in field_analysis['top_values']:
                    value = val_info['value']
                    if value and value.startswith('VCV'):
                        variants['clinvar_ids'].add(value)

        # Look for HGVS notation
        if pattern == 'HGVS':
            if 'top_values' in field_analysis:
                for val_info in field_analysis['top_values']:
                    value = val_info['value']
                    if value:
                        variants['hgvs'].add(value)

    return variants


def calculate_overlap(entity_sets: Dict[str, Set[str]]) -> Dict[str, Any]:
    """
    Calculate overlap statistics for entity sets.

    Args:
        entity_sets: Dictionary mapping source names to sets of entities

    Returns:
        Overlap statistics including counts and intersection data
    """
    sources = list(entity_sets.keys())

    # Calculate pairwise overlaps
    overlaps = {}
    for i, source1 in enumerate(sources):
        for source2 in sources[i+1:]:
            set1 = entity_sets[source1]
            set2 = entity_sets[source2]

            intersection = set1 & set2
            union = set1 | set2

            overlap_key = f"{source1}_vs_{source2}"
            overlaps[overlap_key] = {
                'source1': source1,
                'source2': source2,
                'source1_count': len(set1),
                'source2_count': len(set2),
                'intersection_count': len(intersection),
                'union_count': len(union),
                'jaccard_similarity': len(intersection) / len(union) if union else 0,
                'overlap_percentage_1': (len(intersection) / len(set1) * 100) if set1 else 0,
                'overlap_percentage_2': (len(intersection) / len(set2) * 100) if set2 else 0,
            }

    # Calculate overall statistics
    all_entities = set()
    for entity_set in entity_sets.values():
        all_entities.update(entity_set)

    source_counts = {source: len(entities) for source, entities in entity_sets.items()}

    return {
        'total_unique_entities': len(all_entities),
        'source_counts': source_counts,
        'pairwise_overlaps': overlaps,
    }


def calculate_field_name_similarity(name1: str, name2: str) -> float:
    """
    Calculate similarity between two field names.

    Args:
        name1: First field name
        name2: Second field name

    Returns:
        Similarity score (0-1)
    """
    # Normalize field names
    norm1 = name1.lower().replace('_', ' ').replace('-', ' ')
    norm2 = name2.lower().replace('_', ' ').replace('-', ' ')

    # Use SequenceMatcher for fuzzy matching
    return SequenceMatcher(None, norm1, norm2).ratio()


def suggest_field_mappings(sources_data: Dict[str, Dict[str, Any]],
                          similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
    """
    Suggest field mappings across sources based on name similarity and data type.

    Args:
        sources_data: Dictionary mapping source names to analysis data
        similarity_threshold: Minimum similarity score for suggesting mapping

    Returns:
        List of suggested field mappings
    """
    mappings = []

    # Extract all fields from all sources
    source_fields = {}
    for source_name, analysis_data in sources_data.items():
        if 'field_analyses' not in analysis_data:
            continue

        fields = {}
        for field_analysis in analysis_data['field_analyses']:
            field_name = field_analysis.get('field_name')
            if field_name:
                fields[field_name] = {
                    'data_type': field_analysis.get('data_type'),
                    'pattern': field_analysis.get('pattern'),
                    'cardinality': field_analysis.get('cardinality'),
                }
        source_fields[source_name] = fields

    # Compare fields across sources
    sources = list(source_fields.keys())
    for i, source1 in enumerate(sources):
        for source2 in sources[i+1:]:
            fields1 = source_fields[source1]
            fields2 = source_fields[source2]

            for field1_name, field1_info in fields1.items():
                for field2_name, field2_info in fields2.items():
                    # Calculate name similarity
                    similarity = calculate_field_name_similarity(field1_name, field2_name)

                    if similarity >= similarity_threshold:
                        # Check if data types are compatible
                        type_compatible = field1_info['data_type'] == field2_info['data_type']
                        pattern_match = field1_info.get('pattern') == field2_info.get('pattern')

                        confidence = 'high' if similarity >= 0.9 and type_compatible else \
                                   'medium' if similarity >= 0.8 and type_compatible else 'low'

                        mappings.append({
                            'source1': source1,
                            'field1': field1_name,
                            'source2': source2,
                            'field2': field2_name,
                            'similarity': similarity,
                            'type_compatible': type_compatible,
                            'pattern_match': pattern_match,
                            'confidence': confidence,
                            'type1': field1_info['data_type'],
                            'type2': field2_info['data_type'],
                        })

    # Sort by similarity descending
    mappings.sort(key=lambda x: x['similarity'], reverse=True)

    return mappings


def analyze_identifier_coverage(sources_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze identifier coverage across sources.

    Args:
        sources_data: Dictionary mapping source names to analysis data

    Returns:
        Coverage matrix for different identifier types
    """
    coverage = {
        'hgnc_ids': {},
        'mondo_ids': {},
        'omim_ids': {},
        'dbsnp_ids': {},
        'clinvar_ids': {},
    }

    for source_name, analysis_data in sources_data.items():
        if 'field_analyses' not in analysis_data:
            continue

        # Check which identifier types are present
        identifier_types = set()
        for field_analysis in analysis_data['field_analyses']:
            pattern = field_analysis.get('pattern')
            if pattern == 'HGNC ID':
                identifier_types.add('hgnc_ids')
            elif pattern == 'MONDO ID':
                identifier_types.add('mondo_ids')
            elif pattern == 'OMIM ID':
                identifier_types.add('omim_ids')
            elif pattern == 'dbSNP rsID':
                identifier_types.add('dbsnp_ids')
            elif pattern == 'ClinVar ID':
                identifier_types.add('clinvar_ids')

        # Record presence for each type
        for id_type in coverage.keys():
            coverage[id_type][source_name] = id_type in identifier_types

    return coverage


def analyze_cross_source(sources_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Main entry point for cross-source analysis.

    Args:
        sources_data: Dictionary mapping source names to analysis data

    Returns:
        Complete cross-source analysis results
    """
    # Extract entities from each source
    all_genes = {}
    all_diseases = {}
    all_variants = {}

    for source_name, analysis_data in sources_data.items():
        all_genes[source_name] = extract_genes(analysis_data)
        all_diseases[source_name] = extract_diseases(analysis_data)
        all_variants[source_name] = extract_variants(analysis_data)

    # Calculate overlaps for gene symbols
    gene_symbol_sets = {
        source: genes['symbols']
        for source, genes in all_genes.items()
        if genes['symbols']
    }
    gene_overlap = calculate_overlap(gene_symbol_sets) if gene_symbol_sets else {}

    # Calculate overlaps for disease names
    disease_name_sets = {
        source: diseases['names']
        for source, diseases in all_diseases.items()
        if diseases['names']
    }
    disease_overlap = calculate_overlap(disease_name_sets) if disease_name_sets else {}

    # Suggest field mappings
    field_mappings = suggest_field_mappings(sources_data)

    # Analyze identifier coverage
    identifier_coverage = analyze_identifier_coverage(sources_data)

    return {
        'gene_overlap': gene_overlap,
        'disease_overlap': disease_overlap,
        'field_mappings': field_mappings[:50],  # Top 50 mappings
        'identifier_coverage': identifier_coverage,
        'sources_analyzed': list(sources_data.keys()),
    }
