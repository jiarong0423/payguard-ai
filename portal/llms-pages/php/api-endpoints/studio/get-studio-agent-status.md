# Get Studio Agent Status

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRnN0dWRpbyUyRmdldF9zdHVkaW9fYWdlbnRfc3RhdHVz

Studio Agent Status. Local console route GET /api/v1/studio/agent-status on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function getStudioAgentStatus(): array
```


# Response Type

**200**: Successful Response

`array`


# Example Usage

```php
$studioController = $client->getStudioController();

try {
    $result = $studioController->getStudioAgentStatus();
    echo 'array:';
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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |



