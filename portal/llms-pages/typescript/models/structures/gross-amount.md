# Gross Amount

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkdyb3NzQW1vdW50

Gross amount.


# Interface Name

`GrossAmount`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `currencyCode` | `string \| undefined` | Optional | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `value` | `string \| undefined` | Optional | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```ts
import { GrossAmount } from 'tradeglot-local-consolelib';

const grossAmount: GrossAmount = {
  currencyCode: 'currency_code6',
  value: 'value2',
};
```



