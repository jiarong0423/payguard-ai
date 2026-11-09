# Invoice Review Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkludm9pY2VSZXZpZXdSZXF1ZXN0

InvoiceReviewRequest.


# Interface Name

`InvoiceReviewRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `acknowledgementToken` | [`InvoiceReviewRequestAcknowledgementToken \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/invoice-review-request-acknowledgement-token.md) | Optional | This is a container for any-of cases. |
| `amount` | `string` | Required | Amount.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,9}(?:\.[0-9]{1,2})?$` |
| `confirmSandboxDraft` | `boolean` | Required | Confirm sandbox draft. |
| `currency` | [`CurrencyEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/currency.md) | Required | Currency. |
| `description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` |
| `descriptionDigest` | [`InvoiceReviewRequestDescriptionDigest \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/invoice-review-request-description-digest.md) | Optional | This is a container for any-of cases. |
| `evaluationId` | [`InvoiceReviewRequestEvaluationId \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/invoice-review-request-evaluation-id.md) | Optional | This is a container for any-of cases. |


# Example

```ts
import {
  CurrencyEnum,
  InvoiceReviewRequest,
} from 'tradeglot-local-consolelib';

const invoiceReviewRequest: InvoiceReviewRequest = {
  amount: 'amount8',
  confirmSandboxDraft: false,
  currency: CurrencyEnum.USD,
  description: 'description6',
  acknowledgementToken: 'String7',
  descriptionDigest: 'String5',
  evaluationId: 'String1',
};
```



