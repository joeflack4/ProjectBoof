# Agent Guidelines

- Place data ingestion and analysis scripts under `db/sources/`.
  - Use `db/sources/by_source/<source>/` for source-specific tooling (e.g., `cbioportal`, `clingen`).
  - Put cross-source utilities directly under `db/sources/`.
- Keep automation entry points callable via `make download-sources` so everything can be refreshed in one command.
- Write manifests with checksums for each download to support integrity verification.
- Leave raw datasets under `data/raw/` (git-ignored) and document provenance in the corresponding manifest/README.
