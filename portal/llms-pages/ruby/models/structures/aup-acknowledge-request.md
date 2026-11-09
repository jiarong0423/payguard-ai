# Aup Acknowledge Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVxdWVzdA

AupAcknowledgeRequest.


# Class Name

`AupAcknowledgeRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `choice` | [`ChoiceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/choice.md) | Required | Choice. |
| `description_digest` | `String` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `evaluation_id` | `String` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |


# Example

```ruby
aup_acknowledge_request = AupAcknowledgeRequest.new(
  ChoiceEnum::ACKNOWLEDGE_AND_CONTINUE,
  'description_digest2',
  'evaluation_id8'
)
```



