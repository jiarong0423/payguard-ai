# Get Ai Usage

Source: http://localhost:3000/#/php/x-redirect/JTI0ZSUyRmFpJTJGZ2V0X2FpX3VzYWdl

(optimise r24) This session's AI calls: stage, model, tokens, latency, estimated cost. No prompt or reply
text is ever stored; the hosted demo makes no model call and answers an empty list.

:information_source: **Note** This endpoint does not require authentication.

```php
function getAiUsage(): AiUsageResponse
```


# Response Type

**200**: Successful Response

[`AiUsageResponse`](http://localhost:3000/llms-pages/php/models/structures/ai-usage-response.md)


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


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/php/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/php/models/exceptions/error-body.md) |



