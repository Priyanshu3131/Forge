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

- **Prompt:** "Improve cluster_pages(). Current implementation: Pages are clustered by first URL path segment. Goal: Replace URL-based clustering with deterministic content-based clustering using existing page_keywords() output. Constraints: No new dependencies unless clearly justified. Keep report.json structure unchanged. Maintain hidden-dataset compatibility. Inspect cluster_pages() and propose the smallest high-impact change."
- **For:** Replacing URL-based clustering with deterministic content-based clustering using TF keywords.
- **Revised?** No.

---

- **Prompt:** "Inspect cluster_pages(). The current implementation clusters pages using the first keyword returned by page_keywords(). Problem: Many cluster keys are generic or brand-specific rather than topical. Examples: nmg, estimated, development, design, website, business, team, software, web, app, mobile, marketing. Task: 1. Add a DOMAIN_STOPWORDS set inside analyzer.py. 2. When selecting the cluster key, choose the first keyword that is NOT in DOMAIN_STOPWORDS. 3. If all keywords are filtered out, fall back to the original first keyword."
- **For:** Improving topical cluster quality by filtering out brand and generic agency-wide terms from cluster keys.
- **Revised?** No.

---

- **Prompt:** "Extract 5-10 key entities from the following page text. An entity is a specific person, organization, technology, or unique concept (e.g., 'React', 'SaaS', 'Azure'). Avoid generic words like 'business' or 'service'. Return the entities as a simple comma-separated list."
- **For:** Headless entity extraction for hub pages in run.py.
- **Revised?** Pending implementation.

---

- **Prompt:** "You are an SEO expert. Write a high-quality, contextual internal link anchor for a link from [Source URL] to [Target URL]. The target page is about [Target Topic]. The source page text is: [Source Text]. The anchor should be descriptive, naturally integrated, and use keywords that signal authority. Return only the anchor text and a brief one-sentence reason for the choice."
- **For:** Headless contextual link recommendation generation in run.py.
- **Revised?** Pending implementation.
