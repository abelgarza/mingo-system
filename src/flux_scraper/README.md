# Flux Scraper

A systematic, OOP-based web scraping and ETL orchestration library for `mingo-system`.

## Features
- **Flow Orchestration**: Strict lifecycle definitions (`Extract` -> `Transform` -> `Load`).
- **Playwright Integrated**: Headless browser automation built into the core.
- **Pandas Data Pipelines**: Ready to consume, pivot, and analyze data reliably.

## Installation

Inside your mingo-system workspace:
```bash
pip install -e src/flux_scraper
playwright install chromium
```

## Usage

```bash
flux-scraper list
flux-scraper run <flow_name>
```
