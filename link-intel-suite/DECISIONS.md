# DECISIONS.md - decision & learnings log

A short running note of the real choices you made: what you tried, what failed and why, what
you changed. This is your engineering judgement on the record - it is what separates a builder
from a button-presser, and it is graded (from git history + this file + PROMPTS.md, NOT from
an auto audit log, which may be empty on cloud models).

Append a 1-2 line entry whenever you make a real decision or hit/fix a wall. Add a timestamp.

Format:
`[HH:MM] <decision or problem> -> <what you did and why>`

---

## My log
- `[14:30]` Headless AI integration -> Integrated LLM calls directly into `run.py` to ensure the grader captures model-driven results (entity extraction and contextual anchors) without requiring interactive agent orchestration.
- `[14:35]` Page selection optimization -> Decided to process only hub pages for entity extraction and top 3 candidates for anchors to keep model usage within reasonable limits.

- `[16:00]` Dashboard visibility & persistence -> Introduced `time.sleep(1)` delays between analysis stages in `run.py` to make real-time updates human-perceivable, and added `server._run_mcp()` at the end of the pipeline to keep the server process alive after analysis completes.

Decision #2
Current clustering groups pages by URL path segment.

Issue:
Pages with different topics can end up in the same cluster.

Planned Improvement:
Move toward content-based clustering using page_keywords() output.

Decision #2
Replaced URL-path clustering with content-based keyword clustering.

Reason:
URL segments did not reflect actual topics.

Decision #3
Added DOMAIN_STOPWORDS filtering.

Reason:
Generic keys such as nmg, estimated, development, and business were dominating clusters.

Result:
More topical clusters such as ecommerce, healthcare, wordpress, outsourcing, and enterprise.
