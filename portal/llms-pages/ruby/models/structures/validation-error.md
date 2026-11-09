# Validation Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlZhbGlkYXRpb25FcnJvcg

ValidationError.


# Class Name

`ValidationError`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ctx` | `Object` | Optional | Ctx. |
| `input` | `Object` | Optional | Input. |
| `loc` | Array[String \| Integer] | Required | This is Array of a container for any-of cases. |
| `msg` | `String` | Required | Msg. |
| `type` | `String` | Required | Type. |


# Example

```ruby
validation_error = ValidationError.new(
  [
    'String9',
    'String0',
    'String1'
  ],
  'msg4',
  'type2',
  { 'key1' => 'val1', 'key2' => 'val2' },
  JSON.parse('{"key1":"val1","key2":"val2"}')
)
```



