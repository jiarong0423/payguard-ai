# Provide Evidence Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlc3BvbnNl

ProvideEvidenceResponse.


# Class Name

`ProvideEvidenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_ref` | `String` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `confirm_token` | String \| nil | Optional | This is a container for any-of cases. |
| `content_type` | `String` | Required, Constant | Content type.<br><br>**Value**: `'multipart/form-data'` |
| `data_source_label` | [`DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/data-source-label.md) | Required | Data source label. |
| `dispute_id` | `String` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidence_class` | [`EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `external_send` | [`ExternalSendEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/external-send.md) | Required | External send. |
| `files` | [`Array[MultipartFilePart]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/multipart-file-part.md) | Required | Files.<br><br>**Constraints**: *Maximum Items*: `20` |
| `human_review_required` | `String` | Required, Constant | Human review required.<br><br>**Value**: `'True'` |
| `input` | [`EvidenceInput`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/evidence-input.md) | Required | EvidenceInput. |
| `method` | `String` | Required, Constant | Method.<br><br>**Value**: `'POST'` |
| `observed_at` | `String` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `path` | `String` | Required | Path.<br><br>**Constraints**: *Pattern*: `^/v1/customer/disputes/PP-[A-Z0-9][A-Z0-9-]{2,62}/provide-evidence$` |
| `payload_sha_256` | String \| nil | Optional | This is a container for any-of cases. |
| `paypal_debug_id` | String \| nil | Optional | This is a container for any-of cases. |
| `provider_submission` | [`ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `readback` | [`Readback1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/readback-1.md) | Required | Readback. |
| `send_guard` | [`SendGuard`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). |
| `sent_files` | Array[[SentFileFingerprint](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/sent-file-fingerprint.md)] \| nil | Optional | This is a container for any-of cases. |
| `source` | [`SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/source.md) | Required | Source. |
| `submit_flag_enabled` | `TrueClass \| FalseClass` | Required | Submit flag enabled. |


# Example

```ruby
provide_evidence_response = ProvideEvidenceResponse.new(
  'case_ref4',
  'multipart/form-data',
  DataSourceLabelEnum::SANDBOX,
  'dispute_id2',
  'sandbox',
  EvidenceClassEnum::SYNTHETIC_TEST_RESPONSE,
  ExternalSendEnum::FROZEN,
  [
    MultipartFilePart.new(
      68,
      ContentTypeEnum::ENUM_IMAGEPNG,
      'filename6',
      'name4'
    )
  ],
  'True',
  EvidenceInput.new(
    [
      EvidenceInputItem.new(
        EvidenceInfo.new(
          [
            TrackingInfo.new(
              CarrierNameEnum::DHL,
              'tracking_number6',
              'String1'
            )
          ]
        ),
        'evidence_type2',
        'notes2'
      )
    ]
  ),
  'POST',
  'observed_at4',
  'path4',
  ProviderSubmissionEnum::NOT_PERFORMED,
  Readback1Enum::PROVIDE_EVIDENCE_PREVIEW,
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
  'String1',
  'String1',
  'String1',
  [
    SentFileFingerprint.new(
      196,
      ContentTypeEnum::ENUM_IMAGEPNG,
      'filename6',
      'sha2566'
    )
  ]
)
```



