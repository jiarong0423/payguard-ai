# Get Studio Agent Status

Source: http://localhost:3000/#/ruby/x-redirect/JTI0ZSUyRnN0dWRpbyUyRmdldF9zdHVkaW9fYWdlbnRfc3RhdHVz

Studio Agent Status. Local console route GET /api/v1/studio/agent-status on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def get_studio_agent_status
```


# Response Type

**200**: Successful Response

`Object`


# Example Usage

```ruby
result = studio_controller.get_studio_agent_status
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |



