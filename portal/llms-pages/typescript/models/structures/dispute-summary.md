# Dispute Summary

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkRpc3B1dGVTdW1tYXJ5

DisputeSummary.


# Interface Name

`DisputeSummary`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseRef` | `string` | Required | Case ref. |
| `disputeAmount` | [`SyntheticMoney`](http://localhost:3000/llms-pages/typescript/models/structures/synthetic-money.md) | Required | Same shape as the PayPal Disputes `dispute_amount` (ProviderMoney below); values are synthetic. |
| `openedAt` | `string` | Required | Opened at. |
| `orderRef` | `string` | Required | Order ref. |
| `reason` | `string` | Required | Reason. |
| `sellerResponseDueDate` | `string` | Required | Seller response due date. |
| `status` | [`Status7Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/status-7.md) | Required | Status. |


# Example

```ts
import { DisputeSummary, Status7Enum } from 'tradeglot-local-consolelib';

const disputeSummary: DisputeSummary = {
  caseRef: 'case_ref6',
  disputeAmount: {
    currencyCode: 'currency_code6',
    value: 'value0',
  },
  openedAt: 'opened_at0',
  orderRef: 'order_ref8',
  reason: 'reason8',
  sellerResponseDueDate: 'seller_response_due_date0',
  status: Status7Enum.NeedsReview,
};
```



