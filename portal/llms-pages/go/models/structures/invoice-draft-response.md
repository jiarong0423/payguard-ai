# Invoice Draft Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkludm9pY2VEcmFmdFJlc3BvbnNl

InvoiceDraftResponse.


# Class Name

`InvoiceDraftResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceReceipt` | [`models.SandboxEvidenceReceipt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/sandbox-evidence-receipt.md) | Required | SandboxEvidenceReceipt. |
| `ExternalSend` | `string` | Required, Constant | External send.<br><br>**Value**: `"FROZEN"` |
| `InvoiceId` | `string` | Required | Invoice id.<br><br>**Constraints**: *Minimum Length*: `13`, *Maximum Length*: `69`, *Pattern*: `^INV2-[A-Z0-9-]{8,64}$` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"paypal_sandbox"` |
| `Status` | `string` | Required, Constant | Status.<br><br>**Value**: `"DRAFT"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    invoiceDraftResponse := models.InvoiceDraftResponse{
        Environment:     "sandbox",
        EvidenceReceipt: models.SandboxEvidenceReceipt{
            Action:              models.ActionEnum_OAUTHCONNECT,
            Environment:         "sandbox",
            EvidenceClass:       models.EvidenceClass3Enum_AUTHENTICSANDBOXRESPONSE,
            ExternalSend:        "FROZEN",
            InvoiceId:           models.SandboxEvidenceReceiptInvoiceIdContainer.FromString("String3"),
            ObservedAt:          "observed_at6",
            PaypalDebugId:       models.SandboxEvidenceReceiptPaypalDebugIdContainer.FromString("String3"),
            ProofKind:           "POST_RESPONSE_ONLY",
            SchemaVersion:       1,
            SeparateGetReadback: "False",
            Status:              models.Status10Enum_CONNECTED,
        },
        ExternalSend:    "FROZEN",
        InvoiceId:       "invoice_id6",
        Source:          "paypal_sandbox",
        Status:          "DRAFT",
    }

}
```



