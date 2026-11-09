# Dispute List Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkRpc3B1dGVMaXN0UmVzcG9uc2U

DisputeListResponse.


# Class Name

`DisputeListResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `data_source_label` | [`DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/data-source-label.md) | Required | Data source label. |
| `environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidence_class` | [`EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `items` | [`Array[DisputeRecord]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/dispute-record.md) | Required | Items.<br><br>**Constraints**: *Maximum Items*: `20` |
| `observed_at` | `String` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypal_debug_id` | String \| nil | Optional | This is a container for any-of cases. |
| `provider_submission` | [`ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `readback` | `String` | Required, Constant | Readback.<br><br>**Value**: `'GET_LIST'` |
| `source` | [`SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/source.md) | Required | Source. |


# Example

```ruby
dispute_list_response = DisputeListResponse.new(
  DataSourceLabelEnum::SANDBOX,
  'sandbox',
  EvidenceClassEnum::SYNTHETIC_FIXTURE,
  [
    DisputeRecord.new(
      'create_time4',
      ProviderMoney.new(
        'currency_code6',
        'value0'
      ),
      'dispute_id0',
      DisputeLifeCycleStageEnum::PRE_ARBITRATION,
      Reason2Enum::CREDIT_NOT_PROCESSED,
      Status3Enum::UNDER_REVIEW,
      'String1',
      'String7',
      'String1'
    )
  ],
  'observed_at4',
  ProviderSubmissionEnum::NOT_PERFORMED,
  'GET_LIST',
  SourceEnum::PAYPAL_SANDBOX,
  'String1'
)
```



