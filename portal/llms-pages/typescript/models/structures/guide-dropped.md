# Guide Dropped

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkd1aWRlRHJvcHBlZA

GuideDropped.


# Interface Name

`GuideDropped`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `item` | `string` | Required | Item. |
| `reason` | [`Reason6Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/reason-6.md) | Required | Reason. |


# Example

```ts
import { GuideDropped, Reason6Enum } from 'tradeglot-local-consolelib';

const guideDropped: GuideDropped = {
  item: 'item6',
  reason: Reason6Enum.OtherParty,
};
```



