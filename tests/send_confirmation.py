"""(r30 J2 P2-1) Test helper: a send carries the single-use confirmation from a preview, as the send dialog does.

The harnesses' post() route every submit:true call to provide-evidence or add-tracking through with_confirmation, so the
tests written before the server-side confirmation keep testing the gate they were written for. The confirmation itself
(missing, too early, reused, replaced) is tested in test_send_confirmation.py with plain posts.
"""

from unittest.mock import patch

SEND_ROUTES = ("/paypal/disputes/provide-evidence", "/paypal/disputes/add-tracking")


def with_confirmation(send, route, payload):
    """send(route, payload) posts without this helper. A preview that cannot issue a confirmation leaves the send
    without one, so the send meets the same refusal the preview met."""
    if route not in SEND_ROUTES or not isinstance(payload, dict) or payload.get("submit") is not True \
            or "confirm_token" in payload:
        return send(route, payload)
    preview = send(route, dict(payload, submit=False))
    token = preview.json().get("confirm_token") if preview.status_code == 200 else None
    # The dialog's 3-second hold is a wait for a person; these tests check the other gates, so the hold is 0 here.
    with patch("app.paypal_disputes.CONFIRM_HOLD_SECONDS", 0):
        return send(route, dict(payload, confirm_token=token))
