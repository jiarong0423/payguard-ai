"""Offline HTTP coexistence of public-reference routes and reviewed gateway."""
from copy import deepcopy
from datetime import datetime, timezone
import json
import socket
import unittest
from unittest.mock import AsyncMock, patch

import httpx
from fastapi.testclient import TestClient
from app.main import create_app
from app.paypal import PaypalAdapter, PaypalConfig
from app.paypal_tools import SafePaypalToolGateway
from app.store import SessionStore
from payguard.applicability import ApplicabilityError

ROOT = '/api/v1'
CONTEXT = {'jurisdiction': 'US', 'theme': 'source_compliance', 'as_of': '2026-10-07T00:00:00Z', 'observation_max_age_days': 30}
PAYLOAD = {'description': 'Synthetic ceramic cup', 'amount': '10.00', 'currency': 'USD'}

class PolicyGatewayIntegrationTests(unittest.TestCase):
    def setUp(self):
        for target in ((socket.socket, 'connect'), (socket, 'create_connection')):
            guard = patch.object(*target, side_effect=AssertionError('network forbidden'))
            guard.start(); self.addCleanup(guard.stop)
        self.clock = lambda: datetime(2026, 10, 7, tzinfo=timezone.utc)
        self.store = SessionStore(clock=self.clock, rate_limit=300)
        self.calls = []
        self.failure = False
        def handler(request):
            self.calls.append(request.url.path)
            if request.url.path == '/v1/oauth2/token':
                return httpx.Response(200, json={'access_token': 'synthetic-token', 'token_type': 'Bearer', 'expires_in': 3600})
            self.assertEqual(request.url.path, '/v2/invoicing/invoices')
            if self.failure:
                return httpx.Response(500, json={'private': 'synthetic-provider-residue'})
            return httpx.Response(201, json={'id': 'INV2-SYNTHETIC-0001', 'status': 'DRAFT'})
        self.provider = PaypalAdapter(config_loader=lambda: PaypalConfig(True, 'synthetic-id', 'synthetic-secret'), transport=httpx.MockTransport(handler), clock=self.clock)
        self.app = create_app(store=self.store, paypal=self.provider)
        self.client = TestClient(self.app, base_url='http://127.0.0.1:8000', client=('127.0.0.1', 55331), raise_server_exceptions=False)
        self.client.__enter__()
        self.session = self.new_session()
        self.live = self.store.sessions[self.session['session_id']]

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.assertEqual(self.provider.open_clients, 0)

    def new_session(self):
        return self.client.post(ROOT+'/demo/sessions', json={}, headers={'Origin':'http://localhost:5173'}).json()

    def post(self, route, body=None, session=None):
        s = session or self.session
        return self.client.post(ROOT+route, json={} if body is None else body, headers={'Origin':'http://localhost:5173','X-Demo-Session':s['session_id'],'X-CSRF-Token':s['csrf_token']})

    def review(self):
        evaluation = self.post('/aup/review', {'description': PAYLOAD['description']}).json()
        response = self.post('/paypal/invoices/review', dict(PAYLOAD, confirm_sandbox_draft=True,
                             evaluation_id=evaluation['evaluation_id'], description_digest=evaluation['description_digest']))
        self.assertEqual(response.status_code,200,response.text)
        receipt = response.json()
        return dict(PAYLOAD,review_token=receipt['review_token'],payload_digest=receipt['payload_digest'])

    def policy_pair(self):
        response = self.post('/policy/assess',CONTEXT)
        self.assertEqual(response.status_code,200,response.text)
        result = response.json()
        chunk = next(row['chunk_id'] for row in result['chunks'] if row['chunk_id'] == 'PP-US-AUP-POLICY')
        candidate = dict(schema_version=1,jurisdiction='US',theme='source_compliance',as_of=CONTEXT['as_of'],status='manual_review',advisory_only=True,operational_authority='REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',claims=[dict(claim_id='SYNTHETIC',claim_type='policy_reference',text='Synthetic statement requiring human review.',citation_chunk_ids=[chunk])])
        response = self.post('/advisory/evaluate',dict(CONTEXT,candidate_json=json.dumps(candidate)))
        self.assertEqual(response.status_code,200,response.text)
        self.assertEqual(response.json()['semantic_entailment'],'NOT_EVALUATED')

    def test_reference_routes_preserve_review_and_actual_gateway_path(self):
        self.assertIsInstance(self.app.state.paypal_tools,SafePaypalToolGateway)
        self.assertEqual(self.post('/paypal/connect').status_code,200)
        request = self.review()
        reviews = deepcopy(self.live.invoice_reviews)
        with patch.object(self.app.state.paypal_tools,'invoke',new=AsyncMock(wraps=self.app.state.paypal_tools.invoke)) as gateway:
            self.policy_pair()
            self.assertEqual(gateway.await_count,0)
            self.assertEqual(self.live.invoice_reviews,reviews)
            self.assertEqual(self.live.invoice_attempts,0)
            response = self.post('/paypal/invoices/draft',request)
            self.assertEqual(response.status_code,200,response.text)
            self.assertEqual(gateway.await_count,1)
            args,kw = gateway.await_args
            self.assertEqual(args,('create_invoice',request))
            self.assertIs(kw['session'],self.live)
            self.assertEqual(response.json()['external_send'],'FROZEN')
        self.assertEqual(self.post('/paypal/invoices/draft',request).status_code,422)
        self.assertEqual(self.calls.count('/v2/invoicing/invoices'),1)

    def test_policy_failure_cross_session_and_changed_payload_do_not_consume_review(self):
        self.assertEqual(self.post('/paypal/connect').status_code,200)
        request = self.review(); reviews = deepcopy(self.live.invoice_reviews)
        with patch('app.main.assess_applicability',side_effect=ApplicabilityError('applicability_corpus_unavailable')):
            response = self.post('/policy/assess',CONTEXT)
            self.assertEqual(response.status_code,503)
            self.assertEqual(response.json()['error']['code'],'reference_unavailable')
        self.assertEqual(self.post('/advisory/evaluate',dict(CONTEXT,candidate_json='{"invalid":true}')).status_code,422)
        self.assertEqual(self.post('/paypal/invoices/draft',request,self.new_session()).status_code,422)
        self.assertEqual(self.post('/paypal/invoices/draft',dict(request,amount='11.00')).status_code,422)
        self.assertEqual(self.live.invoice_reviews,reviews)
        self.assertEqual(self.live.invoice_attempts,0)
        self.assertNotIn('/v2/invoicing/invoices',self.calls)
        self.policy_pair()
        self.assertEqual(self.post('/paypal/invoices/draft',request).status_code,200)

    def test_unconnected_failure_retains_review_and_upstream_failure_is_bound_once(self):
        request = self.review(); other = self.review()
        reviews = deepcopy(self.live.invoice_reviews)
        self.policy_pair()
        self.assertEqual(self.post('/paypal/invoices/draft',request).status_code,503)
        self.assertEqual(self.live.invoice_reviews,reviews)
        self.assertEqual(self.live.invoice_attempts,0)
        self.assertEqual(self.calls,[])
        self.assertEqual(self.post('/paypal/connect').status_code,200)
        self.failure = True
        response = self.post('/paypal/invoices/draft',request)
        self.assertEqual(response.status_code,502,response.text)
        self.assertNotIn('synthetic-provider-residue',response.text)
        self.assertNotIn(request['review_token'],self.live.invoice_reviews)
        self.assertIn(other['review_token'],self.live.invoice_reviews)
        self.assertEqual(self.live.invoice_attempts,1)
        self.assertEqual(self.post('/paypal/invoices/draft',request).status_code,422)
        self.assertEqual(self.calls.count('/v2/invoicing/invoices'),1)
