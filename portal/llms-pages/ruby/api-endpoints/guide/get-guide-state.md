# Get Guide State

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0ZSUyRmd1aWRlJTJGZ2V0X2d1aWRlX3N0YXRl

Guide State. Local console route GET /api/v1/guide/state on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def get_guide_state(scenario: nil)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `scenario` | [Scenario1](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/scenario-1.md) \| nil | Query, Optional | This is a container for any-of cases. |


# Response Type

**200**: Successful Response

[`GuideStateResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-state-response.md)


# Example Usage

```ruby
result = guide_controller.get_guide_state
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |



