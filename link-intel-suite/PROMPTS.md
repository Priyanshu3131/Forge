# PROMPTS.md - my key prompts log

Keep the handful of prompts that actually moved the build. Not every message - the ones that
mattered: the system/sub-agent prompts, the ones you iterated on, the "this finally worked"
moment. Paste them here MANUALLY as you go.

Why manual? Some free Ollama cloud models do not save a local session log, so an auto audit
log may be empty. That is fine and expected (see the brief's Model Fairness section). What
guarantees your process is judged fairly is: the working plugin + reproducible report.json,
incremental git commits, this PROMPTS.md, and a short DECISIONS.md. Keep these up to date.

Format per entry:
- **Prompt** (paste it)
- **For:** what you were trying to do
- **Revised?** did you have to change it, and why

---

## My prompts

- Prompt: "Improve cluster_pages(). Current implementation: Pages are clustered by first URL path segment. Goal: Replace URL-based clustering with deterministic content-based clustering using existing page_keywords() output. Constraints: No new dependencies unless clearly justified. Keep report.json structure unchanged. Maintain hidden-dataset compatibility. Inspect cluster_pages() and propose the smallest high-impact change."
For: Replacing URL-based clustering with deterministic content-based clustering using TF keywords.
Revised? No.
Prompt: "Inspect cluster_pages(). The current implementation clusters pages using the first keyword returned by page_keywords(). Problem: Many cluster keys are generic or brand-specific rather than topical. Examples: nmg, estimated, development, design, website, business, team, software, web, app, mobile, marketing. Task: 1. Add a DOMAIN_STOPWORDS set inside analyzer.py. 2. When selecting the cluster key, choose the first keyword that is NOT in DOMAIN_STOPWORDS. 3. If all keywords are filtered out, fall back to the original first keyword."
For: Improving topical cluster quality by filtering out brand and generic agency-wide terms from cluster keys.
Revised? No.
Prompt: "Read linkintel/analyzer.py and locate the function responsible for generating internal link recommendations (link_candidates() or equivalent). Analyze the current recommendation pipeline and compare it against the Forge Sprint 01 rulebook. Identify whether orphan pages, under-linked pages, and scattered clusters are considered. Recommend the smallest deterministic changes that improve recommendation quality without changing the report schema."
For: Auditing recommendation generation against the rulebook before implementing prioritization improvements.
Revised? No.
Prompt: "Implement recommendation prioritization improvements in link_candidates(). Add scoring bonuses for orphan pages, under-linked pages, and pages belonging to scattered clusters. Preserve deterministic behavior, existing report.json schema, and hidden-dataset compatibility."
For: Improving contextual link recommendation quality and aligning recommendation ranking with the rulebook.
Revised? No.
Prompt: "Populate suggested_anchor and reason fields for contextual link recommendations. Use deterministic page metadata (H1, title, shared keywords) rather than model calls. Ensure anchors are descriptive and reasons explain topical similarity and structural SEO benefits."
For: Completing recommendation outputs with actionable anchors and explanations.
Revised? No.
Prompt: "Inspect broken_internal_link detection. The rulebook states that both Source and Destination must be crawled pages. Verify whether external URLs are being included in broken_internal_link, redirect_internal_link, or nofollow_internal_link detection. Trace the code path and propose the smallest rulebook-compliant fix."
For: Identifying and correcting incorrect inclusion of external URLs in internal-link reporting.
Revised? No.
Prompt: "Trace the data flow from link_candidates() through report generation and dashboard rendering. Determine why report.json contains link recommendations while the dashboard displays 'No recommendations yet'. Identify the smallest fix that exposes existing recommendation data to the dashboard."
For: Debugging dashboard recommendation rendering and ensuring generated recommendations are visible during review.
Revised? No.
---

* **Prompt:** "Implement AI-assisted cluster naming using local Ollama only. Keep clustering assignments unchanged. Use run.py as the integration point and li_topics(names) to inject generated names. Input to the model: cluster keyword, top keywords, and sample page titles. Output: a short cluster name (2-5 words). Add graceful fallback so that if Ollama is unavailable, the existing deterministic cluster label is preserved. No API keys, no external services, and no new dependencies beyond the Python standard library."

* **For:** Improving cluster presentation quality while maintaining deterministic execution and hidden-dataset compatibility.

* **Revised?** No.

---

* **Prompt:** "Before implementing AI cluster naming, determine whether the solution requires an external API key, internet access, or third-party model provider. Verify whether a local Ollama-based implementation can be used instead and ensure python run.py <export> continues to work when no model is available."

* **For:** Validating submission safety and ensuring AI enhancements do not introduce grading-time failures.

* **Revised?** No.
