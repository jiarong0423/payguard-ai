# Invoice Review Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkludm9pY2VSZXZpZXdSZXF1ZXN0

InvoiceReviewRequest.


# Class Name

`InvoiceReviewRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AcknowledgementToken` | [`*models.InvoiceReviewRequestAcknowledgementToken`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/invoice-review-request-acknowledgement-token.md) | Optional | This is a container for any-of cases. |
| `Amount` | `string` | Required | Amount.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,9}(?:\.[0-9]{1,2})?$` |
| `ConfirmSandboxDraft` | `bool` | Required | Confirm sandbox draft. |
| `Currency` | [`models.CurrencyEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/currency.md) | Required | Currency. |
| `Description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` |
| `DescriptionDigest` | [`*models.InvoiceReviewRequestDescriptionDigest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/invoice-review-request-description-digest.md) | Optional | This is a container for any-of cases. |
| `EvaluationId` | [`*models.InvoiceReviewRequestEvaluationId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/invoice-review-request-evaluation-id.md) | Optional | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    invoiceReviewRequest := models.InvoiceReviewRequest{
        AcknowledgementToken: models.ToPointer(models.InvoiceReviewRequestAcknowledgementTokenContainer.FromString("String7")),
        Amount:               "amount8",
        ConfirmSandboxDraft:  false,
        Currency:             models.CurrencyEnum_USD,
        Description:          "description6",
        DescriptionDigest:    models.ToPointer(models.InvoiceReviewRequestDescriptionDigestContainer.FromString("String5")),
        EvaluationId:         models.ToPointer(models.InvoiceReviewRequestEvaluationIdContainer.FromString("String1")),
    }

}
```



