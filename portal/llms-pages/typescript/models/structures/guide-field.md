# Guide Field

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkd1aWRlRmllbGQ

GuideField.


# Interface Name

`GuideField`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `item` | `string` | Required | Item.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z_]+$` |
| `value` | `string` | Required | Value.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `120` |


# Example

```ts
import { GuideField } from 'tradeglot-local-consolelib';

const guideField: GuideField = {
  item: 'item8',
  value: 'value8',
};
```



