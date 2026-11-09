# Inject Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkluamVjdFJlcXVlc3Q

InjectRequest.


# Class Name

`InjectRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `scenario` | [`Scenario5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/scenario-5.md) | Required | Scenario. |


# Example

```ruby
inject_request = InjectRequest.new(
  Scenario5Enum::BURST
)
```



