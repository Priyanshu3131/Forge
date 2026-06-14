# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This repository is a "Starter Bundle" for an Internal Linking Intelligence tool. It is designed to analyze Screaming Frog SEO exports to identify internal linking issues and suggest topical authority improvements.

## Architecture
The project is structured as a bundle containing the core implementation and supporting data:
- `link-intel-suite/`: The main application.
    - `linkintel/`: Core deterministic analysis logic (`analyzer.py`).
    - `mcp/`: MCP server and tools providing the live dashboard.
    - `skills/`: Claude Code skill definitions and orchestration.
    - `agents/`: Specialized sub-agents for graph, anchor, topic, and link analysis.
    - `dashboard/`: Frontend for visualizing the internal linking analysis.
    - `run.py`: The primary entry point for executing the analysis pipeline.
- `sample-export/`: A real-world Screaming Frog crawl dataset for testing.
- `rulebook.md`: The official specification for all analysis rules (orphans, anchors, topical clusters, etc.).
- `report.schema.json`: The JSON schema defining the required output format for the analysis report.

## Common Development Tasks
### Running the Analysis
To run the end-to-end analysis pipeline against the sample export:
```bash
cd link-intel-suite
pip install mcp
python run.py ../sample-export/
```
The live cockpit is accessible at `http://localhost:7700`, and outputs are generated in `link-intel-suite/outputs/`.

## Key Constraints & Guidance
- **Deterministic vs. AI**: All graph, orphan detection, anchor classification, and relatedness calculations must be performed in Python (`linkintel/analyzer.py`). The AI should only be used for entity extraction, cluster naming, and writing contextual link recommendations.
- **Data Filtering**: 
    - Page-level checks: Filter for `text/html` content type, 200 status code, and `Indexable` indexability.
    - Link-level checks: Use `Type == Hyperlink` rows from `all_inlinks.csv`.
- **Generalization**: Implementations must work on any Screaming Frog export with the correct column shape, not just the provided `sample-export/`.
- **Output Compliance**: The final `report.json` must strictly adhere to `report.schema.json`.
