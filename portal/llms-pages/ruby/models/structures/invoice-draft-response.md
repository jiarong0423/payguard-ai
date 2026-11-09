# Invoice Draft Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkludm9pY2VEcmFmdFJlc3BvbnNl

InvoiceDraftResponse.


# Class Name

`InvoiceDraftResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidence_receipt` | [`SandboxEvidenceReceipt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/sandbox-evidence-receipt.md) | Required | SandboxEvidenceReceipt. |
| `external_send` | `String` | Required, Constant | External send.<br><br>**Value**: `'FROZEN'` |
| `invoice_id` | `String` | Required | Invoice id.<br><br>**Constraints**: *Minimum Length*: `13`, *Maximum Length*: `69`, *Pattern*: `^INV2-[A-Z0-9-]{8,64}$` |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'paypal_sandbox'` |
| `status` | `String` | Required, Constant | Status.<br><br>**Value**: `'DRAFT'` |


# Example

```ruby
invoice_draft_response = InvoiceDraftResponse.new(
  'sandbox',
  SandboxEvidenceReceipt.new(
    ActionEnum::OAUTH_CONNECT,
    'sandbox',
    EvidenceClass3Enum::AUTHENTIC_SANDBOX_RESPONSE,
    'FROZEN',
    'String3',
    'observed_at6',
    'String3',
    'POST_RESPONSE_ONLY',
    1,
    'False',
    Status10Enum::CONNECTED
  ),
  'FROZEN',
  'invoice_id8',
  'paypal_sandbox',
  'DRAFT'
)
```



