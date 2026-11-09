# Get Ai Usage

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRmFpJTJGZ2V0X2FpX3VzYWdl

(optimise r24) This session's AI calls: stage, model, tokens, latency, estimated cost. No prompt or reply
text is ever stored; the hosted demo makes no model call and answers an empty list.

```php
function getAiUsage(): AiUsageResponse
```


# Authentication

This endpoint requires [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/getting-started/how-to-get-started/authorization.md)


# Response Type

**200**: Successful Response

[`AiUsageResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/ai-usage-response.md)


# Example Usage

```php
$aiController = $client->getAiController();

try {
    $result = $aiController->getAiUsage();
    echo 'AiUsageResponse:';
    var_dump($result);
} catch (ErrorBodyException $exp) {
    echo 'Caught ErrorBodyException:', $exp;
} catch (ApiException $exp) {
    echo 'Caught:', $exp;
}
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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |



