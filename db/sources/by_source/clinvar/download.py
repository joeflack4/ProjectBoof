#!/usr/bin/env python3
"""Download ClinVar bulk release files and write a provenance manifest."""

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
    relative_path: str
    description: str


DOWNLOADS: List[DownloadSpec] = [
    DownloadSpec(
        url="https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz",
        relative_path="tabular/variant_summary.txt.gz",
        description="Monthly variant summary table",
    ),
    DownloadSpec(
        url="https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz",
        relative_path="grch37/vcf/clinvar.vcf.gz",
        description="ClinVar VCF (GRCh37)",
    ),
    DownloadSpec(
        url="https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz",
        relative_path="grch38/vcf/clinvar.vcf.gz",
        description="ClinVar VCF (GRCh38)",
    ),
    DownloadSpec(
        url="https://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/ClinVarVCVRelease_00-latest.xml.gz",
        relative_path="xml/vcv/ClinVarVCVRelease_00-latest.xml.gz",
        description="ClinVar VCV aggregated XML",
    ),
    DownloadSpec(
        url="https://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/RCV_release/ClinVarRCVRelease_00-latest.xml.gz",
        relative_path="xml/rcv/ClinVarRCVRelease_00-latest.xml.gz",
        description="ClinVar RCV aggregated XML",
    ),
    DownloadSpec(
        url="https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/var_citations.txt",
        relative_path="tabular/var_citations.txt",
        description="Variant citation links",
    ),
    DownloadSpec(
        url="https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/cross_references.txt",
        relative_path="tabular/cross_references.txt",
        description="Variant cross references",
    ),
    DownloadSpec(
        url="https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/submission_summary.txt.gz",
        relative_path="tabular/submission_summary.txt.gz",
        description="Submission summary metadata",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-dir",
        default="data/raw/clinvar",
        help="Root directory for ClinVar data (default: %(default)s)",
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
        help="Limit downloads to relative paths or filenames (can be passed multiple times).",
    )
    return parser.parse_args()


def should_download(spec: DownloadSpec, selected: set[str], target: Path, force: bool) -> bool:
    if selected and spec.relative_path not in selected and spec.relative_path.split("/")[-1] not in selected:
        return False
    return force or not target.exists()


def download_to(path: Path, url: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        with urllib.request.urlopen(url) as response:
            shutil.copyfileobj(response, tmp)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def remote_metadata(url: str) -> dict:
    request = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(request) as response:
            headers = response.info()
    except Exception:
        return {}
    meta: dict[str, object] = {}
    if headers.get("Last-Modified"):
        meta["source_last_modified"] = headers.get("Last-Modified")
    if headers.get("Content-Length"):
        try:
            meta["source_content_length"] = int(headers.get("Content-Length"))
        except (TypeError, ValueError):
            pass
    return meta


def collect_metadata(base_dir: Path, specs: Iterable[DownloadSpec]) -> List[dict]:
    records = []
    for spec in specs:
        path = base_dir / spec.relative_path
        if not path.exists():
            records.append(
                {
                    "description": spec.description,
                    "relative_path": spec.relative_path,
                    "url": spec.url,
                    "status": "missing",
                }
            )
            continue
        record = {
            "description": spec.description,
            "relative_path": spec.relative_path,
            "url": spec.url,
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
            "status": "available",
        }
        record.update(remote_metadata(spec.url))
        records.append(record)
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
    selected = set(args.only or [])

    for spec in DOWNLOADS:
        target = base_dir / spec.relative_path
        if should_download(spec, selected, target, args.force):
            print(f"[download] {spec.relative_path} <- {spec.url}")
            download_to(target, spec.url)

    records = collect_metadata(base_dir, DOWNLOADS)
    update_manifest(base_dir / "manifest.json", records)


if __name__ == "__main__":
    main()
