# Sandbox Evidence Receipt

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlNhbmRib3hFdmlkZW5jZVJlY2VpcHQ

SandboxEvidenceReceipt.


# Class Name

`SandboxEvidenceReceipt`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Action` | [`models.ActionEnum`](http://localhost:3000/llms-pages/go/models/enumerations/action.md) | Required | Action. |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceClass` | [`models.EvidenceClass3Enum`](http://localhost:3000/llms-pages/go/models/enumerations/evidence-class-3.md) | Required | Evidence class. |
| `ExternalSend` | `string` | Required, Constant | External send.<br><br>**Value**: `"FROZEN"` |
| `InvoiceId` | [`models.SandboxEvidenceReceiptInvoiceId`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/sandbox-evidence-receipt-invoice-id.md) | Required | This is a container for any-of cases. |
| `ObservedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `PaypalDebugId` | [`models.SandboxEvidenceReceiptPaypalDebugId`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/sandbox-evidence-receipt-paypal-debug-id.md) | Required | This is a container for any-of cases. |
| `ProofKind` | `string` | Required, Constant | Proof kind.<br><br>**Value**: `"POST_RESPONSE_ONLY"` |
| `SchemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `SeparateGetReadback` | `string` | Required, Constant | Separate get readback.<br><br>**Value**: `"False"` |
| `Status` | [`models.Status10Enum`](http://localhost:3000/llms-pages/go/models/enumerations/status-10.md) | Required | Status. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    sandboxEvidenceReceipt := models.SandboxEvidenceReceipt{
        Action:              models.ActionEnum_OAUTHCONNECT,
        Environment:         "sandbox",
        EvidenceClass:       models.EvidenceClass3Enum_AUTHENTICSANDBOXRESPONSE,
        ExternalSend:        "FROZEN",
        InvoiceId:           models.SandboxEvidenceReceiptInvoiceIdContainer.FromString("String5"),
        ObservedAt:          "observed_at8",
        PaypalDebugId:       models.SandboxEvidenceReceiptPaypalDebugIdContainer.FromString("String5"),
        ProofKind:           "POST_RESPONSE_ONLY",
        SchemaVersion:       1,
        SeparateGetReadback: "False",
        Status:              models.Status10Enum_CONNECTED,
    }

}
```



