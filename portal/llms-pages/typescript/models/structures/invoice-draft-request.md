# Invoice Draft Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkludm9pY2VEcmFmdFJlcXVlc3Q

InvoiceDraftRequest.


# Interface Name

`InvoiceDraftRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `amount` | `string` | Required | Amount.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,9}(?:\.[0-9]{1,2})?$` |
| `currency` | [`CurrencyEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/currency.md) | Required | Currency. |
| `description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` |
| `payloadDigest` | `string` | Required | Payload digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `reviewToken` | `string` | Required | Review token.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128` |


# Example

```ts
import {
  CurrencyEnum,
  InvoiceDraftRequest,
} from 'tradeglot-local-consolelib';

const invoiceDraftRequest: InvoiceDraftRequest = {
  amount: 'amount6',
  currency: CurrencyEnum.JPY,
  description: 'description4',
  payloadDigest: 'payload_digest6',
  reviewToken: 'review_token2',
};
```



