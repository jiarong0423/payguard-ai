# Get Connections

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRm90aGVyJTJGZ2V0X2Nvbm5lY3Rpb25z

Connections. Local console route GET /api/v1/connections on synthetic data; advisory only.

```php
function getConnections(): ConnectionsResponse
```


# Authentication

This endpoint requires [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/getting-started/how-to-get-started/authorization.md)


# Response Type

**200**: Successful Response

[`ConnectionsResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/connections-response.md)


# Example Usage

```php
$otherController = $client->getOtherController();

try {
    $result = $otherController->getConnections();
    echo 'ConnectionsResponse:';
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
  "mode": "hosted_demo",
  "sandbox_reads": true
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |



