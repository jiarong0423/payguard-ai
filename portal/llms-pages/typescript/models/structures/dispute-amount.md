# Dispute Amount

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkRpc3B1dGVBbW91bnQ

Dispute amount.


# Interface Name

`DisputeAmount`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `currencyCode` | `string \| undefined` | Optional | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `value` | `string \| undefined` | Optional | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```ts
import { DisputeAmount } from 'tradeglot-local-consolelib';

const disputeAmount: DisputeAmount = {
  currencyCode: 'currency_code0',
  value: 'value6',
};
```



