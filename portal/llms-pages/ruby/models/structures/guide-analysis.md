# Guide Analysis

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkd1aWRlQW5hbHlzaXM

GuideAnalysis.


# Class Name

`GuideAnalysis`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `reason` | [Reason5](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/reason-5.md) | Required | This is a container for any-of cases. |
| `status` | [`Status8Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/status-8.md) | Required | Status. |
| `turn` | `Integer` | Required | Turn. |


# Example

```ruby
guide_analysis = GuideAnalysis.new(
  Reason5Enum::BUDGET,
  Status8Enum::REPLACED,
  142
)
```



