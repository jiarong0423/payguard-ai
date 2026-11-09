# Post Country Rules Check

Source: http://localhost:3000/#/python/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jb3VudHJ5X3J1bGVzX2NoZWNr

Country Rules Check. Local console route POST /api/v1/country-rules/check on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_country_rules_check(self,
                            body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CountryRulesCheckRequest`](http://localhost:3000/llms-pages/python/models/structures/country-rules-check-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

`Any`


# Example Usage

```python
body = CountryRulesCheckRequest(
    buyer_country=BuyerCountryEnum.AU,
    seller_country=SellerCountryEnum.AU,
    account_opened=AccountOpenedEnum.UNKNOWN,
    account_type=AccountTypeEnum.BUSINESS,
    checkout=CheckoutEnum.PAYPAL_ACCOUNT
)

result = other_controller.post_country_rules_check(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |



