# Post Country Rules Check

Source: http://localhost:3000/#/php/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jb3VudHJ5X3J1bGVzX2NoZWNr

Country Rules Check. Local console route POST /api/v1/country-rules/check on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postCountryRulesCheck(CountryRulesCheckRequest $body): array
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CountryRulesCheckRequest`](http://localhost:3000/llms-pages/php/models/structures/country-rules-check-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

`array`


# Example Usage

```php
$body = CountryRulesCheckRequestBuilder::init(
    BuyerCountryEnum::AU,
    SellerCountryEnum::AU
)
    ->accountOpened(AccountOpenedEnum::UNKNOWN)
    ->accountType(AccountTypeEnum::BUSINESS)
    ->checkout(CheckoutEnum::PAYPAL_ACCOUNT)
    ->build();

$otherController = $client->getOtherController();

try {
    $result = $otherController->postCountryRulesCheck($body);
    echo 'array:';
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



