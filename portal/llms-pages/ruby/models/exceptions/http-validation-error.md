# HTTP Validation Error

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationErrorException`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `detail` | [`Array[ValidationError]`](http://localhost:3000/llms-pages/ruby/models/structures/validation-error.md) | Optional | Detail. |


# Example

```ruby
begin
  # make the API call
rescue HTTPValidationErrorException => e
  puts "Caught HTTPValidationErrorException: #{e.message}"
end
```



