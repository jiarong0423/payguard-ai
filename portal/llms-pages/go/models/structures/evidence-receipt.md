# Evidence Receipt

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkV2aWRlbmNlUmVjZWlwdA

Evidence receipt.


# Class Name

`EvidenceReceipt`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Action` | [`*models.ActionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/action.md) | Optional | Action. |
| `Environment` | [`*models.EnvironmentEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/environment.md) | Optional | Environment. |
| `EvidenceClass` | [`*models.EvidenceClass3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/evidence-class-3.md) | Optional | Evidence class. |
| `ExternalSend` | [`*models.ExternalSend1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/external-send-1.md) | Optional | External send. |
| `InvoiceId` | [`*models.EvidenceReceiptInvoiceId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/evidence-receipt-invoice-id.md) | Optional | This is a container for any-of cases. |
| `ObservedAt` | `*string` | Optional | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `PaypalDebugId` | [`*models.EvidenceReceiptPaypalDebugId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/evidence-receipt-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `ProofKind` | [`*models.ProofKindEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/proof-kind.md) | Optional | Proof kind. |
| `SchemaVersion` | [`*models.SchemaVersion1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/schema-version-1.md) | Optional | Schema version. |
| `SeparateGetReadback` | `*bool` | Optional | Separate get readback. |
| `Status` | [`*models.Status10Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/status-10.md) | Optional | Status. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    evidenceReceipt := models.EvidenceReceipt{
        Action:               models.ToPointer(models.ActionEnum_OAUTHCONNECT),
        Environment:          models.ToPointer(models.EnvironmentEnum_SANDBOX),
        EvidenceClass:        models.ToPointer(models.EvidenceClass3Enum_AUTHENTICSANDBOXRESPONSE),
        ExternalSend:         models.ToPointer(models.ExternalSend1Enum_FROZEN),
        InvoiceId:            models.ToPointer(models.EvidenceReceiptInvoiceIdContainer.FromString("String1")),
    }

}
```



