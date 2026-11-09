# Time Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlRpbWVFdmVudA

TimeEvent.


# Interface Name

`TimeEvent`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `string` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `kind` | [`KindEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/kind.md) | Required | Kind. |
| `source` | [`Source5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/source-5.md) | Required | Source. |


# Example

```ts
import { KindEnum, Source5Enum, TimeEvent } from 'tradeglot-local-consolelib';

const timeEvent: TimeEvent = {
  at: 'at6',
  kind: KindEnum.DELIVERY,
  source: Source5Enum.PROVIDER,
};
```



