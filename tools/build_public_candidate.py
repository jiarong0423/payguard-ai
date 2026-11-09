#!/usr/bin/env python3
"""Build one default-deny TradeGlot public source candidate outside the source root."""

from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile

try:
    from validate_public_candidate import (
        DETACHED_NAME,
        LOCAL_EXPORT_STATUS,
        LOCAL_REMAINING_GATES,
        MANIFEST_NAME,
        PACKAGE_DIGEST_ALGORITHM,
        PUBLISHED_REMAINING_GATES,
        PUBLISHED_SOURCE_STATUS,
        validate_candidate,
    )
except ModuleNotFoundError:
    from tools.validate_public_candidate import (
        DETACHED_NAME,
        LOCAL_EXPORT_STATUS,
        LOCAL_REMAINING_GATES,
        MANIFEST_NAME,
        PACKAGE_DIGEST_ALGORITHM,
        PUBLISHED_REMAINING_GATES,
        PUBLISHED_SOURCE_STATUS,
        validate_candidate,
    )


PROJECT_ROOT = Path(__file__).absolute().parents[1]
MAX_FILE_BYTES = 2_000_000
ROOT_FILES = (
    ".dockerignore",
    ".gitignore",
    "Dockerfile",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    "pyproject.toml",
    "render.yaml",
    "requirements.lock",
)
EXACT_FILES = (
    # (optimise r24) Public CI: tests, console build and node contract tests on push and pull_request; no secrets.
    ".github/workflows/ci.yml",
    "backend/SECURITY.md",
    "data/country_rules/paypal_country_rules_v1.json",
    "data/country_rules/spotcheck_sample_20261110.json",
    "data/country_rules/spotcheck_results_20261110.json",
    "data/knowledge/payguard_us_official_v2/chunks.jsonl",
    "data/knowledge/payguard_us_official_v2/scenario_cards.v1.json",
    "data/knowledge/payguard_us_official_v2/sources.json",
    "docs/AG_STUDIO_NOTES.md",
    "docs/BRYNTUM_LICENSE_CHECK.md",
    "docs/CHANNEL3_NOTES.md",
    "docs/SPONSOR_TECH_MAP.md",
    "docs/MCP_SERVER.md",
    "docs/evidence/REVIEW_ZIP_CONTENTS.md",
    "docs/evidence/BRIEF_LIVE_RUN_20261109.md",
    "docs/evidence/APIMATIC_RUN_20261109.md",
    "docs/evidence/READBACK_20261109.md",
    "docs/evidence/IMPACT_SOURCES_20261109.md",
    "docs/evidence/SECOND_RATER_20261109.md",
    "docs/decisions/2026Q4/architecture.md",
    "docs/decisions/2026Q4/case_intake_contract.md",
    "docs/decisions/2026Q4/console_contract.md",
    "docs/decisions/2026Q4/policy_engine_v1.md",
    "docs/decisions/2026Q4/threat_model.md",
    "docs/decisions/2026Q4/us_mainline_contract.md",
    "docs/decisions/2026Q4/us_official_source_register.md",
    "docs/evidence/GEMINI_GUIDE_RUNS_20261103.md",
    "docs/evidence/RED_TEAM_ROUNDS_20261104.md",
    "docs/evidence/AI_DRIFT_CONTROL.md",
    # (review r25) The guide measurement records AI_DRIFT_CONTROL.md and the README cite, with the scorer and the
    # corpora it reads, so the published numbers can be checked against the frozen corpora.
    "docs/evidence/GUIDE_BENCHMARK.md",
    # (r34 E2 P1-1) tests/frontend_benchmark_chart.mjs reads the benchmark record behind the chart data.
    "docs/evidence/guide_benchmark_v1.json",
    "docs/evidence/GUIDE_STEPS12_LIVE.md",
    "docs/evidence/GUIDE_STRESS_TEST.md",
    "docs/evidence/RECEIPT_20261031_live.md",
    "docs/evidence/RECEIPT_20261104_live.md",
    "docs/evidence/RECEIPT_20261105_live.md",
    "docs/evidence/channel3_receipts_v1.json",
    "docs/evidence/channel3_receipts_20261109.json",
    "workflows/__init__.py",
    "workflows/evidence_integrity/__init__.py",
    "workflows/evidence_integrity/main.py",
    "workflows/evidence_integrity/requirements.txt",
    "workflows/evidence_integrity/tasks.py",
    "docs/RENDER_WORKFLOWS_NOTES.md",
    # (2026-11-08) Evidence and method files added so every public number can be reproduced or traced.
    "data/eval/checklist_answer_key_v1.json",
    "data/eval/checklist_answer_key_v2_heldout.json",
    "data/eval/second_rater_labels_v1_v2.json",
    "data/eval/PREREGISTRATION_v2.md",
    "docs/evidence/CHECKLIST_ANSWER_KEY_EVAL.md",
    "docs/evidence/HOW_NUMBERS_WERE_COUNTED.md",
    "docs/evidence/REAL_CASES_PUBLIC_20261108.md",
    "docs/evidence/RED_TEAM_ROUNDS_ADDENDUM_20261108.md",
    "docs/evidence/RULES_SPOTCHECK_20261108.md",
    "docs/evidence/PAYPAL_CLAUSES_SPOTCHECK_20261108.md",
    "docs/evidence/RULES_SPOTCHECK_20261110.md",
    "docs/evidence/TEST_RUN_20261108.md",
    "tools/eval_checklist_answer_key.py",
    "tools/compare_second_rater.py",
    "tools/export_api_docs.py",
    "docs/api/openapi.json",
    "docs/api/postman_collection.json",
    "docs/api/postman_readonly_subset.json",
    "docs/evidence/POSTMAN_RUN_20261109.md",
    "tools/mcp_interop_check.py",
    "tools/sandbox_readback_hash.py",
    "tools/verify_public_numbers.py",
    "docs/fallback/index.html",
    "docs/fallback/README.md",
    "docs/fallback/img/main_flow.gif",
    "docs/fallback/img/01_how_it_works.jpg",
    "docs/fallback/img/02_evidence_guide.jpg",
    "docs/fallback/img/03_review_zip.jpg",
    "docs/fallback/img/04_refusals_locked.jpg",
    "docs/fallback/img/05_ask_confirm.jpg",
    "docs/submission/quickstart.md",
    "docs/submission/devpost_story.md",
    "docs/submission/payguard_judge_overview.png",
    "docs/submission/diagrams/architecture_overview.png",
    "docs/submission/diagrams/architecture_simple.png",
    "docs/submission/diagrams/evidence_guide_funnel.png",
    "docs/submission/diagrams/paypal_write_guards.png",
    "docs/submission/diagrams/review_zip_verified.png",
    "docs/submission/diagrams/architecture_overview.svg",
    "docs/submission/diagrams/architecture_simple.svg",
    "docs/submission/diagrams/evidence_guide_funnel.svg",
    "docs/submission/diagrams/paypal_write_guards.svg",
    "docs/submission/diagrams/review_zip_verified.svg",
    "docs/submission/diagrams/architecture.mmd",
    "docs/submission/diagrams/paypal_write_guards.mmd",
    "docs/submission/payguard_judge_overview.svg",
    "docs/submission/screens/real_send_trace.png",
    "docs/submission/screens/refusals_locked.png",
    "docs/submission/screens/ag_studio_trace.png",
    "docs/submission/screens/delegate_confirm_popup.jpg",
    "docs/submission/screens/evidence_pages.png",
    "docs/submission/video_script.md",
    "frontend/index.html",
    "frontend/evidence.html",
    "frontend/dashboard.html",
    "frontend/scenarios.html",
    "frontend/proof.html",
    "frontend/package-lock.json",
    "frontend/package.json",
    "frontend/vite.config.js",
    "integrations/gemini/check_runtime.py",
    "integrations/gemini/pyproject.toml",
    "integrations/gemini/requirements.lock",
    "integrations/gemini/run.sh",
    "integrations/gemini/test_worker.py",
    "integrations/gemini/worker.py",
    "policies/US/paypal_aup_reference_v1/manifest.json",
    "policies/US/paypal_aup_reference_v1/source_index.json",
    "policies/registry.json",
    "tests/data/authored_replies_v1.json",
    "tests/data/evidence_guide_attack_v1.json",
    "tests/data/evidence_guide_heldout_preflight_v1.json",
    "tests/data/evidence_guide_heldout_preflight_v2.json",
    "tests/data/evidence_guide_heldout_v3.json",
    "tests/data/evidence_guide_heldout_velocity_v1.json",
    "tests/data/evidence_guide_heldout_velocity_v2.json",
    # test_guide_rounds measures the guide on these two held-out corpora (r14: the public test run errored without them).
    "tests/data/evidence_guide_heldout_v2.json",
    "tests/data/evidence_guide_heldout_v4.json",
    "tests/data/recorded_replies_v1.json",
    "tests/frontend_ag_charts_contract.mjs",
    "tests/frontend_ag_studio_contract.mjs",
    "tests/frontend_studio_agent.mjs",
    "tests/frontend_benchmark_chart.mjs",
    "tests/frontend_case_route_api.mjs",
    "tests/frontend_sent_files_api.mjs",
    "tests/frontend_country_rules.mjs",
    "tests/frontend_ai_contract.mjs",
    "tests/frontend_attack_r21_console.mjs",
    "tests/frontend_attack_r23_secondary.mjs",
    "tests/frontend_attack_r22_console.mjs",
    "tests/frontend_attack_r23_console.mjs",
    "tests/frontend_bryntum_board_contract.mjs",
    "tests/frontend_bryntum_board_render.mjs",
    "tests/frontend_bundle_budget.mjs",
    "tests/frontend_bryntum_render.mjs",
    "tests/frontend_guide_funnel_r30.mjs",
    "tests/frontend_guide_live_api.mjs",
    "tests/frontend_hosted_contract.mjs",
    "tests/frontend_hosted_readonly.mjs",
    "tests/frontend_try_example.mjs",
    "tests/frontend_recorded_replay.mjs",
    "tests/frontend_delegate_confirm.mjs",
    "tests/frontend_wording_20261108.mjs",
    "tests/frontend_topbar_sandbox_contract.mjs",
    "tests/frontend_operator_labels.mjs",
    "tests/frontend_optional_timeline.mjs",
    "tests/frontend_optimise_r24.mjs",
    "tests/frontend_product_confirmation.mjs",
    "tests/frontend_proof_contract.mjs",
    "tests/frontend_product_reference_api.mjs",
    "tests/frontend_pwa_contract.mjs",
    "tests/frontend_recording_contract.mjs",
    "tests/frontend_send_guard_r25.mjs",
    "tests/frontend_paypal_issue.mjs",
    "tests/frontend_receipt_parity.mjs",
    "tests/frontend_foolproof_20261104.mjs",
    "tests/frontend_send_confirm_r31.mjs",
    "tests/frontend_lock_reasons_r31.mjs",
    "tests/frontend_console_r32.mjs",
    "tests/frontend_console_r32_followup.mjs",
    "tests/frontend_ui_r33.mjs",
    "tests/frontend_ui_r34.mjs",
    "tests/frontend_scenarios_contract.mjs",
    "tests/frontend_start_here.mjs",
    "tests/frontend_time_evidence_api.mjs",
    "tests/frontend_tokens.mjs",
    "tests/frontend_type_scale.mjs",
    "tests/frontend_zip_api_parity.mjs",
    "tests/frontend_zip_contract.mjs",
    "tools/build_public_candidate.py",
    # Rebuilds the AG Studio dashboard data from the backend fixtures; tests/frontend_ag_studio_contract.mjs runs its --check.
    "tools/build_dashboard_data.py",
    # Operator-run: records one live run of Studio's built-in agents (local console, Gemini key) for the hosted replay.
    "tools/record_studio_agent_run.mjs",
    # Operator-run: records real Channel3 replies the hosted demo replays; documents how the recordings were made.
    "tools/record_channel3.py",
    # test_replays rebuilds the committed replay file with it and checks for drift.
    "tools/build_replays.py",
    # Re-extracts the evidence-page chart data; test_evidence_chart_data imports it (its Markdown sources are
    # not shipped, so the re-extraction tests skip in the public candidate and the totals checks still run).
    "tools/extract_evidence_charts.py",
    # guide_model loads instructions_v6 from this exact file in live mode; test_evidence_guide imports it.
    "tools/make_prompt_pack.py",
    "tools/public_run.sh",
    # Reproducible input-guard attack matrix; tests/test_redteam_input_matrix.py runs every round.
    "tools/redteam_input_matrix.py",
    # Offline scorer for recorded chooser replies against a frozen corpus (GUIDE_STRESS_TEST.md, GUIDE_STEPS12_LIVE.md).
    "tools/score_replies.py",
    "tools/validate_public_candidate.py",
)
TREE_FILES = {
    "backend/app": (
        "__init__.py", "ai_brief.py", "ai_usage.py", "case_routing.py", "channel3.py", "channel3_products.py", "country_routes.py", "demo_mode.py", "guide_model.py", "guide_routes.py",
        "lmstudio_brief.py", "main.py", "studio_agent.py", "paypal.py", "paypal_disputes.py", "paypal_tools.py", "schemas.py", "store.py", "traffic.py",
    ),
    "backend/app/data": ("channel3_recorded_v1.json",),
    # The whole frontend/public tree (PWA manifest, service worker, offline page, icons); a test keeps it complete.
    "frontend/public": (
        "icons/apple-touch-icon.png", "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-512.png",
        "icons/icon-maskable.svg", "icons/icon.svg", "manifest.webmanifest", "offline.html", "start.css", "start.html", "sw.js",
    ),
    "frontend/src": (
        "AnalyticsDashboard.css", "AnalyticsDashboard.jsx", "App.jsx", "CountryRules.css", "CountryRules.jsx", "GuideLive.css", "GuideLive.jsx",
        "GuideReplay.css", "GuideReplay.jsx", "RecordedSendReplay.css", "RecordedSendReplay.jsx", "hostedCopy.js", "PolicyPanel.jsx", "ProductReference.css", "ProductReference.jsx", "ReferencePanel.jsx", "api.js", "evidence.jsx", "index.css",
        "lockReasons.js", "main.jsx", "operatorLabels.js", "productConfirmation.js", "pseudonymizedExport.js", "pwa.css", "pwa.js", "referenceContract.js",
        "resumeNotice.js", "reviewZip.js", "sendConfirm.js", "tabKeys.js", "TimeEvidenceView.jsx",
    ),
    "frontend/src/board": ("EvidenceBoard.jsx", "board.css", "boardData.js"),
    "frontend/src/grid": ("agGrid.jsx",),
    "frontend/src/charts": ("BenchmarkCharts.jsx", "VelocityChart.jsx", "benchmarkChartData.js", "charts.css", "evidence.css", "velocityChartData.js"),
    "frontend/src/dashboard": ("DelegateConfirm.css", "DelegateConfirm.jsx", "agentRecording.js", "auditor.js", "dashboard.css", "dashboardData.js", "layout.js", "main.jsx", "studioAgentClient.js",
                               "theme.js", "widgets.jsx"),
    "frontend/src/data": ("blind_trend_v1.json", "channel3_receipts_v1.json", "dashboard_disputes_v1.json", "guide_benchmark_v1.json",
                          "guide_replays_v1.json", "proof_facts_v1.json", "stress_test_v1.json", "studio_agent_run_v1.json"),
    "frontend/src/proof": ("main.jsx", "proof.css", "proofData.js"),
    "frontend/src/scenarios": ("main.jsx", "scenarios.css", "workOrders.js"),
    "frontend/src/shared": ("asOf.js", "asOfSource.js", "sessionLedger.js"),
    "frontend/src/theme": ("base.css", "chartTheme.js", "format.js", "motion.js", "tokens.css", "tokens.js", "writeTokensCss.mjs"),
    "frontend/src/optional": (
        "OptionalTimeline.jsx", "TimeEvidenceWithTimeline.jsx", "timeline.css", "timelineModel.js",
        "vitePlugin.js",
    ),
    "src/payguard": (
        "__init__.py", "advisory_eval.py", "applicability.py", "case_cards.py",
        "case_contract.py", "case_intake.py", "cli.py", "controlled_fallback.py", "country_rules.py", "dispute_evidence.py",
        "evidence_guide.py",
        "document_privacy.py", "engines.py", "evidence_pdf.py", "ingest.py", "mcp_server.py", "policy.py", "privacy.py",
        "reference_policy.py", "reporting.py", "retrieval.py", "review.py",
    ),
    "tests": (
        "test_advisory_eval.py", "test_ai_api.py", "test_ai_brief.py", "test_api.py",
        "test_applicability.py", "test_boundaries.py", "test_case_cards.py", "test_case_routing.py", "test_channel3.py", "test_channel3_products.py",
        "test_case_intake.py", "test_console_static.py", "test_controlled_fallback.py", "test_country_rules.py", "test_demo_mode.py",
        "test_demo_mode_integration.py", "test_dispute_evidence.py", "test_document_privacy.py", "test_evidence_pdf.py", "test_export_api_docs.py", "test_mcp_server.py",
        "test_engines.py", "test_evidence_chart_data.py", "test_evidence_guide.py", "test_gemini_worker.py", "test_guide_hybrid.py", "test_guide_live_contract.py", "test_guide_rounds.py", "test_guide_routes.py",
        "test_hosted_claims_consistency.py", "test_hosted_readonly_sandbox.py", "test_sandbox_readback_hash.py", "test_hosted_image_layout.py", "test_lmstudio_brief.py",
        "test_paypal_disputes.py", "test_paypal_r24.py", "test_paypal_tools.py", "test_policy_api.py", "test_policy_gateway_integration.py",
        "test_public_export_builder.py", "test_redteam_input_matrix.py", "test_reference_api.py", "test_reference_policy.py", "test_replays.py",
        "test_retrieval.py", "test_sandbox_receipts.py", "test_studio_agent.py", "test_time_evidence.py", "test_traffic.py", "test_attack_r22.py", "test_attack_r23_aup.py",
        "test_optimise_r24.py", "test_r25_backend.py", "test_paypal_issue.py", "test_r26_guide.py",
        "send_confirmation.py", "test_send_confirmation.py", "test_r35_send_flow.py",
    ),
}
MAPPED_FILES = {"tools/run.sh": "tools/public_run.sh"}
EXECUTABLE_PATHS = {
    "integrations/gemini/run.sh",
    "tools/public_run.sh",
    "tools/run.sh",
}
# Kept out of the public package on purpose. Every file under AUDITED_TREES is either exported or listed
# here with a reason, so a new file can be neither shipped nor dropped silently (see the export tests).
EXCLUDED_WITH_REASON = {
    "tools/gemini_api_trial.py": "operator-run model trial against a live API; no test or runtime path needs it",
    "tests/test_svg_diagrams.py": "checks docs/architecture_gap_fill.svg, which is not in the public package, with the shipped overview SVG; C4 may ship both together",
    "tools/render_overview_png.cjs": "operator-run renderer for the committed overview PNG; needs Playwright and Chromium, which the package does not install",
    "tests/test_evidence_integrity_workflow.py": "tests workflows/evidence_integrity, which runs the excluded benchmark tools (run_guide_benchmark, simulate_guide_flow); not shipped",
    "tools/sandbox_scenarios.py": "operator-run scenario work orders against the owner's PayPal Sandbox app",
    "tools/sandbox_proof_run.py": "owner-run Sandbox proof run with the owner's credentials from the environment (network); writes masked receipts outside the package",
    "tools/country_rules_refresh.py": "maintainer-run refresh check for the country-rules pack; fetches official pages into isolation",
    "tools/country_rules_tables.py": "maintainer-run per-country tables of the country-rules pack, written to isolation",
    "tests/test_country_rules_refresh.py": "tests the maintainer-run refresh check, which is not shipped",
    "tests/test_gemini_api_trial.py": "tests tools/gemini_api_trial.py, which is itself excluded (operator-run live trial)",
    "tools/guide_live_turn.py": "operator-run single guide turn against a live model API; no test or runtime path needs it",
    "tools/vertex_trial.py": "operator-run model trial against a live API; no test or runtime path needs it",
    "tools/local_trial.py": "operator-run model trial against a local model; no test or runtime path needs it",
    "tools/trial_evidence_guide.py": "trial harness for the guide classifier; no test or runtime path needs it",
    "tools/score_keyword_chooser.py": "scores the keyword chooser on trial corpora via score_replies; no test or runtime path needs it",
    "tools/simulate_guide_flow.py": "offline whole-flow simulation over trial corpora; no test or runtime path needs it",
    "tools/example_retrieval.py": "evaluation-only retrieval over trial corpora; not used by the product",
    "tools/rag_eval.py": "evaluation-only comparison of retrieval strategies on blind corpora",
    "tools/run_guide_benchmark.py": "regenerates the benchmark JSON via the excluded simulation tool",
    "tools/compare_runs.py": "compares trial runs offline; no test or runtime path needs it",
    "tests/data/evidence_guide_trial_v1.json": "trial corpus; read only by excluded trial tools and the make_prompt_pack CLI; one refused-input item is a non-English sentence",
    "tests/data/evidence_guide_keyword_blind_v1.json": "blind keyword-chooser corpus; read only by the excluded score_keyword_chooser tool",
    "tests/data/evidence_guide_keyword_blind_v2.json": "blind keyword-chooser corpus; read only by the excluded score_keyword_chooser tool",
    "tests/data/evidence_guide_keyword_blind_v3.json": "blind keyword-chooser corpus; read only by the excluded score_keyword_chooser tool",
    "tests/data/evidence_guide_keyword_blind_v4.json": "blind whole-flow corpus; read only by the excluded simulation tools",
    "tests/data/evidence_guide_all_v1.json": "trial corpus; one refused-input item is a non-English sentence, so it stays with the private source",
    "docs/submission/DRAFT_readme_sections_r3.md": "owner-review draft of README text; the owner finalises public wording",
    "docs/submission/DRAFT_devpost_r3.md": "owner-review draft of Devpost text; the owner finalises public wording",
    "docs/submission/DRAFT_render_workflows_r5.md": "owner-review draft of the Render Workflows narration; the owner finalises public wording",
    "docs/submission/DRAFT_readme_r5.md": "owner-review draft of README text; the owner finalises public wording",
    "docs/submission/DRAFT_devpost_r5.md": "owner-review draft; the owner finalises public wording",
    "docs/submission/DRAFT_readme_sections_r5.md": "owner-review draft; the owner finalises public wording",
    "docs/submission/DRAFT_video_script_r5.md": "owner-review draft; the owner finalises public wording",
    "docs/submission/DRAFT_devpost_r6.md": "owner-review draft; the owner finalises public wording",
    "docs/submission/DRAFT_readme_sections_r6.md": "owner-review draft; the owner finalises public wording",
    "docs/submission/DRAFT_video_script_r6.md": "owner-review draft; the owner finalises public wording",
}
AUDITED_TREES = ("backend/app", "docs/submission", "frontend/public", "frontend/src", "src/payguard", "tests", "tools")
REQUIRED_RELEASE_UNIT_FILES = frozenset({
    "frontend/src/operatorLabels.js",
    "tests/frontend_operator_labels.mjs",
    "tests/frontend_recording_contract.mjs",
})


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def source_paths() -> tuple[str, ...]:
    paths = set(ROOT_FILES) | set(EXACT_FILES)
    for directory, names in TREE_FILES.items():
        paths.update(f"{directory}/{name}" for name in names)
    if any(path.startswith("integrations/paypal_toolkit/") for path in paths):
        raise RuntimeError("SOURCE_TOOLKIT_PROFILE_EXCLUDED")
    if len(paths) != sum(len(group) for group in (ROOT_FILES, EXACT_FILES)) + sum(len(names) for names in TREE_FILES.values()):
        raise RuntimeError("SOURCE_ALLOWLIST_DUPLICATE")
    missing_release_units = sorted(REQUIRED_RELEASE_UNIT_FILES - paths)
    if missing_release_units:
        raise RuntimeError(f"SOURCE_RELEASE_UNIT_MISSING:{','.join(missing_release_units)}")
    return tuple(sorted(paths))


PYTHON_PACKAGE_ROOTS = {"payguard": "src/payguard", "app": "backend/app", "tools": "tools"}
JS_SUFFIXES = (".js", ".jsx", ".mjs")
JS_RESOLVE = ("", ".js", ".jsx", ".mjs", ".json", "/index.js", "/index.jsx")
JS_IMPORT_PATTERNS = (
    # Static forms must start a line, so an import quoted inside a string literal is not one.
    re.compile(r"""^[ \t]*(?:import|export)\s[^'";]*?\bfrom\s*['"](\.{1,2}/[^'"]*)['"]""", re.MULTILINE),
    re.compile(r"""^[ \t]*import\s*['"](\.{1,2}/[^'"]*)['"]""", re.MULTILINE),
    re.compile(r"""\bimport\(\s*['"](\.{1,2}/[^'"]*)['"]\s*\)"""),
    re.compile(r"""\bnew\s+URL\(\s*['"](\.{1,2}/[^'"]+)['"]\s*,\s*import\.meta\.url"""),
)
# (r34 E2 P1-1) Shipped node tests read repository files by literal path (resolve(root, 'docs/...')); each must ship.
TEST_FILE_REFERENCE = re.compile(r"""\bresolve\(\s*(?:root|projectRoot)\s*,\s*['"]([^'"]+)['"]\s*\)""")
HTML_ROOT_REFERENCE = re.compile(r"""\b(?:src|href)\s*=\s*["'](/(?!/)[^"'?#]+)["']""")


def _python_module_files(root: str, parts: list[str]) -> tuple[str, str]:
    base = "/".join([root, *parts]) if parts else root
    return f"{base}.py", f"{base}/__init__.py"


def _python_import_targets(relative: str, payload: bytes, source_exists) -> list[tuple[str, tuple[str, ...]]]:
    """(import text, candidate files) for every import that names a module of this source tree."""
    tree = ast.parse(payload.decode("utf-8"), filename=relative)
    directory = PurePosixPath(relative).parent.as_posix()
    targets = []

    def local(module: str) -> tuple[str, list[str]] | None:
        parts = module.split(".")
        if parts[0] in PYTHON_PACKAGE_ROOTS:
            return PYTHON_PACKAGE_ROOTS[parts[0]], parts[1:]
        # Script-style imports: a sibling module, or a tools/ module the caller put on sys.path.
        for root in (directory, "tools"):
            if any(source_exists(path) for path in _python_module_files(root, parts[:1])):
                return root, parts
        return None

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                resolved = local(alias.name)
                if resolved is not None and resolved[1]:
                    targets.append((alias.name, _python_module_files(*resolved)))
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = PurePosixPath(relative).parent
                for _ in range(node.level - 1):
                    base = base.parent
                root, parts = base.as_posix(), node.module.split(".") if node.module else []
                label = "." * node.level + (node.module or "")
                if parts:
                    targets.append((label, _python_module_files(root, parts)))
            else:
                resolved = local(node.module or "")
                if resolved is None:
                    continue
                (root, parts), label = resolved, node.module
                # A bare package root (tools/ is a namespace package) is checked through its names below.
                if parts:
                    targets.append((label, _python_module_files(root, parts)))
            # "from package import name": when the name is a module file in the source, it must ship too.
            for alias in node.names:
                submodule = _python_module_files(root, [*parts, alias.name])
                if any(source_exists(path) for path in submodule):
                    targets.append((f"{label} import {alias.name}", submodule))
    return targets


def _js_import_targets(relative: str, payload: bytes) -> list[tuple[str, tuple[str, ...]]]:
    text = payload.decode("utf-8")
    directory = PurePosixPath(relative).parent.as_posix()
    targets = []
    for pattern in JS_IMPORT_PATTERNS:
        for match in pattern.finditer(text):
            specifier = match.group(1)
            if specifier.endswith("/"):
                continue
            joined = os.path.normpath(f"{directory}/{specifier}").replace(os.sep, "/")
            targets.append((specifier, tuple(joined + suffix for suffix in JS_RESOLVE)))
    return targets


def _test_file_targets(relative: str, payload: bytes) -> list[tuple[str, tuple[str, ...]]]:
    """Literal repository paths a shipped tests/*.mjs file reads through resolve(root, '...').

    Only paths that name a file of this source tree count (not directories, not the local .venv or node_modules,
    and not a file a test treats as optional because it is absent from the source).
    """
    if not (relative.startswith("tests/") and relative.endswith(".mjs")):
        return []
    targets = []
    for match in TEST_FILE_REFERENCE.finditer(payload.decode("utf-8")):
        path = os.path.normpath(match.group(1)).replace(os.sep, "/")
        if path.startswith((".venv/", "node_modules/", "frontend/node_modules/", "../")):
            continue
        if (PROJECT_ROOT / path).is_file():
            targets.append((path, (path,)))
    return targets


def _html_reference_targets(relative: str, payload: bytes) -> list[tuple[str, tuple[str, ...]]]:
    """Root-relative src/href in the console HTML: Vite serves them from frontend/ or frontend/public/."""
    if not relative.startswith("frontend/"):
        return []
    roots = ("frontend/public",) if relative.startswith("frontend/public/") else ("frontend", "frontend/public")
    return [(match.group(1), tuple(f"{root}{match.group(1)}" for root in roots))
            for match in HTML_ROOT_REFERENCE.finditer(payload.decode("utf-8"))]


def import_integrity_problems(payloads: dict[str, bytes], source_exists=None) -> list[str]:
    """Every local import in an exported .py/.js/.jsx/.mjs/.html file must resolve to an exported file.

    ``source_exists`` says whether a path exists in the source tree; it decides which bare Python names
    are local modules. Returns sorted ``"<file> -> <import>"`` problems; an empty list means intact.
    """
    exported = set(payloads)
    if source_exists is None:
        def source_exists(path: str) -> bool:
            return path in exported or (PROJECT_ROOT / path).is_file()
    problems = set()
    for relative, payload in payloads.items():
        try:
            if relative.endswith(".py"):
                targets = _python_import_targets(relative, payload, source_exists)
            elif relative.endswith(JS_SUFFIXES):
                targets = _js_import_targets(relative, payload) + _test_file_targets(relative, payload)
            elif relative.endswith(".html"):
                targets = _html_reference_targets(relative, payload)
            else:
                continue
        except (SyntaxError, UnicodeDecodeError, ValueError):
            problems.add(f"{relative} -> <unparseable>")
            continue
        for label, candidates in targets:
            if not any(candidate in exported for candidate in candidates):
                problems.add(f"{relative} -> {label}")
    return sorted(problems)


def assert_import_integrity(payloads: dict[str, bytes]) -> None:
    problems = import_integrity_problems(payloads)
    if problems:
        raise RuntimeError("SOURCE_IMPORT_UNRESOLVED:" + ";".join(problems))


def read_source(relative: str) -> tuple[bytes, int]:
    parts = Path(relative).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise RuntimeError(f"SOURCE_BOUNDARY_REJECTED:{relative}")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if nofollow is None or directory is None or os.open not in os.supports_dir_fd:
        raise RuntimeError("SOURCE_NOFOLLOW_UNAVAILABLE")
    directory_flags = os.O_RDONLY | directory | nofollow | getattr(os, "O_CLOEXEC", 0)
    file_flags = os.O_RDONLY | nofollow | getattr(os, "O_CLOEXEC", 0)
    descriptors: list[int] = []
    try:
        root_fd = os.open(PROJECT_ROOT, directory_flags)
        descriptors.append(root_fd)
        parent_fd = root_fd
        for part in parts[:-1]:
            parent_fd = os.open(part, directory_flags, dir_fd=parent_fd)
            descriptors.append(parent_fd)
        file_fd = os.open(parts[-1], file_flags, dir_fd=parent_fd)
        descriptors.append(file_fd)
        before = os.fstat(file_fd)
        if not stat.S_ISREG(before.st_mode):
            raise RuntimeError(f"SOURCE_BOUNDARY_REJECTED:{relative}")
        if before.st_size > MAX_FILE_BYTES:
            raise RuntimeError(f"SOURCE_SIZE_REJECTED:{relative}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(file_fd, min(65_536, MAX_FILE_BYTES + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > MAX_FILE_BYTES:
                raise RuntimeError(f"SOURCE_SIZE_REJECTED:{relative}")
        after = os.fstat(file_fd)
        identity_before = (
            before.st_dev, before.st_ino, before.st_mode, before.st_size,
            before.st_mtime_ns, before.st_ctime_ns,
        )
        identity_after = (
            after.st_dev, after.st_ino, after.st_mode, after.st_size,
            after.st_mtime_ns, after.st_ctime_ns,
        )
        payload = b"".join(chunks)
        if identity_before != identity_after or len(payload) != before.st_size:
            raise RuntimeError(f"SOURCE_READ_DRIFT:{relative}")
        return payload, stat.S_IMODE(before.st_mode)
    except RuntimeError:
        raise
    except OSError:
        raise RuntimeError(f"SOURCE_BOUNDARY_REJECTED:{relative}") from None
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def write_candidate_file(root: Path, relative: str, payload: bytes, mode: int) -> None:
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    target.chmod(0o755 if relative in EXECUTABLE_PATHS else mode & 0o666 or 0o644)


def package_digest(rows: list[dict]) -> str:
    payload = "".join(f"{row['sha256']}  {row['path']}\n" for row in sorted(rows, key=lambda item: item["path"])).encode("utf-8")
    return sha256_bytes(payload)


def build_candidate(destination: Path, *, published_source: bool = False) -> dict:
    if not isinstance(published_source, bool):
        raise RuntimeError("RELEASE_MODE_INVALID")
    source_root = PROJECT_ROOT.resolve()
    destination = destination.absolute()
    resolved_parent = destination.parent.resolve()
    projected = resolved_parent / destination.name
    if source_root == projected or source_root in projected.parents or projected in source_root.parents:
        raise RuntimeError("DESTINATION_MUST_BE_OUTSIDE_SOURCE_ROOT")
    if destination.exists() or destination.is_symlink():
        raise RuntimeError("DESTINATION_ALREADY_EXISTS")
    resolved_parent.mkdir(parents=True, exist_ok=True)

    snapshots: dict[str, tuple[bytes, int]] = {}
    for relative in source_paths():
        snapshots[relative] = read_source(relative)
    assert_import_integrity({relative: payload for relative, (payload, _mode) in snapshots.items()})

    with tempfile.TemporaryDirectory(prefix=f".{destination.name}-building-", dir=resolved_parent) as temporary:
        staging = Path(temporary) / "candidate"
        staging.mkdir()
        rows: list[dict] = []
        for relative in source_paths():
            payload, mode = snapshots[relative]
            write_candidate_file(staging, relative, payload, mode)
            rows.append({
                "path": relative,
                "bytes": len(payload),
                "sha256": sha256_bytes(payload),
                "source_path": relative,
                "source_sha256": sha256_bytes(payload),
            })
        for candidate_path, source_path in MAPPED_FILES.items():
            payload, mode = snapshots[source_path]
            write_candidate_file(staging, candidate_path, payload, mode)
            rows.append({
                "path": candidate_path,
                "bytes": len(payload),
                "sha256": sha256_bytes(payload),
                "source_path": source_path,
                "source_sha256": sha256_bytes(payload),
            })

        rows.sort(key=lambda item: item["path"])
        digest = package_digest(rows)
        row_map = {row["path"]: row for row in rows}
        dependency_locks = {
            "root_python": row_map["requirements.lock"]["sha256"],
            "gemini_python": row_map["integrations/gemini/requirements.lock"]["sha256"],
            "frontend_npm": row_map["frontend/package-lock.json"]["sha256"],
        }
        release_status = PUBLISHED_SOURCE_STATUS if published_source else LOCAL_EXPORT_STATUS
        remaining_gates = PUBLISHED_REMAINING_GATES if published_source else LOCAL_REMAINING_GATES
        manifest = {
            "schema_version": "payguard.public_export.v2",
            "status": release_status,
            "publication_authorized": published_source,
            "public_artifact_id": f"payguard-public-source-{digest[:16]}",
            "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "package_digest_algorithm": PACKAGE_DIGEST_ALGORITHM,
            "package_digest_sha256": digest,
            "file_count": len(rows),
            "files": rows,
            "dependency_locks": dependency_locks,
            "owner_attestation": {
                "accepted": True,
                "scope": "RECORDED_OWNER_RIGHTS_AND_ENTRANT_ELIGIBILITY",
            },
            "raw_bounded_prompt_disclosure": {
                "intent": "INTENTIONAL_PUBLIC_EXECUTABLE_PRODUCT_SOURCE",
                "path": "backend/app/ai_brief.py",
                "sha256": row_map["backend/app/ai_brief.py"]["sha256"],
            },
            "remaining_gates": list(remaining_gates),
        }
        manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
        manifest_hash = sha256_bytes(manifest_bytes)
        write_candidate_file(staging, MANIFEST_NAME, manifest_bytes, 0o644)
        write_candidate_file(staging, DETACHED_NAME, f"{manifest_hash}  {MANIFEST_NAME}\n".encode("ascii"), 0o644)

        for relative, (payload, _mode) in snapshots.items():
            if read_source(relative)[0] != payload:
                raise RuntimeError(f"SOURCE_DRIFT:{relative}")

        result = validate_candidate(staging)
        staging.rename(destination)
        return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--published-source",
        action="store_true",
        help="record an already completed public-source publication transition",
    )
    parser.add_argument("destination", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = build_candidate(args.destination, published_source=args.published_source)
    except (OSError, RuntimeError, ValueError) as error:
        print(json.dumps({"status": "FAILED", "reason": str(error)}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
