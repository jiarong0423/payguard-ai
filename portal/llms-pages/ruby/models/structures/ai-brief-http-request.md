# Ai Brief Http Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkFpQnJpZWZIdHRwUmVxdWVzdA

What the console may send: the stage and, for disputes, which case. Session facts are never caller input.


# Class Name

`AiBriefHttpRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_ref` | String \| nil | Optional | This is a container for any-of cases. |
| `stage` | [`StageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/stage.md) | Required | Stage. |


# Example

```ruby
ai_brief_http_request = AiBriefHttpRequest.new(
  StageEnum::DISPUTE_MEDIATION,
  'String7'
)
```



