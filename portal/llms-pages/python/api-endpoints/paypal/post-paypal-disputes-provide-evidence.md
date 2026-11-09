# Post Paypal Disputes Provide Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2Rpc3B1dGVzX3Byb3ZpZGVfZXZpZGVuY2U

Provide Evidence. Local console route POST /api/v1/paypal/disputes/provide-evidence on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_paypal_disputes_provide_evidence(self,
                                         body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ProvideEvidenceRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/provide-evidence-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`ProvideEvidenceResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/provide-evidence-response.md)


# Example Usage

```python
body = ProvideEvidenceRequest(
    case_ref='case_ref0',
    dispute_id='dispute_id8',
    submit=False
)

result = paypal_controller.post_paypal_disputes_provide_evidence(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



