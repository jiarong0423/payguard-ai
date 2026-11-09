# Post Demo Inject

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRmRlbW8lMkZwb3N0X2RlbW9faW5qZWN0

Inject. Local console route POST /api/v1/demo/inject on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_demo_inject(self,
                    body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`InjectRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/inject-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`StateResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/state-response.md)


# Example Usage

```python
body = InjectRequest(
    scenario=Scenario5Enum.DISPUTE
)

result = demo_controller.post_demo_inject(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



