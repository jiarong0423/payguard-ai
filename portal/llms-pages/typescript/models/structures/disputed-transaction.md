# Disputed Transaction

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkRpc3B1dGVkVHJhbnNhY3Rpb24

DisputedTransaction.


# Interface Name

`DisputedTransaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `grossAmount` | [`DisputedTransactionGrossAmount \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/disputed-transaction-gross-amount.md) | Optional | This is a container for any-of cases. |
| `sellerProtectionEligible` | [`DisputedTransactionSellerProtectionEligible \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/disputed-transaction-seller-protection-eligible.md) | Optional | This is a container for any-of cases. |
| `sellerTransactionId` | `string` | Required | Seller transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9._-]{1,64}$` |
| `transactionStatus` | [`DisputedTransactionTransactionStatus \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/disputed-transaction-transaction-status.md) | Optional | This is a container for any-of cases. |


# Example

```ts
import { DisputedTransaction } from 'tradeglot-local-consolelib';

const disputedTransaction: DisputedTransaction = {
  sellerTransactionId: 'seller_transaction_id8',
  grossAmount: {
    currencyCode: 'currency_code0',
    value: 'value6',
  },
  sellerProtectionEligible: true,
  transactionStatus: 'String3',
};
```



