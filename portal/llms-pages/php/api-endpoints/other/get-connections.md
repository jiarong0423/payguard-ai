# Get Connections

Source: http://localhost:3000/#/php/x-redirect/JTI0ZSUyRm90aGVyJTJGZ2V0X2Nvbm5lY3Rpb25z

Connections. Local console route GET /api/v1/connections on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function getConnections(): ConnectionsResponse
```


# Response Type

**200**: Successful Response

[`ConnectionsResponse`](http://localhost:3000/llms-pages/php/models/structures/connections-response.md)


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


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/php/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/php/models/exceptions/error-body.md) |



