# Guide Analysis

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkd1aWRlQW5hbHlzaXM

GuideAnalysis.


# Class Name

`GuideAnalysis`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `reason` | [Reason5](http://localhost:3000/llms-pages/ruby/models/enumerations/reason-5.md) | Required | This is a container for any-of cases. |
| `status` | [`Status8Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/status-8.md) | Required | Status. |
| `turn` | `Integer` | Required | Turn. |


# Example

```ruby
guide_analysis = GuideAnalysis.new(
  Reason5Enum::BUDGET,
  Status8Enum::REPLACED,
  142
)
```



