# Paypal Status Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlBheXBhbFN0YXR1c1Jlc3BvbnNl

PaypalStatusResponse.


# Class Name

`PaypalStatusResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `configured` | `bool` | Required | Configured. | getConfigured(): bool | setConfigured(bool configured): void |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` | getEnvironment(): string | setEnvironment(string environment): void |
| `evidenceReceipt` | [SandboxEvidenceReceipt](http://localhost:3000/llms-pages/php/models/structures/sandbox-evidence-receipt.md) | Required | This is a container for any-of cases. | getEvidenceReceipt(): SandboxEvidenceReceipt | setEvidenceReceipt(SandboxEvidenceReceipt evidenceReceipt): void |
| `lastVerifiedAt` | string | Required | This is a container for any-of cases. | getLastVerifiedAt(): string | setLastVerifiedAt(string lastVerifiedAt): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'paypal_sandbox'` | getSource(): string | setSource(string source): void |
| `status` | [`string(Status11Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/status-11.md) | Required | Status. | getStatus(): string | setStatus(string status): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\PaypalStatusResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\SandboxEvidenceReceiptBuilder;
use TradeGlotLocalConsoleLib\Models\ActionEnum;
use TradeGlotLocalConsoleLib\Models\EvidenceClass3Enum;
use TradeGlotLocalConsoleLib\Models\Status10Enum;
use TradeGlotLocalConsoleLib\Models\Status11Enum;

$paypalStatusResponse = PaypalStatusResponseBuilder::init(
    false,
    SandboxEvidenceReceiptBuilder::init(
        ActionEnum::OAUTH_CONNECT,
        EvidenceClass3Enum::AUTHENTIC_SANDBOX_RESPONSE,
        'String5',
        'observed_at8',
        'String5',
        Status10Enum::CONNECTED
    )->build(),
    'String3',
    Status11Enum::CONNECTED
)->build();
```



