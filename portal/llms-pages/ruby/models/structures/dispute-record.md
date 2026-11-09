# Dispute Record

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkRpc3B1dGVSZWNvcmQ

DisputeRecord.


# Class Name

`DisputeRecord`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `create_time` | `String` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` |
| `dispute_amount` | [`ProviderMoney`](http://localhost:3000/llms-pages/ruby/models/structures/provider-money.md) | Required | ProviderMoney. |
| `dispute_id` | `String` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `dispute_life_cycle_stage` | [`DisputeLifeCycleStageEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `dispute_state` | String \| nil | Optional | This is a container for any-of cases. |
| `reason` | [`Reason2Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/reason-2.md) | Required | Reason. |
| `seller_response_due_date` | String \| nil | Optional | This is a container for any-of cases. |
| `status` | [`Status3Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/status-3.md) | Required | Status. |
| `update_time` | String \| nil | Optional | This is a container for any-of cases. |


# Example

```ruby
dispute_record = DisputeRecord.new(
  'create_time6',
  ProviderMoney.new(
    'currency_code6',
    'value0'
  ),
  'dispute_id2',
  DisputeLifeCycleStageEnum::UNKNOWN,
  Reason2Enum::INCORRECT_AMOUNT,
  Status3Enum::CLOSED,
  'String9',
  'String9',
  'String9'
)
```



