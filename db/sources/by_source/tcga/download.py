#!/usr/bin/env python3
"""Download TCGA open-access data from GDC using gdc-client and GDC API."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

GDC_API_URL = "https://api.gdc.cancer.gov"
GDC_CLIENT = "scripts/tools/gdc-client"

# Default TCGA projects to download (matching cBioPortal studies)
DEFAULT_PROJECTS = ["TCGA-BRCA", "TCGA-LUAD"]

# Data types to download
DATA_TYPES = {
    "clinical": {
        "data_category": "Clinical",
        "data_type": "Clinical Supplement",
        "data_format": "BCR XML",
    },
    "biospecimen": {
        "data_category": "Biospecimen",
        "data_type": "Biospecimen Supplement",
        "data_format": "BCR XML",
    },
    "mutations": {
        "data_category": "Simple Nucleotide Variation",
        "data_type": "Masked Somatic Mutation",
        "data_format": "MAF",
    },
    "expression": {
        "data_category": "Transcriptome Profiling",
        "data_type": "Gene Expression Quantification",
        "workflow_type": "STAR - Counts",
    },
    "copy-number": {
        "data_category": "Copy Number Variation",
        "data_type": "Copy Number Segment",
    },
    "methylation": {
        "data_category": "DNA Methylation",
        "data_type": "Methylation Beta Value",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-dir",
        default="data/raw/tcga",
        help="Root directory for TCGA data (default: %(default)s)",
    )
    parser.add_argument(
        "--project",
        action="append",
        dest="projects",
        help=f"TCGA project to download (default: {DEFAULT_PROJECTS}). Can be specified multiple times.",
    )
    parser.add_argument(
        "--data-type",
        action="append",
        dest="data_types",
        choices=list(DATA_TYPES.keys()),
        help=f"Data types to download (default: all). Can be specified multiple times.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of files per data type (for testing)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be downloaded without actually downloading",
    )
    parser.add_argument(
        "--gdc-client",
        default=GDC_CLIENT,
        help=f"Path to gdc-client binary (default: {GDC_CLIENT})",
    )
    return parser.parse_args()


def query_gdc_files(
    project: str, data_type_filters: Dict[str, str], limit: int | None = None
) -> List[Dict[str, Any]]:
    """Query GDC API for files matching the criteria."""
    filters = {
        "op": "and",
        "content": [
            {"op": "in", "content": {"field": "cases.project.project_id", "value": [project]}},
            {"op": "in", "content": {"field": "access", "value": ["open"]}},
        ],
    }

    for field, value in data_type_filters.items():
        filters["content"].append(
            {"op": "in", "content": {"field": f"files.{field}", "value": [value]}}
        )

    params = {
        "filters": json.dumps(filters),
        "fields": "file_id,file_name,file_size,md5sum,data_type,data_category,data_format",
        "format": "JSON",
        "size": str(limit) if limit else "10000",
    }

    url = f"{GDC_API_URL}/files?" + urllib.parse.urlencode(params)

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())

    return data.get("data", {}).get("hits", [])


def download_with_gdc_client(
    files: List[Dict[str, Any]], output_dir: Path, gdc_client_path: str
) -> bool:
    """Download files using gdc-client."""
    if not files:
        return True

    output_dir.mkdir(parents=True, exist_ok=True)

    # Create proper GDC manifest file (TSV format)
    manifest_file = output_dir / "gdc_manifest.txt"
    with manifest_file.open("w") as f:
        # Header
        f.write("id\tfilename\tmd5\tsize\tstate\n")
        # File entries
        for file_info in files:
            f.write(
                f"{file_info['file_id']}\t"
                f"{file_info['file_name']}\t"
                f"{file_info.get('md5sum', '')}\t"
                f"{file_info.get('file_size', '')}\t"
                f"submitted\n"
            )

    cmd = [
        gdc_client_path,
        "download",
        "-m", str(manifest_file),
        "-d", str(output_dir),
        "--no-annotations",
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading files: {e.stderr}", file=sys.stderr)
        return False


def sha256(path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def create_manifest(
    base_dir: Path, project: str, data_type: str, files: List[Dict[str, Any]]
) -> None:
    """Create a manifest file documenting downloaded files."""
    manifest = {
        "source": "TCGA via GDC",
        "project": project,
        "data_type": data_type,
        "download_date": dt.datetime.now(dt.timezone.utc).isoformat(),
        "file_count": len(files),
        "files": [
            {
                "file_id": f["file_id"],
                "file_name": f["file_name"],
                "file_size": f.get("file_size"),
                "md5sum": f.get("md5sum"),
                "data_type": f.get("data_type"),
                "data_category": f.get("data_category"),
                "data_format": f.get("data_format"),
            }
            for f in files
        ],
    }

    manifest_dir = base_dir / "open-access" / "metadata" / project
    manifest_dir.mkdir(parents=True, exist_ok=True)

    manifest_file = manifest_dir / f"{data_type}_manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2))
    print(f"Created manifest: {manifest_file}")


def main() -> int:
    args = parse_args()

    # Check gdc-client exists
    gdc_client_path = Path(args.gdc_client)
    if not gdc_client_path.exists():
        print(f"Error: gdc-client not found at {gdc_client_path}", file=sys.stderr)
        print("Please run: make install-gdc-client", file=sys.stderr)
        return 1

    base_dir = Path(args.base_dir)
    projects = args.projects or DEFAULT_PROJECTS
    data_types = args.data_types or list(DATA_TYPES.keys())

    print(f"Downloading TCGA data to: {base_dir}")
    print(f"Projects: {projects}")
    print(f"Data types: {data_types}")

    for project in projects:
        print(f"\n{'='*60}")
        print(f"Processing project: {project}")
        print(f"{'='*60}")

        for data_type in data_types:
            print(f"\n--- {data_type} ---")

            filters = DATA_TYPES[data_type]
            files = query_gdc_files(project, filters, limit=args.limit)

            if not files:
                print(f"No {data_type} files found for {project}")
                continue

            print(f"Found {len(files)} {data_type} files")

            if args.dry_run:
                print("  (dry-run, skipping download)")
                for f in files[:5]:  # Show first 5
                    print(f"  - {f['file_name']} ({f.get('file_size', 0) / 1024 / 1024:.2f} MB)")
                if len(files) > 5:
                    print(f"  ... and {len(files) - 5} more")
                continue

            # Download files
            output_dir = base_dir / "open-access" / data_type / project

            success = download_with_gdc_client(files, output_dir, str(gdc_client_path))

            if success:
                create_manifest(base_dir, project, data_type, files)
                print(f"✓ Downloaded {len(files)} {data_type} files to {output_dir}")
            else:
                print(f"✗ Failed to download {data_type} files", file=sys.stderr)

    print(f"\n{'='*60}")
    print("Download complete!")
    print(f"{'='*60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
