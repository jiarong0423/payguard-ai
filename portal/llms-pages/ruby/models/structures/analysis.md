# Analysis

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkFuYWx5c2lz

Analysis.


# Class Name

`Analysis`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `reason` | [Reason5](http://localhost:3000/llms-pages/ruby/models/enumerations/reason-5.md) \| nil | Optional | This is a container for any-of cases. |
| `status` | [`Status8Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/status-8.md) | Optional | Status. |
| `turn` | `Integer` | Optional | Turn. |


# Example

```ruby
analysis = Analysis.new(
  Reason5Enum::INVALID_REPLY,
  Status8Enum::REPLACED,
  198
)
```



