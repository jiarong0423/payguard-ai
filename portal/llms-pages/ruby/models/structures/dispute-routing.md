# Dispute Routing

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkRpc3B1dGVSb3V0aW5n

DisputeRouting.


# Class Name

`DisputeRouting`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `available_actions` | `Array[String]` | Required | Available actions.<br><br>**Constraints**: *Maximum Items*: `20` |
| `dispute_life_cycle_stage` | [`DisputeLifeCycleStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `due_state` | [`DueStateEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/due-state.md) | Required | Due state. |
| `human_review_required` | `String` | Required, Constant | Human review required.<br><br>**Value**: `'True'` |
| `overall_state` | [`OverallStateEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/overall-state.md) | Required | Overall state. |
| `provider_submission` | `String` | Required, Constant | Provider submission.<br><br>**Value**: `'NOT_PERFORMED'` |
| `reason` | [`Reason2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/reason-2.md) | Required | Reason. |
| `requirements` | [`Array[DisputeRequirement]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/dispute-requirement.md) | Required | Requirements.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `schema_version` | `Integer` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `seller_response_due_date` | `String` | Required | Seller response due date.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `snapshot_class` | `String` | Required, Constant | Snapshot class.<br><br>**Value**: `'SYNTHETIC_PROVIDER_FIXTURE'` |
| `status` | [`Status3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/status-3.md) | Required | Status. |


# Example

```ruby
dispute_routing = DisputeRouting.new(
  [
    'available_actions2',
    'available_actions3'
  ],
  DisputeLifeCycleStageEnum::CHARGEBACK,
  DueStateEnum::OPEN,
  'True',
  OverallStateEnum::DUE_DATE_EXPIRED,
  'NOT_PERFORMED',
  Reason2Enum::DUPLICATE_TRANSACTION,
  [
    DisputeRequirement.new(
      20,
      false,
      60,
      'provider_evidence_type0',
      'request_id8',
      RequirementStateEnum::CONTEXT_ONLY,
      'source2',
      'String5',
      'String3'
    )
  ],
  1,
  'seller_response_due_date0',
  'SYNTHETIC_PROVIDER_FIXTURE',
  Status3Enum::OPEN
)
```



