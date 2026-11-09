# HTTP Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkhUVFBWYWxpZGF0aW9uRXJyb3I

HTTPValidationError.


# Class Name

`HTTPValidationError`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `detail` | [`Array[ValidationError]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/validation-error.md) | Optional | Detail. |


# Example

```ruby
http_validation_error = HTTPValidationError.new(
  [
    ValidationError.new(
      [
        'String7',
        'String8',
        'String9'
      ],
      'msg2',
      'type4',
      { 'key1' => 'val1', 'key2' => 'val2' },
      JSON.parse('{"key1":"val1","key2":"val2"}')
    ),
    ValidationError.new(
      [
        'String7',
        'String8',
        'String9'
      ],
      'msg2',
      'type4',
      { 'key1' => 'val1', 'key2' => 'val2' },
      JSON.parse('{"key1":"val1","key2":"val2"}')
    )
  ]
)
```



