# Invoice Review Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkludm9pY2VSZXZpZXdSZXNwb25zZQ

InvoiceReviewResponse.


# Interface Name

`InvoiceReviewResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | `string` | Required, Constant | Action.<br><br>**Value**: `'create_sandbox_invoice_draft'` |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `authenticatedActor` | `string` | Required, Constant | Authenticated actor.<br><br>**Value**: `'False'` |
| `expiresAt` | `string` | Required | Expires at. |
| `limitations` | `string[]` | Required | Limitations. |
| `payloadDigest` | `string` | Required | Payload digest. |
| `policyStatus` | `string` | Required, Constant | Policy status.<br><br>**Value**: `'manual_review'` |
| `reviewToken` | `string` | Required | Review token. |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |


# Example

```ts
import { InvoiceReviewResponse } from 'tradeglot-local-consolelib';

const invoiceReviewResponse: InvoiceReviewResponse = {
  action: 'create_sandbox_invoice_draft',
  advisoryOnly: 'True',
  authenticatedActor: 'False',
  expiresAt: 'expires_at8',
  limitations: [
    'limitations5',
    'limitations6'
  ],
  payloadDigest: 'payload_digest8',
  policyStatus: 'manual_review',
  reviewToken: 'review_token6',
  source: 'synthetic',
};
```



