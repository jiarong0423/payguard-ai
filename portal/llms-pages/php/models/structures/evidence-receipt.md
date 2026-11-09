# Evidence Receipt

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkV2aWRlbmNlUmVjZWlwdA

Evidence receipt.


# Class Name

`EvidenceReceipt`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `action` | [`?string(ActionEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/action.md) | Optional | Action. | getAction(): ?string | setAction(?string action): void |
| `environment` | [`?string(EnvironmentEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/environment.md) | Optional | Environment. | getEnvironment(): ?string | setEnvironment(?string environment): void |
| `evidenceClass` | [`?string(EvidenceClass3Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/evidence-class-3.md) | Optional | Evidence class. | getEvidenceClass(): ?string | setEvidenceClass(?string evidenceClass): void |
| `externalSend` | [`?string(ExternalSend1Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/external-send-1.md) | Optional | External send. | getExternalSend(): ?string | setExternalSend(?string externalSend): void |
| `invoiceId` | string\|null | Optional | This is a container for any-of cases. | getInvoiceId(): ?string | setInvoiceId(?string invoiceId): void |
| `observedAt` | `?string` | Optional | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` | getObservedAt(): ?string | setObservedAt(?string observedAt): void |
| `paypalDebugId` | string\|null | Optional | This is a container for any-of cases. | getPaypalDebugId(): ?string | setPaypalDebugId(?string paypalDebugId): void |
| `proofKind` | [`?string(ProofKindEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/proof-kind.md) | Optional | Proof kind. | getProofKind(): ?string | setProofKind(?string proofKind): void |
| `schemaVersion` | [`?int(SchemaVersion1Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/schema-version-1.md) | Optional | Schema version. | getSchemaVersion(): ?int | setSchemaVersion(?int schemaVersion): void |
| `separateGetReadback` | `?bool` | Optional | Separate get readback. | getSeparateGetReadback(): ?bool | setSeparateGetReadback(?bool separateGetReadback): void |
| `status` | [`?string(Status10Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/status-10.md) | Optional | Status. | getStatus(): ?string | setStatus(?string status): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\EvidenceReceiptBuilder;
use TradeGlotLocalConsoleLib\Models\ActionEnum;
use TradeGlotLocalConsoleLib\Models\EnvironmentEnum;
use TradeGlotLocalConsoleLib\Models\EvidenceClass3Enum;
use TradeGlotLocalConsoleLib\Models\ExternalSend1Enum;

$evidenceReceipt = EvidenceReceiptBuilder::init()
    ->action(ActionEnum::OAUTH_CONNECT)
    ->environment(EnvironmentEnum::SANDBOX)
    ->evidenceClass(EvidenceClass3Enum::AUTHENTIC_SANDBOX_RESPONSE)
    ->externalSend(ExternalSend1Enum::FROZEN)
    ->invoiceId(
        'String1'
    )
    ->build();
```



