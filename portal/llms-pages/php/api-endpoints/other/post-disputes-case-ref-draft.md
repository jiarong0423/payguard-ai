# Post Disputes Case Ref Draft

Source: http://localhost:3000/#/php/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9kaXNwdXRlc19jYXNlX3JlZl9kcmFmdA

Draft. Local console route POST /api/v1/disputes/{case_ref}/draft on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postDisputesCaseRefDraft(string $caseRef, array $body): DisputeDraftResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseRef` | `string` | Template, Required | Case ref. |
| `body` | `array` | Body, Required | - |


# Response Type

**200**: Successful Response

[`DisputeDraftResponse`](http://localhost:3000/llms-pages/php/models/structures/dispute-draft-response.md)


# Example Usage

```php
$caseRef = 'case_ref4';

$body = ApiHelper::deserialize('{"key1":"val1","key2":"val2"}');

$otherController = $client->getOtherController();

try {
    $result = $otherController->postDisputesCaseRefDraft(
        $caseRef,
        $body
    );
    echo 'DisputeDraftResponse:';
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



