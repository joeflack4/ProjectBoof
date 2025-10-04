"""Tests for cross-source analysis."""

import pytest
from analysis.core.cross_source import (
    extract_genes,
    extract_diseases,
    extract_variants,
    calculate_overlap,
    calculate_field_name_similarity,
    suggest_field_mappings,
    analyze_identifier_coverage,
    analyze_cross_source,
)


class TestExtractGenes:
    """Test gene extraction."""

    def test_extract_hgnc_ids(self):
        """Test extraction of HGNC IDs."""
        analysis_data = {
            'field_analyses': [
                {
                    'field_name': 'gene_id',
                    'pattern': 'HGNC ID',
                    'top_values': [
                        {'value': 'HGNC:1234', 'count': 10},
                        {'value': 'HGNC:5678', 'count': 5},
                    ]
                }
            ]
        }

        genes = extract_genes(analysis_data)

        assert 'HGNC:1234' in genes['hgnc_ids']
        assert 'HGNC:5678' in genes['hgnc_ids']

    def test_extract_gene_symbols(self):
        """Test extraction of gene symbols."""
        analysis_data = {
            'field_analyses': [
                {
                    'field_name': 'gene_symbol',
                    'top_values': [
                        {'value': 'BRCA1', 'count': 100},
                        {'value': 'TP53', 'count': 50},
                        {'value': 'invalid', 'count': 10},  # lowercase, should be ignored
                    ]
                }
            ]
        }

        genes = extract_genes(analysis_data)

        assert 'BRCA1' in genes['symbols']
        assert 'TP53' in genes['symbols']
        assert 'invalid' not in genes['symbols']

    def test_extract_genes_empty(self):
        """Test gene extraction with no data."""
        analysis_data = {'field_analyses': []}
        genes = extract_genes(analysis_data)

        assert len(genes['symbols']) == 0
        assert len(genes['hgnc_ids']) == 0


class TestExtractDiseases:
    """Test disease extraction."""

    def test_extract_mondo_ids(self):
        """Test extraction of MONDO IDs."""
        analysis_data = {
            'field_analyses': [
                {
                    'field_name': 'disease_id',
                    'pattern': 'MONDO ID',
                    'top_values': [
                        {'value': 'MONDO:0000001', 'count': 10},
                        {'value': 'MONDO:0000002', 'count': 5},
                    ]
                }
            ]
        }

        diseases = extract_diseases(analysis_data)

        assert 'MONDO:0000001' in diseases['mondo_ids']
        assert 'MONDO:0000002' in diseases['mondo_ids']

    def test_extract_omim_ids(self):
        """Test extraction of OMIM IDs."""
        analysis_data = {
            'field_analyses': [
                {
                    'field_name': 'omim',
                    'pattern': 'OMIM ID',
                    'top_values': [
                        {'value': '123456', 'count': 10},
                        {'value': '654321', 'count': 5},
                    ]
                }
            ]
        }

        diseases = extract_diseases(analysis_data)

        assert '123456' in diseases['omim_ids']
        assert '654321' in diseases['omim_ids']

    def test_extract_disease_names(self):
        """Test extraction of disease names."""
        analysis_data = {
            'field_analyses': [
                {
                    'field_name': 'disease_name',
                    'top_values': [
                        {'value': 'Breast Cancer', 'count': 100},
                        {'value': 'Lung Cancer', 'count': 50},
                    ]
                }
            ]
        }

        diseases = extract_diseases(analysis_data)

        assert 'Breast Cancer' in diseases['names']
        assert 'Lung Cancer' in diseases['names']


class TestExtractVariants:
    """Test variant extraction."""

    def test_extract_dbsnp_ids(self):
        """Test extraction of dbSNP IDs."""
        analysis_data = {
            'field_analyses': [
                {
                    'field_name': 'variant_id',
                    'pattern': 'dbSNP rsID',
                    'top_values': [
                        {'value': 'rs123456', 'count': 10},
                        {'value': 'rs789012', 'count': 5},
                    ]
                }
            ]
        }

        variants = extract_variants(analysis_data)

        assert 'rs123456' in variants['dbsnp_ids']
        assert 'rs789012' in variants['dbsnp_ids']

    def test_extract_clinvar_ids(self):
        """Test extraction of ClinVar IDs."""
        analysis_data = {
            'field_analyses': [
                {
                    'field_name': 'clinvar_id',
                    'pattern': 'ClinVar ID',
                    'top_values': [
                        {'value': 'VCV000001', 'count': 10},
                        {'value': 'VCV000002', 'count': 5},
                    ]
                }
            ]
        }

        variants = extract_variants(analysis_data)

        assert 'VCV000001' in variants['clinvar_ids']
        assert 'VCV000002' in variants['clinvar_ids']


class TestCalculateOverlap:
    """Test overlap calculation."""

    def test_overlap_two_sets(self):
        """Test overlap calculation for two sets."""
        entity_sets = {
            'source1': {'A', 'B', 'C'},
            'source2': {'B', 'C', 'D'},
        }

        overlap = calculate_overlap(entity_sets)

        assert overlap['total_unique_entities'] == 4  # A, B, C, D
        assert overlap['source_counts']['source1'] == 3
        assert overlap['source_counts']['source2'] == 3

        pairwise = overlap['pairwise_overlaps']['source1_vs_source2']
        assert pairwise['intersection_count'] == 2  # B, C
        assert pairwise['union_count'] == 4  # A, B, C, D
        assert pairwise['jaccard_similarity'] == 0.5  # 2/4

    def test_overlap_no_intersection(self):
        """Test overlap with no common elements."""
        entity_sets = {
            'source1': {'A', 'B'},
            'source2': {'C', 'D'},
        }

        overlap = calculate_overlap(entity_sets)

        pairwise = overlap['pairwise_overlaps']['source1_vs_source2']
        assert pairwise['intersection_count'] == 0
        assert pairwise['jaccard_similarity'] == 0

    def test_overlap_complete_intersection(self):
        """Test overlap with complete intersection."""
        entity_sets = {
            'source1': {'A', 'B'},
            'source2': {'A', 'B'},
        }

        overlap = calculate_overlap(entity_sets)

        pairwise = overlap['pairwise_overlaps']['source1_vs_source2']
        assert pairwise['intersection_count'] == 2
        assert pairwise['jaccard_similarity'] == 1.0


class TestFieldNameSimilarity:
    """Test field name similarity calculation."""

    def test_exact_match(self):
        """Test exact match."""
        similarity = calculate_field_name_similarity('gene_name', 'gene_name')
        assert similarity == 1.0

    def test_case_insensitive(self):
        """Test case insensitive matching."""
        similarity = calculate_field_name_similarity('Gene_Name', 'gene_name')
        assert similarity == 1.0

    def test_underscore_vs_dash(self):
        """Test underscore vs dash normalization."""
        similarity = calculate_field_name_similarity('gene_name', 'gene-name')
        assert similarity == 1.0

    def test_partial_match(self):
        """Test partial match."""
        similarity = calculate_field_name_similarity('gene_symbol', 'gene_name')
        assert 0 < similarity < 1

    def test_no_match(self):
        """Test completely different names."""
        similarity = calculate_field_name_similarity('gene', 'disease')
        assert similarity < 0.5


class TestSuggestFieldMappings:
    """Test field mapping suggestions."""

    def test_suggest_high_similarity_mappings(self):
        """Test suggesting mappings for highly similar field names."""
        sources_data = {
            'source1': {
                'field_analyses': [
                    {'field_name': 'gene_symbol', 'data_type': 'string', 'cardinality': 'high'}
                ]
            },
            'source2': {
                'field_analyses': [
                    {'field_name': 'gene_symbol', 'data_type': 'string', 'cardinality': 'high'}
                ]
            }
        }

        mappings = suggest_field_mappings(sources_data, similarity_threshold=0.7)

        assert len(mappings) > 0
        assert mappings[0]['field1'] == 'gene_symbol'
        assert mappings[0]['field2'] == 'gene_symbol'
        assert mappings[0]['type_compatible'] is True
        assert mappings[0]['similarity'] == 1.0

    def test_filter_by_threshold(self):
        """Test that low similarity mappings are filtered."""
        sources_data = {
            'source1': {
                'field_analyses': [
                    {'field_name': 'gene', 'data_type': 'string', 'cardinality': 'high'}
                ]
            },
            'source2': {
                'field_analyses': [
                    {'field_name': 'disease', 'data_type': 'string', 'cardinality': 'high'}
                ]
            }
        }

        mappings = suggest_field_mappings(sources_data, similarity_threshold=0.8)

        # Should have no mappings since gene/disease similarity is low
        assert len(mappings) == 0


class TestAnalyzeIdentifierCoverage:
    """Test identifier coverage analysis."""

    def test_identify_coverage(self):
        """Test identifier coverage detection."""
        sources_data = {
            'source1': {
                'field_analyses': [
                    {'field_name': 'hgnc_id', 'pattern': 'HGNC ID'},
                    {'field_name': 'mondo_id', 'pattern': 'MONDO ID'},
                ]
            },
            'source2': {
                'field_analyses': [
                    {'field_name': 'hgnc_id', 'pattern': 'HGNC ID'},
                    {'field_name': 'dbsnp_id', 'pattern': 'dbSNP rsID'},
                ]
            }
        }

        coverage = analyze_identifier_coverage(sources_data)

        assert coverage['hgnc_ids']['source1'] is True
        assert coverage['hgnc_ids']['source2'] is True
        assert coverage['mondo_ids']['source1'] is True
        assert coverage['mondo_ids']['source2'] is False
        assert coverage['dbsnp_ids']['source1'] is False
        assert coverage['dbsnp_ids']['source2'] is True


class TestAnalyzeCrossSource:
    """Test complete cross-source analysis."""

    def test_analyze_cross_source(self):
        """Test end-to-end cross-source analysis."""
        sources_data = {
            'source1': {
                'field_analyses': [
                    {
                        'field_name': 'gene_symbol',
                        'data_type': 'string',
                        'cardinality': 'high',
                        'top_values': [
                            {'value': 'BRCA1', 'count': 10},
                            {'value': 'TP53', 'count': 5},
                        ]
                    },
                    {
                        'field_name': 'hgnc_id',
                        'pattern': 'HGNC ID',
                        'top_values': [
                            {'value': 'HGNC:1234', 'count': 10},
                        ]
                    }
                ]
            },
            'source2': {
                'field_analyses': [
                    {
                        'field_name': 'gene_name',
                        'data_type': 'string',
                        'cardinality': 'high',
                        'top_values': [
                            {'value': 'BRCA1', 'count': 20},
                            {'value': 'EGFR', 'count': 10},
                        ]
                    }
                ]
            }
        }

        result = analyze_cross_source(sources_data)

        assert 'gene_overlap' in result
        assert 'field_mappings' in result
        assert 'identifier_coverage' in result
        assert result['sources_analyzed'] == ['source1', 'source2']

        # Check gene overlap - both sources have BRCA1
        if result['gene_overlap']:
            assert result['gene_overlap']['total_unique_entities'] >= 1
