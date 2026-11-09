# Sandbox Evidence Receipt

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlNhbmRib3hFdmlkZW5jZVJlY2VpcHQ

SandboxEvidenceReceipt.


# Class Name

`SandboxEvidenceReceipt`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | [`ActionEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/action.md) | Required | Action. |
| `environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidence_class` | [`EvidenceClass3Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/evidence-class-3.md) | Required | Evidence class. |
| `external_send` | `String` | Required, Constant | External send.<br><br>**Value**: `'FROZEN'` |
| `invoice_id` | String | Required | This is a container for any-of cases. |
| `observed_at` | `String` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypal_debug_id` | String | Required | This is a container for any-of cases. |
| `proof_kind` | `String` | Required, Constant | Proof kind.<br><br>**Value**: `'POST_RESPONSE_ONLY'` |
| `schema_version` | `Integer` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `separate_get_readback` | `String` | Required, Constant | Separate get readback.<br><br>**Value**: `'False'` |
| `status` | [`Status10Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/status-10.md) | Required | Status. |


# Example

```ruby
sandbox_evidence_receipt = SandboxEvidenceReceipt.new(
  ActionEnum::OAUTH_CONNECT,
  'sandbox',
  EvidenceClass3Enum::AUTHENTIC_SANDBOX_RESPONSE,
  'FROZEN',
  'String9',
  'observed_at2',
  'String9',
  'POST_RESPONSE_ONLY',
  1,
  'False',
  Status10Enum::CONNECTED
)
```



