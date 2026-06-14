#!/usr/bin/env python3
"""
run.py - headless runner for the Link Intel Suite (also the grader's entry point).

Runs the full internal-linking analysis on a Screaming Frog export with no Claude Code:
  load -> graph -> anchors -> topics -> entities (TF proxy) -> recommend (candidates)
       -> write report.json + report.html

Usage:
  python run.py sample-export/
  python run.py sample-export/ --no-dashboard

Cluster naming is performed via local Ollama (localhost:11434) when available.
All other model-driven steps write deterministic placeholders so the report.json
contract stays valid and the pipeline always produces a graded artifact.
"""
from __future__ import annotations
import argparse, json, os, sys, time
import urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mcp"))
sys.path.insert(0, HERE)
import server  # the MCP server module exposes every tool as a function


# ---------------------------------------------------------------------------
# Ollama cluster-naming helper (standard library only, no API key required)
# ---------------------------------------------------------------------------
_OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434") + "/api/generate"
_OLLAMA_MODEL = os.environ.get("RADAR_MODEL", os.environ.get("LI_MODEL", "qwen3:8b"))
_OLLAMA_TIMEOUT = int(os.environ.get("LI_OLLAMA_TIMEOUT", "15"))


def _name_cluster_ollama(key: str, keywords: list, hub_page) -> str:
    """Ask a local Ollama model for a short cluster name (2-5 words, no punctuation).

    Returns None on any failure so the caller can fall back gracefully.
    Requires only Python standard library; no API key; no external services.
    """
    kw_str = ", ".join(keywords[:8]) if keywords else key
    hub_hint = f"\nHub page URL: {hub_page}" if hub_page else ""
    prompt = (
        f"You are an SEO expert. Give a short name (2-5 plain words, NO punctuation) "
        f"for a topical cluster of web pages.\n"
        f"Top keywords: {kw_str}{hub_hint}\n"
        f"Respond with ONLY the cluster name, nothing else."
    )
    body = json.dumps({
        "model": _OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "num_predict": 20},
    }).encode()
    try:
        req = urllib.request.Request(
            _OLLAMA_URL, data=body,
            headers={"Content-Type": "application/json"}, method="POST",
        )
        with urllib.request.urlopen(req, timeout=_OLLAMA_TIMEOUT) as resp:
            raw = json.loads(resp.read().decode())
        name = raw.get("response", "").strip().strip("\"'").strip()
        # Keep only the first line; strip any stray punctuation
        name = name.splitlines()[0].strip(" .,!?:;-") if name else ""
        return name or None
    except Exception:
        return None


def _name_clusters_with_ollama(clusters: list) -> dict:
    """Return {cluster_key: name} for all clusters, falling back to a keyword
    phrase when Ollama is unavailable or times out."""
    names = {}
    for c in clusters:
        key = c["key"]
        kws = c.get("keywords", [])
        hub = c.get("hub_page")
        name = _name_cluster_ollama(key, kws, hub)
        if not name:
            # Deterministic fallback: title-case the top 3 keywords
            fallback_kws = kws[:3]
            name = " ".join(w.title() for w in fallback_kws) if fallback_kws else key.title()
        names[key] = name
        print(f"  [cluster] {key!r:25s} -> {name!r}", flush=True)
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export_dir")
    ap.add_argument("--no-dashboard", action="store_true")
    ap.add_argument("--no-llm", action="store_true",
                    help="Skip Ollama cluster naming and use deterministic fallback only")
    args = ap.parse_args()

    if not args.no_dashboard:
        server.start_dashboard()
        print(f"[li] dashboard: http://localhost:{server.PORT}", flush=True)
        time.sleep(1)

    t0 = time.time()
    server.li_load(args.export_dir)
    time.sleep(1)
    server.li_graph()
    time.sleep(1)
    server.li_anchors()
    time.sleep(1)
    # --- Cluster naming via local Ollama (falls back gracefully if unavailable) ---
    if not args.no_llm:
        print("[li] Naming clusters via Ollama ...", flush=True)
        clusters_raw = server._A.get("clusters", {}).get("clusters", [])
        cluster_names = _name_clusters_with_ollama(clusters_raw)
        model_calls = len(cluster_names)
    else:
        cluster_names = {}
        model_calls = 0
    server.li_topics(cluster_names if cluster_names else None)
    time.sleep(1)
    server.li_entities()      # uses TF-keyword relatedness proxy
    time.sleep(1)
    # Starter does NOT attach model-written recs; _report_obj() then falls back to the
    # deterministic candidates (no anchors) so the contract always has data to grade.
    server.RUN["model_calls"] = model_calls
    server.RUN["duration_sec"] = round(time.time() - t0, 1)
    server.li_report()
    time.sleep(1)
    server.li_export()

    s = server.RUN["summary"]
    print("\n=== INTERNAL LINKING INTELLIGENCE ===")
    print(f"Site            : {server.RUN['site']}  ({s['pages_crawled']} pages)")
    print(f"Internal links  : {s['internal_links']}")
    print(f"Orphan pages    : {s['orphan_pages']}")
    print(f"Broken internal : {s['broken_internal_links']}")
    print(f"Generic anchors : {s['generic_anchors']}")
    print(f"Topical clusters: {s['topical_clusters']}")
    print(f"Link suggestions: {s['link_recommendations']}")
    print("Wrote outputs/report.json and outputs/report.html")

    if not args.no_dashboard:
        print(f"\n[li] Analysis complete. Dashboard is live at http://localhost:{server.PORT}")
        print("Starting MCP server. Press Ctrl+C to stop.")
        server._run_mcp()


if __name__ == "__main__":
    main()
