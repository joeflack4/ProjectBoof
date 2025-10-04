#!/usr/bin/env python3
"""Download ClinGen bulk data files into the canonical directory layout."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class DownloadSpec:
    url: str
    subdir: str
    filename: str
    description: str


DOWNLOADS: List[DownloadSpec] = [
    DownloadSpec(
        url="https://search.clinicalgenome.org/kb/gene-validity/download",
        subdir="gene-validity",
        filename="gene-validity.csv",
        description="Gene-Disease Validity summary",
    ),
    DownloadSpec(
        url="ftp://ftp.clinicalgenome.org/ClinGen_gene_curation_list_GRCh37.tsv",
        subdir="dosage-sensitivity",
        filename="dosage-sensitivity-grch37.tsv",
        description="Dosage sensitivity gene curation list (GRCh37)",
    ),
    DownloadSpec(
        url="ftp://ftp.clinicalgenome.org/ClinGen_gene_curation_list_GRCh38.tsv",
        subdir="dosage-sensitivity",
        filename="dosage-sensitivity-grch38.tsv",
        description="Dosage sensitivity gene curation list (GRCh38)",
    ),
    DownloadSpec(
        url="ftp://ftp.clinicalgenome.org/ClinGen_region_curation_list_GRCh37.tsv",
        subdir="dosage-regions",
        filename="dosage-sensitivity-regions-grch37.tsv",
        description="Dosage sensitivity region curation list (GRCh37)",
    ),
    DownloadSpec(
        url="ftp://ftp.clinicalgenome.org/ClinGen_region_curation_list_GRCh38.tsv",
        subdir="dosage-regions",
        filename="dosage-sensitivity-regions-grch38.tsv",
        description="Dosage sensitivity region curation list (GRCh38)",
    ),
    DownloadSpec(
        url="ftp://ftp.clinicalgenome.org/ClinGen%20recurrent%20CNV%20.bed%20file%20V1.1-hg19.bed",
        subdir="dosage-regions",
        filename="dosage-sensitivity-regions-grch37.bed",
        description="Dosage sensitivity recurrent CNV BED (hg19)",
    ),
    DownloadSpec(
        url="ftp://ftp.clinicalgenome.org/ClinGen%20recurrent%20CNV%20.bed%20file%20V1.1-hg38.bed",
        subdir="dosage-regions",
        filename="dosage-sensitivity-regions-grch38.bed",
        description="Dosage sensitivity recurrent CNV BED (hg38)",
    ),
    DownloadSpec(
        url="https://actionability.clinicalgenome.org/ac/Adult/api/summ?flavor=flat",
        subdir="actionability",
        filename="clinical-actionability-adult-flat.json",
        description="Clinical actionability adult flat JSON",
    ),
    DownloadSpec(
        url="https://actionability.clinicalgenome.org/ac/Pediatric/api/summ?flavor=flat",
        subdir="actionability",
        filename="clinical-actionability-pediatric-flat.json",
        description="Clinical actionability pediatric flat JSON",
    ),
    DownloadSpec(
        url="https://erepo.clinicalgenome.org/evrepo/api/classifications/all?format=csv",
        subdir="variant-pathogenicity",
        filename="variant-pathogenicity.csv",
        description="Variant pathogenicity classifications (CSV)",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-dir",
        default="data/raw/clingen",
        help="Root directory for ClinGen data (default: %(default)s)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if the target file exists.",
    )
    parser.add_argument(
        "--only",
        action="append",
        dest="only",
        help="Limit downloads to specific filenames (can be passed multiple times).",
    )
    return parser.parse_args()


def download_to(path: Path, url: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        with urllib.request.urlopen(url) as response:
            shutil.copyfileobj(response, tmp)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_metadata(base_dir: Path, specs: Iterable[DownloadSpec]) -> List[dict]:
    records = []
    for spec in specs:
        file_path = base_dir / spec.subdir / spec.filename
        if not file_path.exists():
            records.append(
                {
                    "filename": spec.filename,
                    "relative_path": str(file_path.relative_to(base_dir)),
                    "subdir": spec.subdir,
                    "url": spec.url,
                    "description": spec.description,
                    "status": "missing",
                }
            )
            continue
        records.append(
            {
                "filename": spec.filename,
                "relative_path": str(file_path.relative_to(base_dir)),
                "subdir": spec.subdir,
                "url": spec.url,
                "description": spec.description,
                "size_bytes": file_path.stat().st_size,
                "sha256": sha256(file_path),
                "status": "available",
            }
        )
    return records


def update_manifest(manifest_path: Path, records: List[dict]) -> None:
    manifest = {
        "last_updated": dt.datetime.utcnow().isoformat() + "Z",
        "files": records,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True))


def main() -> None:
    args = parse_args()
    base_dir = Path(args.base_dir)
    selected = {name for name in (args.only or [])}
    specs = [spec for spec in DOWNLOADS if not selected or spec.filename in selected or spec.subdir in selected]

    for spec in specs:
        target = base_dir / spec.subdir / spec.filename
        if target.exists() and not args.force:
            continue
        print(f"[download] {spec.filename} <- {spec.url}")
        download_to(target, spec.url)

    records = collect_metadata(base_dir, specs)
    update_manifest(base_dir / "manifest.json", records)


if __name__ == "__main__":
    main()
