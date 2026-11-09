# Post Country Rules Check

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jb3VudHJ5X3J1bGVzX2NoZWNr

Country Rules Check. Local console route POST /api/v1/country-rules/check on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostCountryRulesCheckAsync(
    Models.CountryRulesCheckRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CountryRulesCheckRequest`](http://localhost:3000/llms-pages/net-standard-library/models/structures/country-rules-check-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

`Task<object>`


# Example Usage

```csharp
CountryRulesCheckRequest body = new CountryRulesCheckRequest
{
    BuyerCountry = BuyerCountryEnum.AU,
    SellerCountry = SellerCountryEnum.AU,
    AccountOpened = AccountOpenedEnum.Unknown,
    AccountType = AccountTypeEnum.Business,
    Checkout = CheckoutEnum.PaypalAccount,
};

try
{
    object result = await otherController.PostCountryRulesCheckAsync(body);
}
catch (ApiException e)
{
    Console.WriteLine(e.Message);
    if (e is ErrorBodyException)
    {
       // TODO: Handle ErrorBodyException exception here
    }
    if (e is HTTPValidationErrorException)
    {
       // TODO: Handle HTTPValidationErrorException exception here
    }
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/net-standard-library/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/net-standard-library/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/net-standard-library/models/exceptions/error-body.md) |



