# Post Country Rules Check

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jb3VudHJ5X3J1bGVzX2NoZWNr

Country Rules Check. Local console route POST /api/v1/country-rules/check on synthetic data; advisory only.

```ruby
def post_country_rules_check(body)
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CountryRulesCheckRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/country-rules-check-request.md) | Body, Required | JSON body for: Country Rules Check. |


# Response Type

**200**: Successful Response

`Object`


# Example Usage

```ruby
body = CountryRulesCheckRequest.new(
  BuyerCountryEnum::US,
  SellerCountryEnum::TW,
  envrr,
  AccountTypeEnum::BUSINESS,
  '120.00',
  CheckoutEnum::PAYPAL_ACCOUNT,
  'USD',
  []
)

result = other_controller.post_country_rules_check(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 403 | Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |



