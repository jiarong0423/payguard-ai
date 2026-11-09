# Dispute Detail Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkRpc3B1dGVEZXRhaWxSZXNwb25zZQ

DisputeDetailResponse.


# Class Name

`DisputeDetailResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `create_time` | `String` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` |
| `data_source_label` | [`DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/data-source-label.md) | Required | Data source label. |
| `dispute_amount` | [`ProviderMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/provider-money.md) | Required | ProviderMoney. |
| `dispute_channel` | String \| nil | Optional | This is a container for any-of cases. |
| `dispute_id` | `String` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `dispute_life_cycle_stage` | [`DisputeLifeCycleStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `dispute_state` | String \| nil | Optional | This is a container for any-of cases. |
| `disputed_transactions` | [`Array[DisputedTransaction]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/disputed-transaction.md) | Required | Disputed transactions.<br><br>**Constraints**: *Maximum Items*: `10` |
| `environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidence_class` | [`EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `evidences` | [`Array[DisputeEvidenceRow]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/dispute-evidence-row.md) | Required | Evidences.<br><br>**Constraints**: *Maximum Items*: `20` |
| `observed_at` | `String` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypal_debug_id` | String \| nil | Optional | This is a container for any-of cases. |
| `provider_submission` | [`ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `readback` | `String` | Required, Constant | Readback.<br><br>**Value**: `'GET_DETAIL'` |
| `reason` | [`Reason2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/reason-2.md) | Required | Reason. |
| `seller_response_due_date` | String \| nil | Optional | This is a container for any-of cases. |
| `source` | [`SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/source.md) | Required | Source. |
| `status` | [`Status3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/status-3.md) | Required | Status. |
| `update_time` | String \| nil | Optional | This is a container for any-of cases. |


# Example

```ruby
dispute_detail_response = DisputeDetailResponse.new(
  'create_time6',
  DataSourceLabelEnum::SANDBOX,
  ProviderMoney.new(
    'currency_code6',
    'value0'
  ),
  'dispute_id2',
  DisputeLifeCycleStageEnum::UNKNOWN,
  [
    DisputedTransaction.new(
      'seller_transaction_id2',
      ProviderMoney.new(
        'currency_code0',
        'value6'
      ),
      true,
      'String7'
    )
  ],
  'sandbox',
  EvidenceClassEnum::AUTHENTIC_SANDBOX_RESPONSE,
  [
    DisputeEvidenceRow.new(
      'evidence_type2',
      Source3Enum::SUBMITTED_BY_PARTNER,
      'String1',
      'String9'
    )
  ],
  'observed_at4',
  ProviderSubmissionEnum::NOT_PERFORMED,
  'GET_DETAIL',
  Reason2Enum::CANCELED_RECURRING_BILLING,
  SourceEnum::PAYPAL_SANDBOX,
  Status3Enum::RESOLVED,
  'String5',
  'String9',
  'String1',
  'String9',
  'String3'
)
```



