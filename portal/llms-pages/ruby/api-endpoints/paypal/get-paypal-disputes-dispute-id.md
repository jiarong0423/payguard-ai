# Get Paypal Disputes Dispute Id

Source: http://localhost:3000/#/ruby/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfZGlzcHV0ZXNfZGlzcHV0ZV9pZA

Get Dispute. Local console route GET /api/v1/paypal/disputes/{dispute_id} on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def get_paypal_disputes_dispute_id(dispute_id)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `dispute_id` | `String` | Template, Required | Dispute id. |


# Response Type

**200**: Successful Response

[`DisputeDetailResponse`](http://localhost:3000/llms-pages/ruby/models/structures/dispute-detail-response.md)


# Example Usage

```ruby
dispute_id = 'dispute_id2'

result = paypal_controller.get_paypal_disputes_dispute_id(dispute_id)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/ruby/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |



