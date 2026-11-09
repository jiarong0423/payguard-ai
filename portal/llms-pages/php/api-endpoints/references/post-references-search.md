# Post References Search

Source: http://localhost:3000/#/php/x-redirect/JTI0ZSUyRnJlZmVyZW5jZXMlMkZwb3N0X3JlZmVyZW5jZXNfc2VhcmNo

References. Local console route POST /api/v1/references/search on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postReferencesSearch(ReferenceRequest $body): ReferenceResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ReferenceRequest`](http://localhost:3000/llms-pages/php/models/structures/reference-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`ReferenceResponse`](http://localhost:3000/llms-pages/php/models/structures/reference-response.md)


# Example Usage

```php
$body = ReferenceRequestBuilder::init(
    'query6',
    ThemeEnum::DISPUTE_MEDIATION
)
    ->caseStage(CaseStage2Enum::ANY)
    ->limit(3)
    ->requireKnownSourceDate(false)
    ->build();

$referencesController = $client->getReferencesController();

try {
    $result = $referencesController->postReferencesSearch($body);
    echo 'ReferenceResponse:';
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



