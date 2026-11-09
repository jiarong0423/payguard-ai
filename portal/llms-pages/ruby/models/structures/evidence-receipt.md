# Evidence Receipt

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkV2aWRlbmNlUmVjZWlwdA

Evidence receipt.


# Class Name

`EvidenceReceipt`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | [`ActionEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/action.md) | Optional | Action. |
| `environment` | [`EnvironmentEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/environment.md) | Optional | Environment. |
| `evidence_class` | [`EvidenceClass3Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/evidence-class-3.md) | Optional | Evidence class. |
| `external_send` | [`ExternalSend1Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/external-send-1.md) | Optional | External send. |
| `invoice_id` | String \| nil | Optional | This is a container for any-of cases. |
| `observed_at` | `String` | Optional | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypal_debug_id` | String \| nil | Optional | This is a container for any-of cases. |
| `proof_kind` | [`ProofKindEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/proof-kind.md) | Optional | Proof kind. |
| `schema_version` | [`SchemaVersion1Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/schema-version-1.md) | Optional | Schema version. |
| `separate_get_readback` | `TrueClass \| FalseClass` | Optional | Separate get readback. |
| `status` | [`Status10Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/status-10.md) | Optional | Status. |


# Example

```ruby
evidence_receipt = EvidenceReceipt.new(
  ActionEnum::OAUTH_CONNECT,
  EnvironmentEnum::SANDBOX,
  EvidenceClass3Enum::AUTHENTIC_SANDBOX_RESPONSE,
  ExternalSend1Enum::FROZEN,
  'String3',
  nil,
  nil,
  envrr,
  envrr,
  nil,
  envrr
)
```



