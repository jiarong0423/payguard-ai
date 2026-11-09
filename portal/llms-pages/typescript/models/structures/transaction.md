# Transaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlRyYW5zYWN0aW9u

Transaction.


# Interface Name

`Transaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `amount` | `string` | Required | Amount. |
| `currency` | `string` | Required | Currency. |
| `occurredAt` | `string` | Required | Occurred at. |
| `orderId` | `string` | Required | Order id. |


# Example

```ts
import { Transaction } from 'tradeglot-local-consolelib';

const transaction: Transaction = {
  amount: 'amount0',
  currency: 'currency8',
  occurredAt: 'occurred_at2',
  orderId: 'order_id2',
};
```



