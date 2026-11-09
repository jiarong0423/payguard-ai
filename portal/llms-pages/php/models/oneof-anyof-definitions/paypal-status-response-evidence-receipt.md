# Paypal Status Response Evidence Receipt

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlBheXBhbFN0YXR1c1Jlc3BvbnNlRXZpZGVuY2VSZWNlaXB0


# Data Type

`SandboxEvidenceReceipt`


# Cases

| Type |
|  --- |
| [`SandboxEvidenceReceipt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/sandbox-evidence-receipt.md) |


# SandboxEvidenceReceipt

## Initialization Code

### Example

```php
$value = SandboxEvidenceReceiptBuilder::init(
    ActionEnum::OAUTH_CONNECT,
    EvidenceClass3Enum::AUTHENTIC_SANDBOX_RESPONSE,
    'String5',
    'observed_at8',
    'String5',
    Status10Enum::CONNECTED
)->build();
```



