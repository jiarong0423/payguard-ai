# Get Ai Usage

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRmFpJTJGZ2V0X2FpX3VzYWdl

(optimise r24) This session's AI calls: stage, model, tokens, latency, estimated cost. No prompt or reply
text is ever stored; the hosted demo makes no model call and answers an empty list.

```python
def get_ai_usage(self)
```


# Authentication

This endpoint requires [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/getting-started/how-to-get-started/authorization.md)


# Response Type

**200**: Successful Response

[`AiUsageResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/ai-usage-response.md)


# Example Usage

```python
result = ai_controller.get_ai_usage()
print(result)
```


# Example Response *(as JSON)*

```json
{
  "cost_note": "example",
  "entries": [
    {
      "at": "example",
      "latency_ms": 0,
      "outcome": "ok",
      "stage": "source_compliance"
    }
  ],
  "price_table_source": "example",
  "source": "session_memory"
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



