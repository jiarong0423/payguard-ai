# Post Country Rules Check

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jb3VudHJ5X3J1bGVzX2NoZWNr

Country Rules Check. Local console route POST /api/v1/country-rules/check on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def post_country_rules_check(body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CountryRulesCheckRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/country-rules-check-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

`Object`


# Example Usage

```ruby
body = CountryRulesCheckRequest.new(
  BuyerCountryEnum::AU,
  SellerCountryEnum::AU,
  AccountOpenedEnum::UNKNOWN,
  AccountTypeEnum::BUSINESS,
  nil,
  CheckoutEnum::PAYPAL_ACCOUNT,
  nil,
  []
)

result = other_controller.post_country_rules_check(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |



