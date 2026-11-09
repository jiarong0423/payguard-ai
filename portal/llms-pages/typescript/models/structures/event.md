# Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkV2ZW50


# Interface Name

`Event`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `string \| undefined` | Optional | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `channel` | [`ChannelEnum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/channel.md) | Optional | Channel. |
| `direction` | [`DirectionEnum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/direction.md) | Optional | Direction. |
| `kind` | [`Kind1Enum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/kind-1.md) | Optional | Kind. |
| `messageDigest` | `string \| undefined` | Optional | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` |
| `source` | [`Source6Enum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/source-6.md) | Optional | Source. |
| `topic` | [`TopicEnum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/topic.md) | Optional | Topic. |


# Example

```ts
import {
  ChannelEnum,
  DirectionEnum,
  Event,
  Kind1Enum,
} from 'tradeglot-local-consolelib';

const event: Event = {
  at: 'at6',
  channel: ChannelEnum.EMAIL,
  direction: DirectionEnum.INBOUND,
  kind: Kind1Enum.MESSAGE,
  messageDigest: 'message_digest6',
};
```



