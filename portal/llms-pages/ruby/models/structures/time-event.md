# Time Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlRpbWVFdmVudA

TimeEvent.


# Class Name

`TimeEvent`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `String` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `kind` | [`KindEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/kind.md) | Required | Kind. |
| `source` | [`Source5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/source-5.md) | Required | Source. |


# Example

```ruby
time_event = TimeEvent.new(
  'at2',
  KindEnum::PAYMENT,
  Source5Enum::PROVIDER
)
```



