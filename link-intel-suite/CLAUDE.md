# CLAUDE.md - project memory for the Link Intel Suite build

This file is your **context / memory for the AI**. Claude Code loads it automatically every
session. Strong builders engineer this file instead of re-explaining everything in chat - it
is one of the clearest signals of good practice, and it is graded (see the build brief
section on process). Keep it short, specific, and update it as you learn.

## What we are building
A Claude Code plugin that ingests a Screaming Frog export (`internal_html.csv` +
`all_inlinks.csv` + `all_outlinks.csv` + `all_anchor_text.csv` + a `page text/` folder) and
produces an **internal-linking + topical-authority** analysis: the internal link graph,
anchor-text issues, topical clusters, an entity graph, and **contextual internal-link
recommendations**. It serves a live dashboard at localhost:7700 and outputs
`outputs/report.json` + `outputs/report.html`.

## Hard rules (the agent must follow these)
- Do the graph, orphan detection, anchor classification and relatedness math in **plain
  Python** (`linkintel/analyzer.py`). Use the model ONLY for: extracting entities per page,
  naming clusters, and writing the contextual link suggestions + anchors. Never feed raw
  crawl rows to the model.
- `outputs/report.json` MUST match `report.schema.json`. Validate before declaring done.
- Pre-filter to `text/html` + 200 + Indexable for page-level checks; use `Type == Hyperlink`
  rows for link-level checks (see `rulebook.md`).
- Do not hard-code anything to the sample export - it must work on an unseen export with the
  same column shape.
- Keep model calls small and few (free-tier / cloud quota). One page per entity/anchor call.

## Architecture (keep it real)
- `skills/link-intel/SKILL.md` orchestrates. Sub-agents: `graph-agent`, `anchor-agent`,
  `topic-agent`, `linker-agent`, `reporter`.
- `linkintel/analyzer.py` = deterministic analysis (extend it - biggest score).
- `mcp/server.py` = MCP tools + the live dashboard host.

## Conventions
- Commit after each working step with a real message.
- Run `python run.py sample-export/` to test end to end.

## Things I have learned during the build (update this as you go)
- Page text filenames are URL-encoded with an `original_https_` prefix - decode before matching to Address.
- Orphans = `Unique Inlinks` == 0, NOT `Inlinks` == 0.
- Internal Link Stats: To be truly "internal", both Source AND Destination must be in the crawled page set; otherwise, external 4xx/3xx links pollute the broken/redirect lists.
- Entity Pipeline: `topic-agent` extracts model entities $\rightarrow$ `li_entities()` tool $\rightarrow$ `analyzer.relatedness()` (Jaccard overlap) $\rightarrow$ `analyzer.link_candidates()` $\rightarrow$ `report.json`.
- `relatedness()` in `analyzer.py` is a generic overlap calculator that uses TF keywords by default but accepts model-extracted entities via the MCP server.

## Current Status

Starter bundle runs successfully.

Completed:
- Baseline run and report generation verified.
- Rulebook reviewed.
- `cluster_pages()` improved from URL-path clustering to content-based clustering using TF keywords.
- Implemented `DOMAIN_STOPWORDS` filter to remove brand/generic noise from cluster keys.
- Fixed dashboard visibility: Introduced pacing delays in `run.py` and used `_run_mcp()` to ensure the dashboard remains live after analysis.
- Enhanced `link_candidates()`: Implemented strategic prioritization (bonus scores for orphans/under-linked/scattered), deterministic anchors, and detailed reasons.
- Fixed graph stats: Corrected `broken_internal_link`, `redirect_internal_link`, and `nofollow_internal_link` to exclude external URLs.

Current Priority:
- Integrate model-driven analysis (entities and recommendations) into the headless `run.py` path for grader compliance.

Next Steps:
- Implement a basic LLM invocation utility in `run.py`.
- Implement entity extraction loop for hub pages (LLM $\rightarrow$ `li_entities()`).
- Implement contextual anchor generation loop for top candidates (LLM $\rightarrow$ `li_set_recommendations()`).
- Refine `DOMAIN_STOPWORDS` to further remove noise.
