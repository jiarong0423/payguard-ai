# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationErrorException`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `detail` | [`Array[ValidationError]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/validation-error.md) | Optional | Detail. |


# Example

```ruby
begin
  # make the API call
rescue HTTPValidationErrorException => e
  puts "Caught HTTPValidationErrorException: #{e.message}"
end
```



