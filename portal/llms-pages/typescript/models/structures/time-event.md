# Time Event

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlRpbWVFdmVudA

TimeEvent.


# Interface Name

`TimeEvent`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `string` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `kind` | [`KindEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/kind.md) | Required | Kind. |
| `source` | [`Source5Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/source-5.md) | Required | Source. |


# Example

```ts
import { KindEnum, Source5Enum, TimeEvent } from 'tradeglot-local-consolelib';

const timeEvent: TimeEvent = {
  at: 'at6',
  kind: KindEnum.DELIVERY,
  source: Source5Enum.PROVIDER,
};
```



