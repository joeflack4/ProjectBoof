"""Semi-structured data (JSON/XML) analysis engine."""

from pathlib import Path
from typing import Dict, Any, List, Optional, Set
import json
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict


def parse_json(filepath: Path) -> Dict[str, Any]:
    """
    Parse JSON file and return data structure.

    Args:
        filepath: Path to JSON file

    Returns:
        Parsed JSON data as dictionary
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_xml(filepath: Path) -> ET.Element:
    """
    Parse XML file and return root element.

    Args:
        filepath: Path to XML file

    Returns:
        Root element of XML tree
    """
    tree = ET.parse(filepath)
    return tree.getroot()


def extract_json_paths(data: Any, prefix: str = "") -> Set[str]:
    """
    Extract all JSON paths from nested structure.

    Args:
        data: JSON data (dict, list, or primitive)
        prefix: Current path prefix

    Returns:
        Set of all paths in the structure
    """
    paths = set()

    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{prefix}.{key}" if prefix else key
            paths.add(current_path)
            paths.update(extract_json_paths(value, current_path))
    elif isinstance(data, list) and len(data) > 0:
        # Sample first element for structure
        paths.add(f"{prefix}[]")
        paths.update(extract_json_paths(data[0], f"{prefix}[]"))

    return paths


def extract_xml_paths(element: ET.Element, prefix: str = "") -> Set[str]:
    """
    Extract all XPath-like paths from XML structure.

    Args:
        element: XML element
        prefix: Current path prefix

    Returns:
        Set of all paths in the structure
    """
    paths = set()

    # Remove namespace prefix for cleaner paths
    tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
    current_path = f"{prefix}/{tag}" if prefix else tag
    paths.add(current_path)

    for child in element:
        paths.update(extract_xml_paths(child, current_path))

    return paths


def calculate_json_depth(data: Any, current_depth: int = 0) -> int:
    """
    Calculate maximum nesting depth of JSON structure.

    Args:
        data: JSON data
        current_depth: Current depth level

    Returns:
        Maximum depth
    """
    if isinstance(data, dict):
        if not data:
            return current_depth
        return max(calculate_json_depth(v, current_depth + 1) for v in data.values())
    elif isinstance(data, list):
        if not data:
            return current_depth
        return max(calculate_json_depth(item, current_depth + 1) for item in data)
    else:
        return current_depth


def calculate_xml_depth(element: ET.Element, current_depth: int = 0) -> int:
    """
    Calculate maximum nesting depth of XML structure.

    Args:
        element: XML element
        current_depth: Current depth level

    Returns:
        Maximum depth
    """
    children = list(element)
    if not children:
        return current_depth

    return max(calculate_xml_depth(child, current_depth + 1) for child in children)


def count_nodes(data: Any) -> int:
    """
    Count total number of nodes in JSON structure.

    Args:
        data: JSON data

    Returns:
        Total node count
    """
    count = 1  # Current node

    if isinstance(data, dict):
        for value in data.values():
            count += count_nodes(value)
    elif isinstance(data, list):
        for item in data:
            count += count_nodes(item)

    return count


def count_xml_nodes(element: ET.Element) -> int:
    """
    Count total number of nodes in XML tree.

    Args:
        element: XML element

    Returns:
        Total node count
    """
    count = 1  # Current element

    for child in element:
        count += count_xml_nodes(child)

    return count


def infer_json_schema(data: Any, path: str = "root") -> Dict[str, Any]:
    """
    Infer JSON schema-like structure from data.

    Args:
        data: JSON data
        path: Current path (for debugging)

    Returns:
        Schema description
    """
    if isinstance(data, dict):
        return {
            "type": "object",
            "properties": {
                key: infer_json_schema(value, f"{path}.{key}")
                for key, value in data.items()
            }
        }
    elif isinstance(data, list):
        if not data:
            return {"type": "array", "items": {}}
        # Infer from first element
        return {
            "type": "array",
            "items": infer_json_schema(data[0], f"{path}[0]"),
            "length": len(data)
        }
    elif isinstance(data, bool):
        return {"type": "boolean"}
    elif isinstance(data, int):
        return {"type": "integer"}
    elif isinstance(data, float):
        return {"type": "number"}
    elif isinstance(data, str):
        return {"type": "string"}
    elif data is None:
        return {"type": "null"}
    else:
        return {"type": "unknown"}


def analyze_json_structure(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze JSON structure and return statistics.

    Args:
        data: Parsed JSON data

    Returns:
        Dictionary of structural statistics
    """
    paths = extract_json_paths(data)
    depth = calculate_json_depth(data)
    node_count = count_nodes(data)
    schema = infer_json_schema(data)

    return {
        "format": "json",
        "max_depth": depth,
        "node_count": node_count,
        "unique_paths": len(paths),
        "paths": sorted(list(paths)),
        "schema": schema,
    }


def analyze_xml_structure(root: ET.Element) -> Dict[str, Any]:
    """
    Analyze XML structure and return statistics.

    Args:
        root: XML root element

    Returns:
        Dictionary of structural statistics
    """
    paths = extract_xml_paths(root)
    depth = calculate_xml_depth(root)
    node_count = count_xml_nodes(root)

    # Extract tag frequencies
    tag_counter = Counter()

    def count_tags(element):
        tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
        tag_counter[tag] += 1
        for child in element:
            count_tags(child)

    count_tags(root)

    return {
        "format": "xml",
        "root_tag": root.tag.split('}')[-1] if '}' in root.tag else root.tag,
        "max_depth": depth,
        "node_count": node_count,
        "unique_paths": len(paths),
        "paths": sorted(list(paths))[:50],  # Limit to top 50 for readability
        "tag_frequencies": dict(tag_counter.most_common(20)),
    }


def analyze_semistructured_file(filepath: Path) -> Dict[str, Any]:
    """
    Main entry point for analyzing semi-structured files.

    Args:
        filepath: Path to JSON or XML file

    Returns:
        Analysis results dictionary
    """
    suffix = filepath.suffix.lower()

    result = {
        "filepath": str(filepath),
        "filename": filepath.name,
        "file_size_mb": filepath.stat().st_size / (1024 * 1024),
    }

    try:
        if suffix == '.json':
            data = parse_json(filepath)
            result.update(analyze_json_structure(data))
        elif suffix == '.xml':
            root = parse_xml(filepath)
            result.update(analyze_xml_structure(root))
        else:
            result["error"] = f"Unsupported file type: {suffix}"

        return result

    except Exception as e:
        result["error"] = str(e)
        return result
