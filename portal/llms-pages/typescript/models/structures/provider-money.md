# Provider Money

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlByb3ZpZGVyTW9uZXk

ProviderMoney.


# Interface Name

`ProviderMoney`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `currencyCode` | `string` | Required | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `value` | `string` | Required | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```ts
import { ProviderMoney } from 'tradeglot-local-consolelib';

const providerMoney: ProviderMoney = {
  currencyCode: 'currency_code4',
  value: 'value0',
};
```



