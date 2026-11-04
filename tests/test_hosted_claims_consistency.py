"""(r34 #1) The public text about the hosted demo agrees with the code that runs it.

Owner decision 2026-11-04: the hosted demo keeps the opt-in Gemini guide. The guide's hosted caps and the disabled
provider routes are read from the backend constants, and README, SECURITY, the Devpost story, AI_DRIFT_CONTROL,
quickstart and render.yaml must state the same numbers and must not carry the old absolute "no Gemini" phrases.
No network, no environment file, no provider call.
"""

from pathlib import Path
import re
import unittest

from app import guide_routes
from app.demo_mode import DISABLED_ROUTES

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PER_MINUTE = guide_routes.HOSTED_GUIDE_CALLS_PER_MINUTE
PER_DAY = guide_routes.HOSTED_GUIDE_CALLS_PER_DAY
CAPS_PHRASE = f"at most {PER_MINUTE} calls a minute and {PER_DAY} a day"
PUBLIC_TEXTS = (
    "README.md",
    "SECURITY.md",
    "docs/submission/devpost_story.md",
    "docs/submission/quickstart.md",
    "docs/evidence/AI_DRIFT_CONTROL.md",
    "render.yaml",
)
# Absolute claims that stopped being true when the hosted guide's Gemini opt-in was turned on (2026-11-04).
STALE_PHRASES = (
    "rules-only hosted demo",
    "hosted demo (rules-only)",
    "never calls a model",
    "never a model",
    "no paypal or gemini call",
    "makes no paypal, gemini",
    "needs no keys and must not be given any",
    "the hosted demo makes no model call",
    "the hosted demo makes no provider call",
    "it holds no credential, and every provider",
    "gemini and local-model calls are disabled",
    "do not add paypal, gemini or google credentials",
)
# How each disabled route is named in README "Hosted demo" and in SECURITY.md. A new disabled route fails here
# until both documents name it.
ROUTE_NAMES = {
    ("POST", "/api/v1/paypal/connect"): ("**Connect US Sandbox**", "Sandbox connect"),
    ("POST", "/api/v1/paypal/invoices/draft"): ("the invoice draft", "invoice draft"),
    ("POST", "/api/v1/paypal/disputes/provide-evidence"): ("`provide-evidence`", "provide-evidence"),
    ("POST", "/api/v1/paypal/disputes/add-tracking"): ("`add-tracking`", "add-tracking"),
    ("POST", "/api/v1/paypal/webhooks/verify"): ("webhook verification", "webhook verification"),
    ("POST", "/api/v1/ai/evidence-brief"): ("**Generate AI brief**", "AI brief"),
    ("POST", "/api/v1/studio/agent-turn"): ("the AG Studio agent turn", "the AG Studio agent turn"),
}
OPT_IN_KEYS = ("PAYGUARD_HOSTED_GUIDE_MODEL", "PAYGUARD_GUIDE_MODEL", "PAYGUARD_GEMINI_TRANSPORT", "GEMINI_API_KEY")


def read(relative: str) -> str:
    return (PROJECT_ROOT / relative).read_text(encoding="utf-8")


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).casefold()


class HostedClaimsConsistencyTests(unittest.TestCase):
    def test_caps_in_code_are_the_free_tier_numbers_the_docs_state(self):
        self.assertEqual((PER_MINUTE, PER_DAY), (5, 20), "change README, SECURITY and the Devpost story with the caps")
        self.assertEqual(guide_routes.HOSTED_GUIDE_MODEL_ENV, "PAYGUARD_HOSTED_GUIDE_MODEL")

    def test_readme_security_devpost_and_drift_state_the_same_caps(self):
        for relative in ("README.md", "SECURITY.md", "docs/submission/devpost_story.md",
                         "docs/evidence/AI_DRIFT_CONTROL.md", "docs/submission/quickstart.md"):
            with self.subTest(relative=relative):
                self.assertIn(CAPS_PHRASE, flat(read(relative)))

    def test_readme_names_the_cap_constants_and_the_opt_in_switch(self):
        readme = read("README.md")
        for name in ("HOSTED_GUIDE_CALLS_PER_MINUTE", "HOSTED_GUIDE_CALLS_PER_DAY",
                     f"{guide_routes.HOSTED_GUIDE_MODEL_ENV}=gemini"):
            self.assertIn(name, readme)
        self.assertIn(f"{guide_routes.HOSTED_GUIDE_MODEL_ENV}=gemini", read("SECURITY.md"))

    def test_no_public_text_keeps_the_old_absolute_claims(self):
        for relative in PUBLIC_TEXTS:
            text = flat(read(relative))
            for phrase in STALE_PHRASES:
                with self.subTest(relative=relative, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_disabled_routes_match_the_documented_list(self):
        self.assertEqual(set(ROUTE_NAMES), set(DISABLED_ROUTES), "document each disabled route in README and SECURITY")
        readme, security = read("README.md"), read("SECURITY.md")
        for route, (readme_name, security_name) in ROUTE_NAMES.items():
            with self.subTest(route=route):
                self.assertIn(readme_name, readme)
                self.assertIn(security_name, security)
        # Only the guide may reach a model on the hosted demo: the brief and Studio routes stay refused,
        # and no guide route is in the refused set.
        self.assertIn(("POST", "/api/v1/ai/evidence-brief"), DISABLED_ROUTES)
        self.assertIn(("POST", "/api/v1/studio/agent-turn"), DISABLED_ROUTES)
        self.assertFalse(any("/guide/" in path for _method, path in DISABLED_ROUTES))

    def test_render_blueprint_declares_the_opt_in_without_values(self):
        blueprint = read("render.yaml")
        for key in OPT_IN_KEYS:
            with self.subTest(key=key):
                block = re.search(rf"^      - key: {key}\n((?:        .*\n)+)", blueprint, re.MULTILINE)
                self.assertIsNotNone(block, f"{key} declared")
                self.assertEqual(block.group(1).strip(), "sync: false", f"{key} has no value in the file")
        self.assertIn("at most 5 calls a minute and 20 a day", flat(blueprint))
        self.assertNotRegex(blueprint, r"AIza[0-9A-Za-z_-]{20,}")


if __name__ == "__main__":
    unittest.main()
