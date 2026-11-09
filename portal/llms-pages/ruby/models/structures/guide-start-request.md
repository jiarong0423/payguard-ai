# Guide Start Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkd1aWRlU3RhcnRSZXF1ZXN0

GuideStartRequest.


# Class Name

`GuideStartRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `goods_type` | [GoodsType](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/goods-type.md) \| nil | Optional | This is a container for any-of cases. |
| `scenario` | [`Scenario2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/scenario-2.md) | Required | Scenario. |


# Example

```ruby
guide_start_request = GuideStartRequest.new(
  Scenario2Enum::DISPUTE,
  GoodsTypeEnum::PHYSICAL
)
```



