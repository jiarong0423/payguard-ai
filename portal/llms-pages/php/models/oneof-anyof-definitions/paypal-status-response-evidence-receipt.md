# Paypal Status Response Evidence Receipt

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlBheXBhbFN0YXR1c1Jlc3BvbnNlRXZpZGVuY2VSZWNlaXB0


# Data Type

`SandboxEvidenceReceipt`


# Cases

| Type |
|  --- |
| [`SandboxEvidenceReceipt`](http://localhost:3000/llms-pages/php/models/structures/sandbox-evidence-receipt.md) |


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



