# Paypal Status Response

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlBheXBhbFN0YXR1c1Jlc3BvbnNl

PaypalStatusResponse.


# Class Name

`PaypalStatusResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `configured` | `TrueClass \| FalseClass` | Required | Configured. |
| `environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` |
| `evidence_receipt` | [SandboxEvidenceReceipt](http://localhost:3000/llms-pages/ruby/models/structures/sandbox-evidence-receipt.md) | Required | This is a container for any-of cases. |
| `last_verified_at` | String | Required | This is a container for any-of cases. |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'paypal_sandbox'` |
| `status` | [`Status11Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/status-11.md) | Required | Status. |


# Example

```ruby
paypal_status_response = PaypalStatusResponse.new(
  false,
  'sandbox',
  SandboxEvidenceReceipt.new(
    ActionEnum::OAUTH_CONNECT,
    'sandbox',
    EvidenceClass3Enum::AUTHENTIC_SANDBOX_RESPONSE,
    'FROZEN',
    'String5',
    'observed_at8',
    'String5',
    'POST_RESPONSE_ONLY',
    1,
    'False',
    Status10Enum::CONNECTED
  ),
  'String3',
  'paypal_sandbox',
  Status11Enum::CONNECTED
)
```



