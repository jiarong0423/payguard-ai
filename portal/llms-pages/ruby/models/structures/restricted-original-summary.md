# Restricted Original Summary

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlJlc3RyaWN0ZWRPcmlnaW5hbFN1bW1hcnk

RestrictedOriginalSummary.


# Class Name

`RestrictedOriginalSummary`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `attachment_count` | `Integer` | Required | Attachment count.<br><br>**Constraints**: `>= 0`, `<= 20` |
| `content_returned` | `String` | Required, Constant | Content returned.<br><br>**Value**: `'False'` |
| `custody` | `String` | Required, Constant | Custody.<br><br>**Value**: `'SESSION_MEMORY_ONLY'` |
| `data_class` | `String` | Required, Constant | Data class.<br><br>**Value**: `'SYNTHETIC_RESTRICTED_EVIDENCE'` |
| `persistent_storage` | `String` | Required, Constant | Persistent storage.<br><br>**Value**: `'NOT_IMPLEMENTED'` |
| `production_pii_vault` | `String` | Required, Constant | Production pii vault.<br><br>**Value**: `'NOT_IMPLEMENTED'` |
| `profile` | `String` | Required, Constant | Profile.<br><br>**Value**: `'RESTRICTED_ORIGINAL_METADATA_V1'` |
| `proof_record_count` | `Integer` | Required | Proof record count.<br><br>**Constraints**: `>= 0`, `<= 128` |
| `provider_submission` | `String` | Required, Constant | Provider submission.<br><br>**Value**: `'NOT_PERFORMED'` |
| `schema_version` | `Integer` | Required, Constant | Schema version.<br><br>**Value**: `1` |


# Example

```ruby
restricted_original_summary = RestrictedOriginalSummary.new(
  20,
  'False',
  'SESSION_MEMORY_ONLY',
  'SYNTHETIC_RESTRICTED_EVIDENCE',
  'NOT_IMPLEMENTED',
  'NOT_IMPLEMENTED',
  'RESTRICTED_ORIGINAL_METADATA_V1',
  96,
  'NOT_PERFORMED',
  1
)
```



