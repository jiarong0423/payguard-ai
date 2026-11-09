# Sandbox Evidence Receipt

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlNhbmRib3hFdmlkZW5jZVJlY2VpcHQ

SandboxEvidenceReceipt.


# Class Name

`SandboxEvidenceReceipt`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `action` | [`string(ActionEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/action.md) | Required | Action. | getAction(): string | setAction(string action): void |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` | getEnvironment(): string | setEnvironment(string environment): void |
| `evidenceClass` | [`string(EvidenceClass3Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/evidence-class-3.md) | Required | Evidence class. | getEvidenceClass(): string | setEvidenceClass(string evidenceClass): void |
| `externalSend` | `string` | Required, Constant | External send.<br><br>**Value**: `'FROZEN'` | getExternalSend(): string | setExternalSend(string externalSend): void |
| `invoiceId` | string | Required | This is a container for any-of cases. | getInvoiceId(): string | setInvoiceId(string invoiceId): void |
| `observedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` | getObservedAt(): string | setObservedAt(string observedAt): void |
| `paypalDebugId` | string | Required | This is a container for any-of cases. | getPaypalDebugId(): string | setPaypalDebugId(string paypalDebugId): void |
| `proofKind` | `string` | Required, Constant | Proof kind.<br><br>**Value**: `'POST_RESPONSE_ONLY'` | getProofKind(): string | setProofKind(string proofKind): void |
| `schemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` | getSchemaVersion(): int | setSchemaVersion(int schemaVersion): void |
| `separateGetReadback` | `string` | Required, Constant | Separate get readback.<br><br>**Value**: `'False'` | getSeparateGetReadback(): string | setSeparateGetReadback(string separateGetReadback): void |
| `status` | [`string(Status10Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/status-10.md) | Required | Status. | getStatus(): string | setStatus(string status): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\SandboxEvidenceReceiptBuilder;
use TradeGlotLocalConsoleLib\Models\ActionEnum;
use TradeGlotLocalConsoleLib\Models\EvidenceClass3Enum;
use TradeGlotLocalConsoleLib\Models\Status10Enum;

$sandboxEvidenceReceipt = SandboxEvidenceReceiptBuilder::init(
    ActionEnum::OAUTH_CONNECT,
    EvidenceClass3Enum::AUTHENTIC_SANDBOX_RESPONSE,
    'String5',
    'observed_at8',
    'String5',
    Status10Enum::CONNECTED
)->build();
```



