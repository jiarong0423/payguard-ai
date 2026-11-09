# Post Paypal Invoices Review

Source: http://localhost:3000/#/php/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2ludm9pY2VzX3Jldmlldw

Invoice Review. Local console route POST /api/v1/paypal/invoices/review on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postPaypalInvoicesReview(InvoiceReviewRequest $body): InvoiceReviewResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`InvoiceReviewRequest`](http://localhost:3000/llms-pages/php/models/structures/invoice-review-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`InvoiceReviewResponse`](http://localhost:3000/llms-pages/php/models/structures/invoice-review-response.md)


# Example Usage

```php
$body = InvoiceReviewRequestBuilder::init(
    'amount8',
    false,
    CurrencyEnum::USD,
    'description4'
)->build();

$paypalController = $client->getPaypalController();

try {
    $result = $paypalController->postPaypalInvoicesReview($body);
    echo 'InvoiceReviewResponse:';
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



