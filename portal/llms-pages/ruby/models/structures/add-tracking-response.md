# Add Tracking Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkFkZFRyYWNraW5nUmVzcG9uc2U

AddTrackingResponse.


# Class Name

`AddTrackingResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`TrackerBatch`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/tracker-batch.md) | Required | TrackerBatch. |
| `case_ref` | `String` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `confirm_token` | String \| nil | Optional | This is a container for any-of cases. |
| `content_type` | `String` | Required, Constant | Content type.<br><br>**Value**: `'application/json'` |
| `data_source_label` | [`DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/data-source-label.md) | Required | Data source label. |
| `dispute_id` | `String` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidence_class` | [`EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `external_send` | [`ExternalSendEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/external-send.md) | Required | External send. |
| `human_review_required` | `String` | Required, Constant | Human review required.<br><br>**Value**: `'True'` |
| `method` | `String` | Required, Constant | Method.<br><br>**Value**: `'POST'` |
| `observed_at` | `String` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `path` | `String` | Required, Constant | Path.<br><br>**Value**: `'/v1/shipping/trackers-batch'` |
| `payload_sha_256` | String \| nil | Optional | This is a container for any-of cases. |
| `paypal_debug_id` | String \| nil | Optional | This is a container for any-of cases. |
| `provider_submission` | [`ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `readback` | [`ReadbackEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/readback.md) | Required | Readback. |
| `send_guard` | [`SendGuard`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). |
| `source` | [`SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/source.md) | Required | Source. |
| `submit_flag_enabled` | `TrueClass \| FalseClass` | Required | Submit flag enabled. |


# Example

```ruby
add_tracking_response = AddTrackingResponse.new(
  TrackerBatch.new(
    [
      TrackerItem.new(
        CarrierEnum::JP_JAPANPOST,
        'SHIPPED',
        'tracking_number0',
        'transaction_id0',
        'String5'
      )
    ]
  ),
  'case_ref0',
  'application/json',
  DataSourceLabelEnum::SANDBOX,
  'dispute_id8',
  'sandbox',
  EvidenceClassEnum::SYNTHETIC_FIXTURE,
  ExternalSendEnum::FROZEN,
  'True',
  'POST',
  'observed_at0',
  '/v1/shipping/trackers-batch',
  ProviderSubmissionEnum::NOT_PERFORMED,
  ReadbackEnum::ADD_TRACKING_PREVIEW,
  SendGuard.new(
    AccountStatusEnum::MATCH,
    'case_ref6',
    'dispute_masked0',
    'String3',
    'String7',
    ProviderMoney.new(
      'currency_code0',
      'value6'
    ),
    'String9',
    'String1'
  ),
  SourceEnum::PAYPAL_SANDBOX,
  false,
  'String5',
  'String5',
  'String5'
)
```



