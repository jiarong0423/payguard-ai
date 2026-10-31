"""Time evidence and digital delivery proof: ordering and preserving, never judging.

PayGuard keeps payment time, order-record time, message records (keyed digest and a
closed topic, never text), delivery time and claim time, and computes the gaps. It
makes no statement about intent or outcome.
"""

import hashlib
import json
import unittest

from payguard.dispute_evidence import (
    DisputeEvidenceError,
    build_time_evidence,
    message_digest,
    resolve_dispute_requirements,
)


KEY = b"synthetic-test-key-0123456789abcdef"
DIGEST_A = "a" * 64
DIGEST_B = "b" * 64

TIMES = {
    "payment_at": "2026-10-28T03:00:00Z",
    "order_record_at": "2026-10-28T09:00:00Z",
    "delivered_at": "2026-10-31T06:00:00Z",
    "claim_at": "2026-10-30T04:00:00Z",
}


def comm(channel="EMAIL", direction="INBOUND", sent_at="2026-10-28T03:30:00Z",
         topic="PAYMENT_NOTICE", digest=DIGEST_A):
    return {"channel": channel, "direction": direction, "sent_at": sent_at,
            "topic": topic, "message_digest": digest}


def comms():
    return [
        comm("EMAIL", "INBOUND", "2026-10-28T03:30:00Z", "PAYMENT_NOTICE", DIGEST_A),
        comm("EMAIL", "OUTBOUND", "2026-10-28T08:00:00Z", "ORDER_DETAILS_REQUEST", DIGEST_B),
        comm("PRIVATE_MESSAGE", "INBOUND", "2026-10-28T08:40:00Z", "ORDER_DETAILS_PROVIDED", "c" * 64),
        comm("EMAIL", "OUTBOUND", "2026-10-31T06:00:00Z", "DELIVERY_NOTICE", "d" * 64),
    ]


def times(**changes):
    value = dict(TIMES)
    value.update(changes)
    return value


class TimeEvidenceTests(unittest.TestCase):
    def assert_code(self, operation, code="time_evidence_invalid"):
        with self.assertRaises(DisputeEvidenceError) as result:
            operation()
        self.assertEqual(str(result.exception), code)
        self.assertIsNone(result.exception.__cause__)

    def test_gap_case_orders_events_computes_gaps_and_flags_delivery_after_claim(self):
        result = build_time_evidence(times(), comms())
        kinds = [event["kind"] for event in result["events"]]
        self.assertEqual(kinds[0], "PAYMENT")
        self.assertEqual(kinds[-1], "DELIVERY")
        stamps = [event["at"] for event in result["events"]]
        self.assertEqual(stamps, sorted(stamps))
        self.assertEqual(result["gaps_seconds"], {
            "payment_to_order_record": 21600,
            "payment_to_delivery": 3 * 86400 + 3 * 3600,
            "delivery_to_claim": -(86400 + 2 * 3600),
            "payment_to_claim": 2 * 86400 + 3600,
        })
        self.assertEqual(result["flags"], ["DELIVERY_AFTER_CLAIM"])
        self.assertEqual(result["judgement"], "NOT_MADE")
        self.assertIs(result["advisory_only"], True)

    def test_every_event_carries_a_source_and_only_the_claim_is_provider_sourced(self):
        result = build_time_evidence(times(), comms())
        sources = {event["kind"]: event["source"] for event in result["events"]}
        self.assertEqual(sources["CLAIM_OPENED"], "PROVIDER")
        for kind in ("PAYMENT", "ORDER_RECORD_CREATED", "DELIVERY", "MESSAGE"):
            self.assertEqual(sources[kind], "SELLER_PROVIDED_UNVERIFIED")

    def test_missing_order_record_and_missing_delivery_are_flagged_not_guessed(self):
        result = build_time_evidence(times(order_record_at=None, delivered_at=None), [])
        self.assertEqual(result["flags"], ["DELIVERY_NOT_RECORDED", "ORDER_RECORD_ABSENT"])
        self.assertIsNone(result["gaps_seconds"]["payment_to_order_record"])
        self.assertIsNone(result["gaps_seconds"]["payment_to_delivery"])
        self.assertIsNone(result["gaps_seconds"]["delivery_to_claim"])
        self.assertEqual(result["gaps_seconds"]["payment_to_claim"], 2 * 86400 + 3600)
        self.assertNotIn("ORDER_RECORD_CREATED", [e["kind"] for e in result["events"]])

    def test_claim_time_earlier_than_payment_time_is_a_neutral_timestamp_flag(self):
        result = build_time_evidence(times(claim_at="2026-10-27T00:00:00Z", delivered_at="2026-10-31T06:00:00Z"), [])
        self.assertIn("CLAIM_TIME_EARLIER_THAN_PAYMENT_TIME", result["flags"])
        self.assertLess(result["gaps_seconds"]["payment_to_claim"], 0)

    def test_delivery_before_claim_has_no_delivery_flag(self):
        result = build_time_evidence(times(delivered_at="2026-10-29T06:00:00Z"), [])
        self.assertEqual(result["flags"], [])
        self.assertEqual(result["gaps_seconds"]["delivery_to_claim"], 22 * 3600)

    def test_ties_keep_a_fixed_kind_order(self):
        same = "2026-10-28T03:00:00Z"
        result = build_time_evidence(times(order_record_at=same, delivered_at=None, claim_at=same), [])
        self.assertEqual([e["kind"] for e in result["events"]],
                         ["PAYMENT", "ORDER_RECORD_CREATED", "CLAIM_OPENED"])

    def test_naive_and_malformed_times_are_rejected(self):
        for field, value in (("payment_at", "2026-10-28T03:00:00"), ("claim_at", "yesterday"),
                             ("delivered_at", 12345), ("order_record_at", "2026-10-28 09:00:00Z")):
            self.assert_code(lambda: build_time_evidence(times(**{field: value}), []))

    def test_required_times_must_be_present_and_keys_are_closed(self):
        self.assert_code(lambda: build_time_evidence(times(payment_at=None), []))
        self.assert_code(lambda: build_time_evidence(times(claim_at=None), []))
        extra = times()
        extra["intent"] = "deliberate"
        self.assert_code(lambda: build_time_evidence(extra, []))
        missing = times()
        del missing["delivered_at"]
        self.assert_code(lambda: build_time_evidence(missing, []))

    def test_message_records_are_closed_and_cannot_carry_text(self):
        for bad in (
            dict(comm(), body="please refund me"),
            dict(comm(), summary="buyer says paid"),
            {key: value for key, value in comm().items() if key != "topic"},
            comm(channel="SMS"),
            comm(direction="SIDEWAYS"),
            comm(topic="BUYER_IS_LYING"),
            comm(digest="A" * 64),
            comm(digest="a" * 63),
            comm(digest="not a digest"),
            comm(sent_at="2026-10-28T03:30:00"),
        ):
            self.assert_code(lambda bad=bad: build_time_evidence(times(), [bad]))

    def test_message_list_is_bounded_and_must_be_a_list(self):
        self.assert_code(lambda: build_time_evidence(times(), [comm()] * 21))
        self.assert_code(lambda: build_time_evidence(times(), "none"))
        self.assertEqual(len(build_time_evidence(times(), [comm()] * 20)["events"]), 4 + 20)

    def test_output_has_no_text_fields_and_no_intent_field(self):
        result = build_time_evidence(times(), comms())
        serialized = json.dumps(result)
        for forbidden in ("summary", "body", "text", "intent", "fraud", "deliberate", "winner"):
            self.assertNotIn(forbidden, serialized.lower())
        for event in result["events"]:
            self.assertLessEqual(set(event), {"kind", "at", "source", "channel", "direction", "topic", "message_digest"})

    def test_input_is_not_mutated_and_output_is_a_copy(self):
        original_times, original_comms = times(), comms()
        build_time_evidence(original_times, original_comms)
        self.assertEqual(original_times, times())
        self.assertEqual(original_comms, comms())


class MessageDigestTests(unittest.TestCase):
    def test_digest_is_keyed_deterministic_hex_and_not_a_plain_hash(self):
        digest = message_digest(KEY, "Hello, I paid yesterday.")
        self.assertRegex(digest, r"^[0-9a-f]{64}$")
        self.assertEqual(digest, message_digest(KEY, "Hello, I paid yesterday."))
        self.assertNotEqual(digest, message_digest(b"another-synthetic-key-0123456789ab", "Hello, I paid yesterday."))
        self.assertNotEqual(digest, hashlib.sha256(b"Hello, I paid yesterday.").hexdigest())

    def test_unicode_is_normalised_and_short_keys_or_empty_text_are_rejected(self):
        self.assertEqual(message_digest(KEY, "Ｈello"), message_digest(KEY, "Hello"))
        for key, text in ((b"short", "x"), (KEY, ""), (KEY, "   "), (KEY, "x" * 20001), ("not bytes", "x"), (KEY, 5)):
            with self.assertRaises(DisputeEvidenceError) as result:
                message_digest(key, text)
            self.assertEqual(str(result.exception), "message_digest_invalid")


def digital_snapshot():
    return {
        "schema_version": 1,
        "snapshot_class": "SYNTHETIC_PROVIDER_FIXTURE",
        "observed_at": "2026-10-31T08:00:00Z",
        "dispute_id": "demo-case-002",
        "order_id": "demo-dispute-order-002",
        "reason": "MERCHANDISE_OR_SERVICE_NOT_RECEIVED",
        "status": "WAITING_FOR_SELLER_RESPONSE",
        "dispute_life_cycle_stage": "INQUIRY",
        "seller_response_due_date": "2026-11-02T08:00:00Z",
        "available_actions": ["PROVIDE_EVIDENCE"],
        "evidences": [{
            "request_id": "request-fulfillment-002",
            "evidence_type": "PROOF_OF_FULFILLMENT",
            "source": "REQUESTED_FROM_SELLER",
            "mandatory": True,
            "action": "PROVIDE_EVIDENCE",
        }],
    }


def digital_proof(fields):
    return {
        "evidence_id": "proof-fulfillment-002",
        "request_id": "request-fulfillment-002",
        "evidence_type": "FULFILLMENT",
        "proof_fields": fields,
        "observed_at": "2026-10-31T08:30:00Z",
        "evidence_state": "SUPPLIED_UNVERIFIED",
        "attachment_ids": [],
    }


class DigitalDeliveryProofTests(unittest.TestCase):
    def resolve(self, fields):
        return resolve_dispute_requirements(digital_snapshot(), [digital_proof(fields)], [], "2026-10-31T09:00:00Z")

    def test_digital_delivery_can_satisfy_a_fulfilment_request(self):
        result = self.resolve({"delivery_channel": "EMAIL_LINK", "delivered_at": "2026-10-31T06:00:00Z"})
        self.assertEqual(result["routing"]["requirements"][0]["requirement_state"], "STRUCTURALLY_PRESENT")
        self.assertNotIn("EMAIL_LINK", json.dumps(result["routing"]))

    def test_physical_tracking_still_satisfies_it(self):
        result = self.resolve({"carrier_name": "USPS", "tracking_number": "SYNTHETICTRACK002"})
        self.assertEqual(result["routing"]["requirements"][0]["requirement_state"], "STRUCTURALLY_PRESENT")

    def test_partial_or_mixed_or_unknown_fields_are_rejected(self):
        for fields in (
            {"delivery_channel": "EMAIL_LINK"},
            {"delivered_at": "2026-10-31T06:00:00Z"},
            {"carrier_name": "USPS"},
            {"tracking_number": "SYNTHETICTRACK002"},
            {"delivery_channel": "carrier pigeon", "delivered_at": "2026-10-31T06:00:00Z"},
            {"delivery_channel": "EMAIL_LINK", "delivered_at": "2026-10-31T06:00:00"},
            {"delivery_channel": "EMAIL_LINK", "delivered_at": "2026-10-31T06:00:00Z", "buyer_email": "x@example.invalid"},
            {},
        ):
            with self.assertRaises(DisputeEvidenceError, msg=str(fields)):
                self.resolve(fields)


if __name__ == "__main__":
    unittest.main()
