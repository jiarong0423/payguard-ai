# Get Paypal Disputes

Source: http://localhost:3000/#/ruby/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfZGlzcHV0ZXM

List Disputes. Local console route GET /api/v1/paypal/disputes on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def get_paypal_disputes
```


# Response Type

**200**: Successful Response

[`DisputeListResponse`](http://localhost:3000/llms-pages/ruby/models/structures/dispute-list-response.md)


# Example Usage

```ruby
result = paypal_controller.get_paypal_disputes
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |



