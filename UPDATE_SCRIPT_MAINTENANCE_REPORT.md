# Update Script Maintenance Report

Date: 2026-03-04

- Re-ran `scripts/process.py`; local outputs already matched currently available upstream files, so no data changes were produced in this run.
- Updated GitHub Actions automation at `.github/workflows/actions.yml`:
  - removed push/PR triggers and kept schedule + manual dispatch,
  - added explicit `permissions: contents: write`,
  - upgraded to `actions/checkout@v4` and `actions/setup-python@v5`,
  - simplified script execution via `make -C scripts`.
- Current freshness gap is tied to EIA publication lag and next daily release timing, not a local pipeline failure.
