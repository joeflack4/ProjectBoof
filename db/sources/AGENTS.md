# Agent Guidelines — `db/sources/`

- Add each source-specific workflow under `by_source/<source>/`.
- Shared helpers used by multiple sources belong directly in `db/sources/`.
- Expose repeatable entrypoints (e.g., `download.py`) so `make download-sources` can orchestrate them.
