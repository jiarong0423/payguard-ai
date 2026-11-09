# Invoice Draft Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkludm9pY2VEcmFmdFJlc3BvbnNl

InvoiceDraftResponse.


# Class Name

`InvoiceDraftResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` | getEnvironment(): string | setEnvironment(string environment): void |
| `evidenceReceipt` | [`SandboxEvidenceReceipt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/sandbox-evidence-receipt.md) | Required | SandboxEvidenceReceipt. | getEvidenceReceipt(): SandboxEvidenceReceipt | setEvidenceReceipt(SandboxEvidenceReceipt evidenceReceipt): void |
| `externalSend` | `string` | Required, Constant | External send.<br><br>**Value**: `'FROZEN'` | getExternalSend(): string | setExternalSend(string externalSend): void |
| `invoiceId` | `string` | Required | Invoice id.<br><br>**Constraints**: *Minimum Length*: `13`, *Maximum Length*: `69`, *Pattern*: `^INV2-[A-Z0-9-]{8,64}$` | getInvoiceId(): string | setInvoiceId(string invoiceId): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'paypal_sandbox'` | getSource(): string | setSource(string source): void |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'DRAFT'` | getStatus(): string | setStatus(string status): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\InvoiceDraftResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\SandboxEvidenceReceiptBuilder;
use TradeGlotLocalConsoleLib\Models\ActionEnum;
use TradeGlotLocalConsoleLib\Models\EvidenceClass3Enum;
use TradeGlotLocalConsoleLib\Models\Status10Enum;

$invoiceDraftResponse = InvoiceDraftResponseBuilder::init(
    SandboxEvidenceReceiptBuilder::init(
        ActionEnum::OAUTH_CONNECT,
        EvidenceClass3Enum::AUTHENTIC_SANDBOX_RESPONSE,
        'String3',
        'observed_at6',
        'String3',
        Status10Enum::CONNECTED
    )->build(),
    'invoice_id6'
)->build();
```



