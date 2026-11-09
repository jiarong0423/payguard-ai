# Synthetic Money

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlN5bnRoZXRpY01vbmV5

Same shape as the PayPal Disputes `dispute_amount` (ProviderMoney below); values are synthetic.


# Interface Name

`SyntheticMoney`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `currencyCode` | `string` | Required | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `value` | `string` | Required | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```ts
import { SyntheticMoney } from 'tradeglot-local-consolelib';

const syntheticMoney: SyntheticMoney = {
  currencyCode: 'currency_code8',
  value: 'value4',
};
```



