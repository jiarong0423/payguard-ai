# Paypal Status Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlBheXBhbFN0YXR1c1Jlc3BvbnNl

PaypalStatusResponse.


# Class Name

`PaypalStatusResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Configured` | `bool` | Required | Configured. |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceReceipt` | [`models.PaypalStatusResponseEvidenceReceipt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/paypal-status-response-evidence-receipt.md) | Required | This is a container for any-of cases. |
| `LastVerifiedAt` | [`models.PaypalStatusResponseLastVerifiedAt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/paypal-status-response-last-verified-at.md) | Required | This is a container for any-of cases. |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"paypal_sandbox"` |
| `Status` | [`models.Status11Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/status-11.md) | Required | Status. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    paypalStatusResponse := models.PaypalStatusResponse{
        Configured:      false,
        Environment:     "sandbox",
        EvidenceReceipt: models.PaypalStatusResponseEvidenceReceiptContainer.FromSandboxEvidenceReceipt(models.SandboxEvidenceReceipt{
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
        }),
        LastVerifiedAt:  models.PaypalStatusResponseLastVerifiedAtContainer.FromString("String3"),
        Source:          "paypal_sandbox",
        Status:          models.Status11Enum_CONNECTED,
    }

}
```



