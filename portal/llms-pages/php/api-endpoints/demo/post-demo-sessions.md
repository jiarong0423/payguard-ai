# Post Demo Sessions

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRmRlbW8lMkZwb3N0X2RlbW9fc2Vzc2lvbnM

New Session. Local console route POST /api/v1/demo/sessions on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postDemoSessions(array $body): SessionResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | `array` | Body, Required | JSON body for: New Session. |


# Response Type

**201**: Successful Response

[`SessionResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/session-response.md)


# Example Usage

```php
$body = ApiHelper::deserialize('{}');

$demoController = $client->getDemoController();

try {
    $result = $demoController->postDemoSessions($body);
    echo 'SessionResponse:';
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
  "csrf_token": "csrf-example-0001",
  "expires_at": "2026-10-07T10:30:00Z",
  "session_id": "sess-example-0001",
  "source": "synthetic"
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |



