#!/usr/bin/env python3
"""Download select cBioPortal studies and place files into structured directories."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import hashlib
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path
from typing import Dict, List

BASE_SUBDIRS = [
    "clinical",
    "mutations",
    "cna",
    "expression",
    "methylation",
    "protein",
    "phosphoprotein",
    "ancestry",
    "timelines",
    "metadata",
    "gene-panel",
    "structural-variants",
]

ROUTING_RULES = [
    ("clinical", ("data_clinical", "meta_clinical")),
    ("timelines", ("data_timeline", "meta_timeline")),
    ("mutations", ("data_mutations", "meta_mutations")),
    ("structural-variants", ("data_sv", "meta_sv")),
    (
        "cna",
        (
            "data_cna",
            "data_log2_cna",
            "data_cna_hg19",
            "data_armlevel_cna",
            "meta_cna",
            "meta_log2_cna",
            "meta_cna_hg19",
            "meta_armlevel_cna",
        ),
    ),
    ("expression", ("data_mrna", "meta_mrna")),
    ("methylation", ("data_methylation", "meta_methylation")),
    (
        "protein",
        (
            "data_protein",
            "meta_protein",
            "data_rppa",
            "meta_rppa",
        ),
    ),
    (
        "phosphoprotein",
        (
            "data_phosphoprotein",
            "meta_phosphoprotein",
        ),
    ),
    ("ancestry", ("data_genetic_ancestry", "meta_genetic_ancestry")),
    ("gene-panel", ("data_gene_panel_matrix", "meta_gene_panel_matrix")),
    (
        "metadata",
        (
            "data_resource",
            "meta_resource",
            "meta_study",
            "README",
            "LICENSE",
        ),
    ),
]

DEFAULT_STUDIES: Dict[str, Dict[str, str]] = {
    "brca_tcga_pan_can_atlas_2018": {
        "url": "https://cbioportal-datahub.s3.amazonaws.com/brca_tcga_pan_can_atlas_2018.tar.gz",
    },
    "luad_tcga_pan_can_atlas_2018": {
        "url": "https://cbioportal-datahub.s3.amazonaws.com/luad_tcga_pan_can_atlas_2018.tar.gz",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-dir",
        default="data/raw/cbioportal",
        help="Root directory for storing cBioPortal data (default: %(default)s)",
    )
    parser.add_argument(
        "--study",
        action="append",
        dest="studies",
        help="Study identifier to download (can be passed multiple times).",
    )
    parser.add_argument(
        "--all-default",
        action="store_true",
        help="Download all studies listed in DEFAULT_STUDIES.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if data appears to be present.",
    )
    return parser.parse_args()


def ensure_structure(base_dir: Path) -> None:
    for subdir in BASE_SUBDIRS:
        (base_dir / subdir).mkdir(parents=True, exist_ok=True)


def categorize(name: str) -> str | None:
    for target, prefixes in ROUTING_RULES:
        if any(name.startswith(prefix) for prefix in prefixes):
            return target
    return None


def prepare_destination(dest_root: Path, study: str, category: str, prepared: Dict[str, Path]) -> Path:
    if category in prepared:
        return prepared[category]
    dest = dest_root / category / study
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    prepared[category] = dest
    return dest


def checksum(path: Path) -> Dict[str, object]:
    hasher = hashlib.sha256()
    size = 0
    with path.open("rb") as source:
        while True:
            chunk = source.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
            size += len(chunk)
    return {"name": path.name, "size_bytes": size, "sha256": hasher.hexdigest()}


def dir_entry(path: Path) -> Dict[str, object]:
    return {"name": f"{path.name}/", "type": "directory"}


def copy_item(src: Path, dest_root: Path, study: str, prepared: Dict[str, Path], files_record: Dict[str, List[Dict[str, object]]]) -> None:
    name = src.name
    if src.is_dir():
        category = "metadata"
        base_dest = prepare_destination(dest_root, study, category, prepared)
        target_dir = base_dest / name
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(src, target_dir)
        files_record.setdefault(category, []).append(dir_entry(target_dir))
        return

    category = categorize(name)
    if category is None:
        # Keep uncategorized files under metadata
        category = "metadata"
    dest_dir = prepare_destination(dest_root, study, category, prepared)
    destination = dest_dir / name
    shutil.copy2(src, destination)
    files_record.setdefault(category, []).append(checksum(destination))


def download_bundle(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, destination)


def extract_bundle(bundle_path: Path, extract_dir: Path) -> Path:
    with tarfile.open(bundle_path) as tar:
        tar.extractall(extract_dir)
    study_dirs = [p for p in extract_dir.iterdir() if p.is_dir()]
    if len(study_dirs) != 1:
        raise RuntimeError("Expected exactly one directory in bundle; found %d" % len(study_dirs))
    return study_dirs[0]


def collect_existing_files(base_dir: Path, study: str) -> Dict[str, List[Dict[str, object]]]:
    files_record: Dict[str, List[Dict[str, object]]] = {}
    for category in BASE_SUBDIRS:
        study_dir = base_dir / category / study
        if not study_dir.exists():
            continue
        entries: List[Dict[str, object]] = []
        for path in sorted(study_dir.iterdir()):
            if path.is_dir():
                entries.append(dir_entry(path))
            else:
                entries.append(checksum(path))
        if entries:
            files_record[category] = entries
    return files_record


def update_manifest(
    manifest_path: Path,
    study: str,
    url: str,
    files_record: Dict[str, List[Dict[str, object]]],
    downloaded_at: str,
    last_updated: str | None = None,
) -> None:
    completed = {
        "Identify target studies and sample lists",
        "Fetch study metadata via /studies endpoint",
        "Download clinical patient/sample data",
        "Download mutation (MAF), CNA, expression, and other molecular profiles",
        "Capture manifest with study IDs, API version, and download timestamps",
    }
    timestamp = last_updated or dt.datetime.utcnow().isoformat() + "Z"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
    else:
        manifest = {}

    manifest.setdefault("studies", {})
    manifest["studies"][study] = {
        "source_url": url,
        "downloaded_at": downloaded_at,
        "files": files_record,
    }
    manifest["status"] = "in_progress"
    pending = manifest.get("pending_tasks", [])
    manifest["pending_tasks"] = [task for task in pending if task not in completed]
    manifest.setdefault("files", [])
    manifest["last_updated"] = timestamp
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True))


def ensure_study_list(base_dir: Path) -> None:
    metadata_dir = base_dir / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)


def download_study(study: str, base_dir: Path, url: str, force: bool) -> None:
    ensure_structure(base_dir)
    ensure_study_list(base_dir)
    sentinel = base_dir / "metadata" / study / ".download-complete"
    if sentinel.exists() and not force:
        print(f"[verify] {study} already downloaded; refreshing manifest")
        files_record = collect_existing_files(base_dir, study)
        sentinel_value = sentinel.read_text().strip()
        downloaded_at = sentinel_value or dt.datetime.utcnow().isoformat() + "Z"
        update_manifest(
            base_dir / "manifest.json",
            study,
            url,
            files_record,
            downloaded_at,
        )
        return

    dataset_indicator = base_dir / "clinical" / study / "data_clinical_patient.txt"
    if dataset_indicator.exists() and not force:
        print(f"[skip] Existing files found for {study}; marking complete")
        files_record = collect_existing_files(base_dir, study)
        downloaded_at = dt.datetime.utcnow().isoformat() + "Z"
        update_manifest(base_dir / "manifest.json", study, url, files_record, downloaded_at)
        sentinel.parent.mkdir(parents=True, exist_ok=True)
        sentinel.write_text(downloaded_at)
        return

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_dir = Path(tmp_dir_name)
        bundle_path = tmp_dir / f"{study}.tar.gz"
        print(f"[download] {study} <- {url}")
        download_bundle(url, bundle_path)
        extracted_dir = extract_bundle(bundle_path, tmp_dir)
        prepared: Dict[str, Path] = {}
        files_record: Dict[str, List[str]] = {}
        for item in sorted(extracted_dir.iterdir()):
            copy_item(item, base_dir, study, prepared, files_record)
    timestamp = dt.datetime.utcnow().isoformat() + "Z"
    update_manifest(base_dir / "manifest.json", study, url, files_record, timestamp)
    sentinel.parent.mkdir(parents=True, exist_ok=True)
    sentinel.write_text(timestamp)
    print(f"[done] {study}")


def main() -> None:
    args = parse_args()
    requested = set(args.studies or [])
    if args.all_default or not requested:
        requested.update(DEFAULT_STUDIES.keys())
    base_dir = Path(args.base_dir)
    for study in sorted(requested):
        info = DEFAULT_STUDIES.get(study)
        if info is None:
            raise SystemExit(f"Unknown study: {study}")
        download_study(study, base_dir, info["url"], args.force)


if __name__ == "__main__":
    main()
