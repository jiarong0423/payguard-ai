# Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlNpZ25hbA

Signal.


# Class Name

`Signal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | String \| nil | Optional | This is a container for any-of cases. |
| `confidence` | [Confidence](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/confidence.md) \| nil | Optional | This is a container for any-of cases. |
| `source` | [`Source2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/source-2.md) | Optional | Source. |


# Example

```ruby
signal = Signal.new(
  'String1',
  ConfidenceEnum::HIGH,
  Source2Enum::CHANNEL3
)
```



