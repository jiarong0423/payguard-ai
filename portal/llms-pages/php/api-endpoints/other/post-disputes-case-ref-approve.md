# Post Disputes Case Ref Approve

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9kaXNwdXRlc19jYXNlX3JlZl9hcHByb3Zl

Approve. Local console route POST /api/v1/disputes/{case_ref}/approve on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postDisputesCaseRefApprove(string $caseRef, ApproveRequest $body): DisputeApprovalResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseRef` | `string` | Template, Required | Case ref. |
| `body` | [`ApproveRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/approve-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`DisputeApprovalResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/dispute-approval-response.md)


# Example Usage

```php
$caseRef = 'case_ref4';

$body = ApproveRequestBuilder::init(
    'draft_digest6'
)->build();

$otherController = $client->getOtherController();

try {
    $result = $otherController->postDisputesCaseRefApprove(
        $caseRef,
        $body
    );
    echo 'DisputeApprovalResponse:';
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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |



