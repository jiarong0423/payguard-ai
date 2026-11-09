"""2026-11-10: the dispute write routes omit unset envelope fields, like the list and detail reads.

A live provide-evidence preview carried "note": null; the console's exact-key contract check refused it and the
recording stopped at "API contract mismatch". The fixture note is still set where it applies (list and detail reads).
"""
import unittest

from app.main import create_app


class DisputeWriteEnvelopeTest(unittest.TestCase):
    def test_write_routes_drop_unset_fields(self):
        app = create_app()
        routes = {route.path: route for route in app.routes if hasattr(route, "response_model_exclude_unset")}
        for path in ("/api/v1/paypal/disputes", "/api/v1/paypal/disputes/{dispute_id}",
                     "/api/v1/paypal/disputes/provide-evidence", "/api/v1/paypal/disputes/add-tracking"):
            self.assertTrue(routes[path].response_model_exclude_unset, path)


if __name__ == "__main__":
    unittest.main()
