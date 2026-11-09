# Invoice Review Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkludm9pY2VSZXZpZXdSZXF1ZXN0

InvoiceReviewRequest.


# Class Name

`InvoiceReviewRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AcknowledgementToken` | [`InvoiceReviewRequestAcknowledgementToken`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/invoice-review-request-acknowledgement-token.md) | Optional | This is a container for any-of cases. | InvoiceReviewRequestAcknowledgementToken getAcknowledgementToken() | setAcknowledgementToken(InvoiceReviewRequestAcknowledgementToken acknowledgementToken) |
| `Amount` | `String` | Required | Amount.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,9}(?:\.[0-9]{1,2})?$` | String getAmount() | setAmount(String amount) |
| `ConfirmSandboxDraft` | `boolean` | Required | Confirm sandbox draft. | boolean getConfirmSandboxDraft() | setConfirmSandboxDraft(boolean confirmSandboxDraft) |
| `Currency` | [`CurrencyEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/currency.md) | Required | Currency. | CurrencyEnum getCurrency() | setCurrency(CurrencyEnum currency) |
| `Description` | `String` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` | String getDescription() | setDescription(String description) |
| `DescriptionDigest` | [`InvoiceReviewRequestDescriptionDigest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/invoice-review-request-description-digest.md) | Optional | This is a container for any-of cases. | InvoiceReviewRequestDescriptionDigest getDescriptionDigest() | setDescriptionDigest(InvoiceReviewRequestDescriptionDigest descriptionDigest) |
| `EvaluationId` | [`InvoiceReviewRequestEvaluationId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/invoice-review-request-evaluation-id.md) | Optional | This is a container for any-of cases. | InvoiceReviewRequestEvaluationId getEvaluationId() | setEvaluationId(InvoiceReviewRequestEvaluationId evaluationId) |


# Example

```java
import m18000.m0.m0.m127.models.CurrencyEnum;
import m18000.m0.m0.m127.models.InvoiceReviewRequest;
import m18000.m0.m0.m127.models.containers.InvoiceReviewRequestAcknowledgementToken;
import m18000.m0.m0.m127.models.containers.InvoiceReviewRequestDescriptionDigest;
import m18000.m0.m0.m127.models.containers.InvoiceReviewRequestEvaluationId;

InvoiceReviewRequest invoiceReviewRequest = new InvoiceReviewRequest.Builder(
    "amount8",
    false,
    CurrencyEnum.USD,
    "description6"
)
.acknowledgementToken(InvoiceReviewRequestAcknowledgementToken.fromString(
        "String7"
    ))
.descriptionDigest(InvoiceReviewRequestDescriptionDigest.fromString(
        "String5"
    ))
.evaluationId(InvoiceReviewRequestEvaluationId.fromString(
        "String1"
    ))
.build();
```



