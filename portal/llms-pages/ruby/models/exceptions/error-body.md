# Error Body

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkVycm9yQm9keQ

The error body every refusal uses.


# Class Name

`ErrorBodyException`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `error` | [`Error`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/error.md) | Required | What was refused and why. |


# Example

```ruby
begin
  # make the API call
rescue ErrorBodyException => e
  puts "Caught ErrorBodyException: #{e.message}"
end
```



