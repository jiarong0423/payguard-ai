# Aup Acknowledge Request

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVxdWVzdA

AupAcknowledgeRequest.


# Class Name

`AupAcknowledgeRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `choice` | [`ChoiceEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/choice.md) | Required | Choice. |
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



