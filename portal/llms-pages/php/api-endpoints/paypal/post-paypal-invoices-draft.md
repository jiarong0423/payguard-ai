# Post Paypal Invoices Draft

Source: http://localhost:3000/#/php/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2ludm9pY2VzX2RyYWZ0

Invoice Draft. Local console route POST /api/v1/paypal/invoices/draft on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```php
function postPaypalInvoicesDraft(InvoiceDraftRequest $body): InvoiceDraftResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`InvoiceDraftRequest`](http://localhost:3000/llms-pages/php/models/structures/invoice-draft-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`InvoiceDraftResponse`](http://localhost:3000/llms-pages/php/models/structures/invoice-draft-response.md)


# Example Usage

```php
$body = InvoiceDraftRequestBuilder::init(
    'amount8',
    CurrencyEnum::USD,
    'description4',
    'payload_digest4',
    'review_token4'
)->build();

$paypalController = $client->getPaypalController();

try {
    $result = $paypalController->postPaypalInvoicesDraft($body);
    echo 'InvoiceDraftResponse:';
    var_dump($result);
} catch (ErrorBodyException $exp) {
    echo 'Caught ErrorBodyException:', $exp;
} catch (HTTPValidationErrorException $exp) {
    echo 'Caught HTTPValidationErrorException:', $exp;
} catch (ApiException $exp) {
    echo 'Caught:', $exp;
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/php/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/php/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/php/models/exceptions/error-body.md) |



