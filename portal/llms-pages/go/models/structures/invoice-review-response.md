# Invoice Review Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkludm9pY2VSZXZpZXdSZXNwb25zZQ

InvoiceReviewResponse.


# Class Name

`InvoiceReviewResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Action` | `string` | Required, Constant | Action.<br><br>**Value**: `"create_sandbox_invoice_draft"` |
| `AdvisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `AuthenticatedActor` | `string` | Required, Constant | Authenticated actor.<br><br>**Value**: `"False"` |
| `ExpiresAt` | `string` | Required | Expires at. |
| `Limitations` | `[]string` | Required | Limitations. |
| `PayloadDigest` | `string` | Required | Payload digest. |
| `PolicyStatus` | `string` | Required, Constant | Policy status.<br><br>**Value**: `"manual_review"` |
| `ReviewToken` | `string` | Required | Review token. |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    invoiceReviewResponse := models.InvoiceReviewResponse{
        Action:             "create_sandbox_invoice_draft",
        AdvisoryOnly:       "True",
        AuthenticatedActor: "False",
        ExpiresAt:          "expires_at8",
        Limitations:        []string{
            "limitations5",
            "limitations6",
        },
        PayloadDigest:      "payload_digest8",
        PolicyStatus:       "manual_review",
        ReviewToken:        "review_token6",
        Source:             "synthetic",
    }

}
```



