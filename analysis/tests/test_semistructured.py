"""Tests for semi-structured data analysis engine."""

import pytest
import json
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from analysis.core.semistructured import (
    parse_json,
    parse_xml,
    extract_json_paths,
    extract_xml_paths,
    calculate_json_depth,
    calculate_xml_depth,
    count_nodes,
    count_xml_nodes,
    infer_json_schema,
    analyze_json_structure,
    analyze_xml_structure,
    analyze_semistructured_file,
)


class TestParseJSON:
    """Test JSON parsing."""

    def test_parse_simple_json(self):
        """Test parsing simple JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"key": "value", "number": 42}, f)
            temp_path = f.name

        try:
            data = parse_json(Path(temp_path))
            assert data == {"key": "value", "number": 42}
        finally:
            Path(temp_path).unlink()

    def test_parse_nested_json(self):
        """Test parsing nested JSON."""
        nested = {"outer": {"inner": {"deep": "value"}}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(nested, f)
            temp_path = f.name

        try:
            data = parse_json(Path(temp_path))
            assert data["outer"]["inner"]["deep"] == "value"
        finally:
            Path(temp_path).unlink()


class TestParseXML:
    """Test XML parsing."""

    def test_parse_simple_xml(self):
        """Test parsing simple XML file."""
        xml_content = '<?xml version="1.0"?><root><item>value</item></root>'
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(xml_content)
            temp_path = f.name

        try:
            root = parse_xml(Path(temp_path))
            assert root.tag == 'root'
            assert root.find('item').text == 'value'
        finally:
            Path(temp_path).unlink()


class TestExtractJSONPaths:
    """Test JSON path extraction."""

    def test_simple_object_paths(self):
        """Test paths from simple object."""
        data = {"name": "test", "age": 25}
        paths = extract_json_paths(data)

        assert "name" in paths
        assert "age" in paths

    def test_nested_object_paths(self):
        """Test paths from nested object."""
        data = {"person": {"name": "test", "address": {"city": "NYC"}}}
        paths = extract_json_paths(data)

        assert "person" in paths
        assert "person.name" in paths
        assert "person.address" in paths
        assert "person.address.city" in paths

    def test_array_paths(self):
        """Test paths with arrays."""
        data = {"items": [{"id": 1}, {"id": 2}]}
        paths = extract_json_paths(data)

        assert "items" in paths
        assert "items[]" in paths
        assert "items[].id" in paths


class TestExtractXMLPaths:
    """Test XML path extraction."""

    def test_simple_xml_paths(self):
        """Test paths from simple XML."""
        xml_content = '<root><item>value</item></root>'
        root = ET.fromstring(xml_content)
        paths = extract_xml_paths(root)

        assert "root" in paths
        assert "root/item" in paths

    def test_nested_xml_paths(self):
        """Test paths from nested XML."""
        xml_content = '<root><person><name>test</name><age>25</age></person></root>'
        root = ET.fromstring(xml_content)
        paths = extract_xml_paths(root)

        assert "root" in paths
        assert "root/person" in paths
        assert "root/person/name" in paths
        assert "root/person/age" in paths


class TestCalculateDepth:
    """Test depth calculation."""

    def test_json_depth_flat(self):
        """Test JSON depth for flat structure."""
        data = {"a": 1, "b": 2}
        assert calculate_json_depth(data) == 1

    def test_json_depth_nested(self):
        """Test JSON depth for nested structure."""
        data = {"a": {"b": {"c": {"d": 1}}}}
        assert calculate_json_depth(data) == 4

    def test_xml_depth_flat(self):
        """Test XML depth for flat structure."""
        xml_content = '<root><item1/><item2/></root>'
        root = ET.fromstring(xml_content)
        assert calculate_xml_depth(root) == 1

    def test_xml_depth_nested(self):
        """Test XML depth for nested structure."""
        xml_content = '<root><level1><level2><level3/></level2></level1></root>'
        root = ET.fromstring(xml_content)
        assert calculate_xml_depth(root) == 3


class TestCountNodes:
    """Test node counting."""

    def test_count_json_nodes_simple(self):
        """Test counting nodes in simple JSON."""
        data = {"a": 1, "b": 2}
        # Root object + 2 primitive values = 3
        assert count_nodes(data) == 3

    def test_count_json_nodes_nested(self):
        """Test counting nodes in nested JSON."""
        data = {"a": {"b": 1}}
        # Root + inner object + primitive = 3
        assert count_nodes(data) == 3

    def test_count_xml_nodes_simple(self):
        """Test counting nodes in simple XML."""
        xml_content = '<root><item1/><item2/></root>'
        root = ET.fromstring(xml_content)
        # root + item1 + item2 = 3
        assert count_xml_nodes(root) == 3

    def test_count_xml_nodes_nested(self):
        """Test counting nodes in nested XML."""
        xml_content = '<root><parent><child/></parent></root>'
        root = ET.fromstring(xml_content)
        # root + parent + child = 3
        assert count_xml_nodes(root) == 3


class TestInferJSONSchema:
    """Test JSON schema inference."""

    def test_infer_primitive_types(self):
        """Test schema inference for primitive types."""
        assert infer_json_schema("text")["type"] == "string"
        assert infer_json_schema(42)["type"] == "integer"
        assert infer_json_schema(3.14)["type"] == "number"
        assert infer_json_schema(True)["type"] == "boolean"
        assert infer_json_schema(None)["type"] == "null"

    def test_infer_object_schema(self):
        """Test schema inference for objects."""
        data = {"name": "test", "age": 25}
        schema = infer_json_schema(data)

        assert schema["type"] == "object"
        assert "properties" in schema
        assert schema["properties"]["name"]["type"] == "string"
        assert schema["properties"]["age"]["type"] == "integer"

    def test_infer_array_schema(self):
        """Test schema inference for arrays."""
        data = [{"id": 1}, {"id": 2}]
        schema = infer_json_schema(data)

        assert schema["type"] == "array"
        assert schema["items"]["type"] == "object"
        assert schema["length"] == 2


class TestAnalyzeStructures:
    """Test structure analysis functions."""

    def test_analyze_json_structure(self):
        """Test JSON structure analysis."""
        data = {"person": {"name": "test", "age": 25}}
        result = analyze_json_structure(data)

        assert result["format"] == "json"
        assert result["max_depth"] == 2
        assert result["node_count"] >= 3
        assert result["unique_paths"] >= 3
        assert "person" in result["paths"]

    def test_analyze_xml_structure(self):
        """Test XML structure analysis."""
        xml_content = '<root><person><name>test</name></person></root>'
        root = ET.fromstring(xml_content)
        result = analyze_xml_structure(root)

        assert result["format"] == "xml"
        assert result["root_tag"] == "root"
        assert result["max_depth"] >= 2
        assert result["node_count"] == 3


class TestAnalyzeSemistructuredFile:
    """Test file analysis entry point."""

    def test_analyze_json_file(self):
        """Test analyzing a JSON file end-to-end."""
        data = {"test": {"nested": "value"}}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = Path(f.name)

        try:
            result = analyze_semistructured_file(temp_path)

            assert "filepath" in result
            assert result["format"] == "json"
            assert result["max_depth"] >= 1
            assert "error" not in result
        finally:
            temp_path.unlink()

    def test_analyze_xml_file(self):
        """Test analyzing an XML file end-to-end."""
        xml_content = '<?xml version="1.0"?><root><item>value</item></root>'
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(xml_content)
            temp_path = Path(f.name)

        try:
            result = analyze_semistructured_file(temp_path)

            assert "filepath" in result
            assert result["format"] == "xml"
            assert result["root_tag"] == "root"
            assert "error" not in result
        finally:
            temp_path.unlink()

    def test_analyze_unsupported_file(self):
        """Test error handling for unsupported file type."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("test")
            temp_path = Path(f.name)

        try:
            result = analyze_semistructured_file(temp_path)

            assert "error" in result
            assert "Unsupported" in result["error"]
        finally:
            temp_path.unlink()
