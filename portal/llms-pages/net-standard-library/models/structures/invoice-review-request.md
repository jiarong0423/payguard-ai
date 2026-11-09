# Invoice Review Request

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkludm9pY2VSZXZpZXdSZXF1ZXN0

InvoiceReviewRequest.


# Class Name

`InvoiceReviewRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AcknowledgementToken` | [`InvoiceReviewRequestAcknowledgementToken`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/invoice-review-request-acknowledgement-token.md) | Optional | This is a container for any-of cases. |
| `Amount` | `string` | Required | Amount.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,9}(?:\.[0-9]{1,2})?$` |
| `ConfirmSandboxDraft` | `bool` | Required | Confirm sandbox draft. |
| `Currency` | [`CurrencyEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/currency.md) | Required | Currency. |
| `Description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` |
| `DescriptionDigest` | [`InvoiceReviewRequestDescriptionDigest`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/invoice-review-request-description-digest.md) | Optional | This is a container for any-of cases. |
| `EvaluationId` | [`InvoiceReviewRequestEvaluationId`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/invoice-review-request-evaluation-id.md) | Optional | This is a container for any-of cases. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

InvoiceReviewRequest invoiceReviewRequest = new InvoiceReviewRequest
{
    Amount = "amount8",
    ConfirmSandboxDraft = false,
    Currency = CurrencyEnum.USD,
    Description = "description6",
    AcknowledgementToken = InvoiceReviewRequestAcknowledgementToken.FromString("String7"),
    DescriptionDigest = InvoiceReviewRequestDescriptionDigest.FromString("String5"),
    EvaluationId = InvoiceReviewRequestEvaluationId.FromString("String1"),
};
```



