"""Offline receipt proof: every successful HTTP result here is synthetic."""
import asyncio
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
import socket
import unittest
from unittest.mock import patch
import httpx
from pydantic import ValidationError
from app.paypal import PaypalAdapter, PaypalConfig, operator_config
from app.schemas import SandboxEvidenceReceipt, PaypalStatusResponse, InvoiceDraftResponse
from app.store import BoundaryError, SessionStore, utc_now
from app.paypal_tools import SafePaypalToolGateway

FIELDS = {'schema_version','environment','action','status','observed_at','invoice_id','evidence_class','proof_kind','separate_get_readback','external_send'}

class ReceiptTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.now = datetime(2026, 10, 6, 0, 0, tzinfo=timezone.utc)
        self.calls = []
        self.oauth = {'access_token':'synthetic-token','token_type':'Bearer','expires_in':120,
                      'account':'private-account-marker','email':'private@example.invalid'}
        self.invoice = {'id':'INV2-SYNTHETIC-0001','status':'DRAFT','payer':'private@example.invalid',
                        'headers':'private-header-marker','description':'private-body-marker'}
        self.fail = False
        def handler(request):
            self.calls.append((request.method, request.url.path))
            if self.fail:
                return httpx.Response(401, json={'secret':'private-error-marker'})
            return httpx.Response(200, json=self.oauth if request.url.path == '/v1/oauth2/token' else self.invoice)
        self.adapter = PaypalAdapter(config_loader=lambda: PaypalConfig(True,'synthetic-id','synthetic-secret'),
                                     transport=httpx.MockTransport(handler), clock=lambda:self.now)
        self.network = [patch.object(socket.socket,'connect',side_effect=AssertionError('network forbidden')),
                        patch.object(socket,'create_connection',side_effect=AssertionError('network forbidden'))]
        for p in self.network:p.start();self.addCleanup(p.stop)

    def assert_receipt(self, value, action, invoice=None):
        self.assertEqual(set(value), FIELDS)
        self.assertEqual(value['evidence_class'],'SYNTHETIC_TEST_RESPONSE')
        self.assertEqual(value['action'],action)
        self.assertEqual(value['invoice_id'],invoice)
        self.assertEqual(value['proof_kind'],'POST_RESPONSE_ONLY')
        self.assertIs(value['separate_get_readback'],False)
        self.assertEqual(value['external_send'],'FROZEN')
        SandboxEvidenceReceipt.model_validate(value)
        encoded=json.dumps(value)
        for marker in ('synthetic-token','synthetic-id','synthetic-secret','private-account-marker','private@example.invalid',
                       'private-header-marker','private-body-marker','private-error-marker'):
            self.assertNotIn(marker,encoded)

    async def test_no_receipt_or_network_before_explicit_connect(self):
        response=self.adapter.status()
        self.assertIsNone(response['evidence_receipt'])
        self.assertEqual(self.calls,[])
        PaypalStatusResponse.model_validate(response)

    async def test_connect_receipt_is_synthetic_sanitized_and_detached(self):
        response=await self.adapter.connect()
        self.assert_receipt(response['evidence_receipt'],'OAUTH_CONNECT')
        self.assertEqual(response['last_verified_at'],response['evidence_receipt']['observed_at'])
        self.assertEqual(self.calls,[('POST','/v1/oauth2/token')])
        response['evidence_receipt']['evidence_class']='AUTHENTIC_SANDBOX_RESPONSE'
        self.assertEqual(self.adapter.status()['evidence_receipt']['evidence_class'],'SYNTHETIC_TEST_RESPONSE')
        self.assertEqual(self.adapter.open_clients,0)

    async def test_expiry_and_failed_reconnect_revoke_connection_receipt(self):
        await self.adapter.connect();self.now+=timedelta(seconds=120)
        self.assertIsNone(self.adapter.status()['evidence_receipt'])
        await self.adapter.connect();self.fail=True
        with self.assertRaises(BoundaryError):await self.adapter.connect()
        response=self.adapter.status();self.assertEqual(response['status'],'error')
        self.assertIsNone(response['evidence_receipt']);self.assertIsNone(response['last_verified_at'])
        PaypalStatusResponse.model_validate(response)

    async def test_loader_failure_after_success_revokes_every_connection_artifact_before_loader_call(self):
        await self.adapter.connect()
        calls=len(self.calls)
        def broken_loader():
            raise RuntimeError('private-loader-marker')
        self.adapter.config_loader=broken_loader
        with self.assertRaises(BoundaryError) as caught:
            await self.adapter.connect()
        self.assertEqual((caught.exception.status,caught.exception.code),(503,'provider_not_configured'))
        self.assertIsNone(caught.exception.__cause__)
        self.assertNotIn('private-loader-marker',str(caught.exception))
        self.assertEqual(len(self.calls),calls)
        self.assertIsNone(self.adapter._access_token)
        self.assertIsNone(self.adapter._token_expiry)
        self.assertIsNone(self.adapter._last_verified_at)
        self.assertIsNone(self.adapter._connection_receipt)
        self.assertEqual(self.adapter._status,'not_configured')
        response=self.adapter.status()
        self.assertNotEqual(response['status'],'connected')
        self.assertIsNone(response['evidence_receipt'])
        self.assertIsNone(response['last_verified_at'])
        self.assertEqual(self.adapter.open_clients,0)

    async def test_bad_loader_clock_and_provider_exception_after_success_fail_closed_and_sanitized(self):
        good_loader=lambda:PaypalConfig(True,'synthetic-id','synthetic-secret')
        good_transport=self.adapter.transport
        good_clock=lambda:self.now

        async def connect_good():
            self.adapter.config_loader=good_loader
            self.adapter.transport=good_transport
            self.adapter.clock=good_clock
            result=await self.adapter.connect()
            self.assertEqual(result['status'],'connected')

        def assert_revoked(expected_status):
            self.assertEqual(self.adapter._status,expected_status)
            self.assertIsNone(self.adapter._access_token)
            self.assertIsNone(self.adapter._token_expiry)
            self.assertIsNone(self.adapter._last_verified_at)
            self.assertIsNone(self.adapter._connection_receipt)
            response=self.adapter.status()
            self.assertNotEqual(response['status'],'connected')
            self.assertIsNone(response['evidence_receipt'])
            self.assertIsNone(response['last_verified_at'])
            self.assertEqual(self.adapter.open_clients,0)

        await connect_good();calls=len(self.calls)
        self.adapter.config_loader=lambda:{'enabled':True}
        with self.assertRaises(BoundaryError) as bad_loader:
            await self.adapter.connect()
        self.assertEqual((bad_loader.exception.status,bad_loader.exception.code),(503,'provider_not_configured'))
        self.assertIsNone(bad_loader.exception.__cause__)
        self.assertEqual(len(self.calls),calls)
        assert_revoked('not_configured')

        await connect_good();calls=len(self.calls)
        def broken_clock():
            raise RuntimeError('private-clock-marker')
        self.adapter.clock=broken_clock
        with self.assertRaises(BoundaryError) as bad_clock:
            await self.adapter.connect()
        self.assertEqual((bad_clock.exception.status,bad_clock.exception.code),(503,'clock_unavailable'))
        self.assertIsNone(bad_clock.exception.__cause__)
        self.assertNotIn('private-clock-marker',str(bad_clock.exception))
        self.assertEqual(len(self.calls),calls)
        assert_revoked('not_configured')

        await connect_good();calls=len(self.calls);provider_attempts=[]
        def broken_provider(request):
            provider_attempts.append((request.method,request.url.path))
            raise RuntimeError('private-provider-marker')
        self.adapter.transport=httpx.MockTransport(broken_provider)
        with self.assertRaises(BoundaryError) as bad_provider:
            await self.adapter.connect()
        self.assertEqual((bad_provider.exception.status,bad_provider.exception.code),(502,'provider_upstream_failure'))
        self.assertIsNone(bad_provider.exception.__cause__)
        self.assertNotIn('private-provider-marker',str(bad_provider.exception))
        self.assertEqual(len(self.calls),calls)
        self.assertEqual(provider_attempts,[('POST','/v1/oauth2/token')])
        assert_revoked('error')

    def assert_every_connection_field_revoked(self, status, open_clients=0):
        self.assertEqual(self.adapter._config, PaypalConfig())
        for name in ('_access_token', '_token_expiry', '_last_verified_at', '_connection_receipt'):
            self.assertIsNone(getattr(self.adapter, name), name)
        self.assertEqual(self.adapter._status, status)
        self.assertEqual(self.adapter.open_clients, open_clients)
        response = self.adapter.status()
        self.assertIs(response['configured'], False)
        self.assertIsNone(response['last_verified_at'])
        self.assertIsNone(response['evidence_receipt'])

    async def test_connect_never_runs_third_clock_or_status_after_commit(self):
        await self.adapter.connect()
        calls = 0
        def third_fails():
            nonlocal calls
            calls += 1
            if calls == 3:
                raise RuntimeError('private-third-clock-marker')
            return self.now
        self.adapter.clock = third_fails
        with patch.object(self.adapter, 'status', side_effect=AssertionError('post-commit status forbidden')):
            response = await self.adapter.connect()
        self.assertEqual(calls, 2)
        self.assertEqual(response['status'], 'connected')
        self.assert_receipt(response['evidence_receipt'], 'OAUTH_CONNECT')
        with self.assertRaises(BoundaryError) as caught:
            self.adapter.status()
        self.assertEqual((caught.exception.status, caught.exception.code), (503, 'clock_unavailable'))
        self.assertIsNone(caught.exception.__cause__)
        self.assertNotIn('private-third', str(caught.exception))
        self.assert_every_connection_field_revoked('not_configured')

    async def test_status_clock_failure_revokes_config_token_and_all_evidence(self):
        await self.adapter.connect()
        calls = len(self.calls)
        def broken():
            raise RuntimeError('private-status-clock-marker')
        self.adapter.clock = broken
        with self.assertRaises(BoundaryError) as caught:
            self.adapter.status()
        self.assertEqual((caught.exception.status, caught.exception.code), (503, 'clock_unavailable'))
        self.assertIsNone(caught.exception.__cause__)
        self.assertNotIn('private-status', str(caught.exception))
        self.assertEqual(len(self.calls), calls)
        self.assert_every_connection_field_revoked('not_configured')

    async def test_transport_http_os_timeout_causes_are_removed_and_state_revoked(self):
        good_transport = self.adapter.transport
        for failure in (httpx.ConnectError, OSError, TimeoutError):
            with self.subTest(failure=failure):
                self.adapter.transport = good_transport
                await self.adapter.connect()
                attempted = []
                def broken(request):
                    attempted.append((request.method, request.url.path))
                    raise failure('private-transport-marker')
                self.adapter.transport = httpx.MockTransport(broken)
                with self.assertRaises(BoundaryError) as caught:
                    await self.adapter.connect()
                self.assertEqual((caught.exception.status, caught.exception.code), (502, 'provider_upstream_failure'))
                self.assertIsNone(caught.exception.__cause__)
                self.assertNotIn('private-transport', str(caught.exception))
                self.assertEqual(attempted, [('POST', '/v1/oauth2/token')])
                self.assert_every_connection_field_revoked('error')

    async def test_parse_duplicate_nonfinite_decode_recursion_errors_are_cause_free(self):
        good_transport = self.adapter.transport
        invalid = (b'{private-json-marker', b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}',
                   b'\xff', b'{"x":' + b'[' * 33 + b'0' + b']' * 33 + b'}',
                   b'{"x":[' + b','.join([b'0'] * 4097) + b']}',
                   b'{"x":' + b'[' * 2000 + b'0' + b']' * 2000 + b'}')
        for data in invalid:
            with self.subTest(data_length=len(data)):
                self.adapter.transport = good_transport
                await self.adapter.connect()
                attempted = []
                def malformed(request):
                    attempted.append((request.method, request.url.path))
                    return httpx.Response(200, content=data)
                self.adapter.transport = httpx.MockTransport(malformed)
                with self.assertRaises(BoundaryError) as caught:
                    await self.adapter.connect()
                self.assertEqual((caught.exception.status, caught.exception.code), (502, 'provider_response_invalid'))
                self.assertIsNone(caught.exception.__cause__)
                self.assertNotIn('private-json', str(caught.exception))
                self.assertEqual(attempted, [('POST', '/v1/oauth2/token')])
                self.assert_every_connection_field_revoked('error')

    async def test_exponent_overflow_anywhere_rejects_and_revokes_reconnect(self):
        good_transport = self.adapter.transport
        invalid = (
            b'{"access_token":"synthetic-token","token_type":"Bearer","expires_in":120,"extra":1e999}',
            b'{"access_token":"synthetic-token","token_type":"Bearer","expires_in":120,"extra":+1e999}',
            b'{"access_token":"synthetic-token","token_type":"Bearer","expires_in":120,"extra":-1e999}',
            b'{"access_token":"synthetic-token","token_type":"Bearer","expires_in":120,"ignored":{"nested":[0,1e999]}}',
            b'{"access_token":"synthetic-token","token_type":"Bearer","expires_in":120,"ignored":[{"nested":-1e999}]}',
        )
        for data in invalid:
            with self.subTest(data=data):
                self.adapter.transport = good_transport
                await self.adapter.connect()
                attempted = []
                def overflow(request):
                    attempted.append((request.method, request.url.path))
                    return httpx.Response(200, content=data)
                self.adapter.transport = httpx.MockTransport(overflow)
                with self.assertRaises(BoundaryError) as caught:
                    await self.adapter.connect()
                self.assertEqual(
                    (caught.exception.status, caught.exception.code),
                    (502, 'provider_response_invalid'),
                )
                self.assertIsNone(caught.exception.__cause__)
                self.assertEqual(attempted, [('POST', '/v1/oauth2/token')])
                self.assert_every_connection_field_revoked('error')

    async def test_exponent_overflow_in_draft_ignored_field_is_rejected(self):
        await self.adapter.connect()
        calls = len(self.calls)
        def overflow(request):
            self.calls.append((request.method, request.url.path))
            return httpx.Response(
                200,
                content=b'{"id":"INV2-SYNTHETIC-0001","status":"DRAFT","ignored":{"value":1e999}}',
            )
        self.adapter.transport = httpx.MockTransport(overflow)
        with self.assertRaises(BoundaryError) as caught:
            await self.adapter.create_invoice_draft(
                {'description':'Synthetic cup','amount':'10.00','currency':'USD'},
                'synthetic-request-id',
            )
        self.assertEqual(
            (caught.exception.status, caught.exception.code),
            (502, 'provider_response_invalid'),
        )
        self.assertIsNone(caught.exception.__cause__)
        self.assertEqual(self.calls[calls:], [('POST', '/v2/invoicing/invoices')])
        self.assertEqual(self.adapter.open_clients, 0)

    async def test_draft_second_and_third_clock_failures_revoke_without_retry(self):
        payload = {'description':'Synthetic cup','amount':'10.00','currency':'USD'}
        for failure_call, expected_invoice_posts in ((2, 0), (3, 1)):
            with self.subTest(failure_call=failure_call):
                self.adapter.clock = lambda:self.now
                await self.adapter.connect()
                previous = len(self.calls)
                clock_calls = 0
                def failing_clock():
                    nonlocal clock_calls
                    clock_calls += 1
                    if clock_calls == failure_call:
                        raise RuntimeError('private-draft-clock-marker')
                    return self.now
                self.adapter.clock = failing_clock
                with self.assertRaises(BoundaryError) as caught:
                    await self.adapter.create_invoice_draft(payload, 'synthetic-request-id')
                self.assertEqual(
                    (caught.exception.status, caught.exception.code),
                    (503, 'clock_unavailable'),
                )
                self.assertIsNone(caught.exception.__cause__)
                self.assertNotIn('private-draft-clock-marker', str(caught.exception))
                self.assertEqual(clock_calls, failure_call)
                self.assertEqual(
                    self.calls[previous:],
                    [('POST', '/v2/invoicing/invoices')] * expected_invoice_posts,
                )
                self.assert_every_connection_field_revoked('not_configured')
                calls_after_failure = len(self.calls)
                with self.assertRaises(BoundaryError) as disconnected:
                    await self.adapter.create_invoice_draft(payload, 'synthetic-request-id')
                self.assertEqual(disconnected.exception.code, 'provider_disabled')
                self.assertEqual(len(self.calls), calls_after_failure)

    async def test_second_clock_failure_before_commit_revokes_every_field(self):
        await self.adapter.connect()
        calls = 0
        def second_fails():
            nonlocal calls
            calls += 1
            if calls == 2:
                raise RuntimeError('private-second-clock-marker')
            return self.now
        self.adapter.clock = second_fails
        previous = len(self.calls)
        with self.assertRaises(BoundaryError) as caught:
            await self.adapter.connect()
        self.assertEqual(caught.exception.code, 'clock_unavailable')
        self.assertIsNone(caught.exception.__cause__)
        self.assertEqual(len(self.calls) - previous, 1)
        self.assert_every_connection_field_revoked('not_configured')

    async def test_response_validation_failure_before_commit_revokes_every_field(self):
        await self.adapter.connect()
        previous = len(self.calls)
        with patch.object(PaypalStatusResponse, 'model_validate', side_effect=ValueError('private-response-marker')):
            with self.assertRaises(BoundaryError) as caught:
                await self.adapter.connect()
        self.assertEqual((caught.exception.status, caught.exception.code), (502, 'provider_upstream_failure'))
        self.assertIsNone(caught.exception.__cause__)
        self.assertNotIn('private-response', str(caught.exception))
        self.assertEqual(len(self.calls) - previous, 1)
        self.assert_every_connection_field_revoked('error')

    async def test_receipt_builder_failure_before_commit_revokes_and_removes_cause(self):
        for failure in (RuntimeError('private-receipt-marker'), BoundaryError(502, 'provider_response_invalid')):
            failure.__cause__ = ValueError('private-receipt-cause')
            await self.adapter.connect()
            previous = len(self.calls)
            with patch.object(self.adapter, '_receipt', side_effect=failure):
                with self.assertRaises(BoundaryError) as caught:
                    await self.adapter.connect()
            self.assertEqual(caught.exception.status, 502)
            self.assertIsNone(caught.exception.__cause__)
            self.assertNotIn('private-receipt', str(caught.exception))
            self.assertEqual(len(self.calls) - previous, 1)
            self.assert_every_connection_field_revoked('error')

    async def test_loader_sees_revoked_state_and_config_is_uncommitted_during_provider(self):
        await self.adapter.connect()
        attempts = []
        def loader():
            self.assert_every_connection_field_revoked('not_configured')
            return PaypalConfig(True, 'synthetic-id', 'synthetic-secret')
        def provider(request):
            self.assert_every_connection_field_revoked('not_configured', open_clients=1)
            attempts.append((request.method, request.url.path))
            return httpx.Response(200, json=self.oauth)
        self.adapter.config_loader = loader
        self.adapter.transport = httpx.MockTransport(provider)
        response = await self.adapter.connect()
        self.assertEqual(response['status'], 'connected')
        self.assertEqual(attempts, [('POST', '/v1/oauth2/token')])
        response['evidence_receipt']['status'] = 'DRAFT'
        self.assertEqual(self.adapter._connection_receipt['status'], 'CONNECTED')

    async def test_reviewed_draft_receipt_only_post_and_replay_remains_blocked(self):
        await self.adapter.connect();store=SessionStore(clock=lambda:self.now);s=store.create();session=store.sessions[s['session_id']]
        p={'description':'Synthetic cup','amount':'10.00','currency':'USD'}
        evaluation=store.review_aup(session,p['description'])
        review=store.review_invoice(session,dict(p,confirm_sandbox_draft=True,evaluation_id=evaluation['evaluation_id'],description_digest=evaluation['description_digest']))
        request=dict(p,review_token=review['review_token'],payload_digest=review['payload_digest'])
        gateway=SafePaypalToolGateway(store,self.adapter)
        response=await gateway.invoke('create_invoice',request,session=session)
        self.assert_receipt(response['evidence_receipt'],'CREATE_INVOICE_DRAFT',response['invoice_id'])
        InvoiceDraftResponse.model_validate(response)
        self.assertEqual(self.calls,[('POST','/v1/oauth2/token'),('POST','/v2/invoicing/invoices')])
        with self.assertRaises(BoundaryError):await gateway.invoke('create_invoice',request,session=session)
        self.assertEqual(len(self.calls),2)
        self.assertEqual(self.adapter.open_clients,0)

    async def test_invalid_provider_response_never_issues_draft_receipt(self):
        await self.adapter.connect();p={'description':'Synthetic cup','amount':'10.00','currency':'USD'}
        for bad in [{'id':'private@example.invalid','status':'DRAFT'},{'id':'INV2-SYNTHETIC-0001','status':'SENT'}]:
            self.invoice=bad
            with self.assertRaises(BoundaryError) as caught:await self.adapter.create_invoice_draft(p,'synthetic-request-id')
            self.assertEqual(caught.exception.code,'provider_response_invalid')
            self.assertNotIn('private@',str(caught.exception))
        self.assertEqual(self.adapter.open_clients,0)

    async def test_bad_clock_fails_before_oauth_request_or_state_commit(self):
        for bad in [None,'2026-10-06',datetime(2026,10,6)]:
            self.adapter.clock=lambda value=bad:value
            with self.assertRaises(BoundaryError) as caught:await self.adapter.connect()
            self.assertEqual(caught.exception.code,'clock_unavailable')
            self.assertIsNone(self.adapter._access_token)
            self.assertIsNone(self.adapter._connection_receipt)
        self.assertEqual(self.calls,[])

    async def test_clock_exception_and_overflow_do_not_commit_token_or_receipt(self):
        def broken():raise RuntimeError('private-clock-marker')
        self.adapter.clock=broken
        with self.assertRaises(BoundaryError) as caught:await self.adapter.connect()
        self.assertEqual(caught.exception.code,'clock_unavailable')
        self.assertIsNone(caught.exception.__cause__)
        self.assertNotIn('private-clock-marker',str(caught.exception))
        self.assertEqual(self.calls,[])
        self.adapter.clock=lambda:datetime(9999,12,31,23,59,59,tzinfo=timezone.utc)
        with self.assertRaises(BoundaryError) as caught:await self.adapter.connect()
        self.assertEqual(caught.exception.code,'clock_unavailable')
        self.assertIsNone(self.adapter._access_token)
        self.assertIsNone(self.adapter._connection_receipt)
        self.assertEqual(self.adapter.open_clients,0)

    async def test_receipt_schema_rejects_forged_raw_extra_type_time_and_action(self):
        r=(await self.adapter.connect())['evidence_receipt']
        mutations=[('secret','private-marker'),('schema_version',True),('separate_get_readback',0),
                   ('separate_get_readback',True),('proof_kind','GET_READBACK'),('environment','production'),
                   ('evidence_class','MOCK_AUTHENTIC'),('observed_at','2026-02-30T00:00:00Z'),
                   ('observed_at','2026-10-06T00:00:00+00:60'),('observed_at','2026-10-06T00:00:00'),
                   ('status','DRAFT'),('invoice_id','INV2-SYNTHETIC-0001')]
        for key,value in mutations:
            with self.subTest(key=key,value=value),self.assertRaises(ValidationError):
                SandboxEvidenceReceipt.model_validate(dict(r,**{key:value}))
        for key in r:
            candidate=deepcopy(r);candidate.pop(key)
            with self.subTest(missing=key),self.assertRaises(ValidationError):SandboxEvidenceReceipt.model_validate(candidate)

    async def test_nested_receipt_bound_to_outer_connection_and_invoice(self):
        connected=await self.adapter.connect()
        for change in [{'last_verified_at':'2026-10-06T00:00:01Z'},{'status':'disconnected'},
                       {'configured':False},{'evidence_receipt':None}]:
            with self.subTest(change=change),self.assertRaises(ValidationError):PaypalStatusResponse.model_validate(dict(connected,**change))
        p={'description':'Synthetic cup','amount':'10.00','currency':'USD'}
        draft=await self.adapter.create_invoice_draft(p,'synthetic-request-id')
        for change in [{'invoice_id':'INV2-SYNTHETIC-0002'}, {'evidence_receipt':connected['evidence_receipt']},
                       {'evidence_receipt':None}, {'raw_body':self.invoice}]:
            with self.subTest(change=list(change)),self.assertRaises(ValidationError):InvoiceDraftResponse.model_validate(dict(draft,**change))

    async def test_custom_transport_cannot_upgrade_receipt_class(self):
        await self.adapter.connect();store=SessionStore(clock=lambda:self.now);created=store.create();session=store.sessions[created['session_id']]
        payload={'description':'Synthetic cup','amount':'10.00','currency':'USD'}
        scan=store.review_aup(session,payload['description'])
        review=store.review_invoice(session,dict(payload,confirm_sandbox_draft=True,evaluation_id=scan['evaluation_id'],description_digest=scan['description_digest']))
        real=self.adapter.create_invoice_draft
        async def forged(p,r):
            value=await real(p,r);value['evidence_receipt']['evidence_class']='AUTHENTIC_SANDBOX_RESPONSE';return value
        with patch.object(self.adapter,'create_invoice_draft',forged),self.assertRaises(BoundaryError) as caught:
            await SafePaypalToolGateway(store,self.adapter).invoke('create_invoice',dict(payload,review_token=review['review_token'],payload_digest=review['payload_digest']),session=session)
        self.assertEqual(caught.exception.code,'provider_response_invalid')

    async def test_authentic_class_is_native_operator_only_without_executing_it(self):
        native=PaypalAdapter()
        self.assertEqual(native._evidence_class,'AUTHENTIC_SANDBOX_RESPONSE')
        self.assertIsNone(native.status()['evidence_receipt'])
        native.config_loader=lambda:PaypalConfig()
        self.assertEqual(native._evidence_class,'SYNTHETIC_TEST_RESPONSE')
        for adapter in [PaypalAdapter(config_loader=lambda:PaypalConfig()),PaypalAdapter(transport=self.adapter.transport),
                        PaypalAdapter(clock=lambda:self.now)]:
            self.assertEqual(adapter._evidence_class,'SYNTHETIC_TEST_RESPONSE')
        self.assertEqual(self.calls,[])

    async def test_each_constructor_injection_is_permanently_synthetic_after_public_restore(self):
        for adapter in [PaypalAdapter(config_loader=lambda:PaypalConfig()),
                        PaypalAdapter(transport=self.adapter.transport),
                        PaypalAdapter(clock=lambda:self.now)]:
            with self.subTest(adapter=adapter):
                adapter.config_loader=operator_config
                adapter.transport=None
                adapter.clock=utc_now
                self.assertEqual(adapter._evidence_class,'SYNTHETIC_TEST_RESPONSE')
                self.assertIsNone(adapter.status()['evidence_receipt'])
        self.assertEqual(self.calls,[])

    async def test_injected_callbacks_restoring_native_fields_cannot_upgrade_connect_or_gateway_draft(self):
        for constructor_seam in ('loader','transport','clock'):
            with self.subTest(constructor_seam=constructor_seam):
                await self._assert_callback_restore_stays_synthetic(native_constructor=False,constructor_seam=constructor_seam)

    async def test_native_constructor_runtime_mock_captured_before_callback_restore(self):
        await self._assert_callback_restore_stays_synthetic(native_constructor=True)

    async def _assert_callback_restore_stays_synthetic(self, *, native_constructor, constructor_seam=None):
        calls=[]
        injected={
            'loader':{'config_loader':lambda:PaypalConfig(True,'synthetic-id','synthetic-secret')},
            'transport':{'transport':self.adapter.transport},
            'clock':{'clock':lambda:self.now},
        }
        adapter=PaypalAdapter() if native_constructor else PaypalAdapter(**injected[constructor_seam])
        def handler(request):
            calls.append((request.method,request.url.path))
            # The active HTTP client retains MockTransport after these public mutations.
            adapter.transport=None
            adapter.config_loader=operator_config
            adapter.clock=utc_now
            return httpx.Response(200,json=self.oauth if request.url.path=='/v1/oauth2/token' else self.invoice)
        transport=httpx.MockTransport(handler)
        adapter.config_loader=lambda:PaypalConfig(True,'synthetic-id','synthetic-secret')
        adapter.transport=transport
        adapter.clock=lambda:self.now
        connected=await adapter.connect()
        self.assert_receipt(connected['evidence_receipt'],'OAUTH_CONNECT')
        self.assertEqual(adapter.open_clients,0)
        # Reinsert only the trusted test transport; no credential accessor is executed.
        adapter.transport=transport
        store=SessionStore(clock=lambda:self.now)
        created=store.create()
        session=store.sessions[created['session_id']]
        payload={'description':'Synthetic cup','amount':'10.00','currency':'USD'}
        scan=store.review_aup(session,payload['description'])
        review=store.review_invoice(session,dict(payload,confirm_sandbox_draft=True,
            evaluation_id=scan['evaluation_id'],description_digest=scan['description_digest']))
        response=await SafePaypalToolGateway(store,adapter).invoke('create_invoice',dict(payload,
            review_token=review['review_token'],payload_digest=review['payload_digest']),session=session)
        self.assert_receipt(response['evidence_receipt'],'CREATE_INVOICE_DRAFT',response['invoice_id'])
        self.assertEqual(calls,[('POST','/v1/oauth2/token'),('POST','/v2/invoicing/invoices')])
        self.assertEqual(adapter.status()['evidence_receipt']['evidence_class'],'SYNTHETIC_TEST_RESPONSE')
        self.assertEqual(adapter.open_clients,0)
        if not native_constructor:
            self.assertEqual(adapter._evidence_class,'SYNTHETIC_TEST_RESPONSE')

if __name__=='__main__':unittest.main()
