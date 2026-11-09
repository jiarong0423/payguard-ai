# Message Time Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRk1lc3NhZ2VUaW1lRXZlbnQ

MessageTimeEvent.


# Interface Name

`MessageTimeEvent`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `string` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `channel` | [`ChannelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/channel.md) | Required | Channel. |
| `direction` | [`DirectionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/direction.md) | Required | Direction. |
| `kind` | `string` | Required, Constant | Kind.<br><br>**Value**: `'MESSAGE'` |
| `messageDigest` | `string` | Required | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'SELLER_PROVIDED_UNVERIFIED'` |
| `topic` | [`TopicEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/topic.md) | Required | Topic. |


# Example

```ts
import {
  ChannelEnum,
  DirectionEnum,
  MessageTimeEvent,
  TopicEnum,
} from 'tradeglot-local-consolelib';

const messageTimeEvent: MessageTimeEvent = {
  at: 'at6',
  channel: ChannelEnum.EMAIL,
  direction: DirectionEnum.INBOUND,
  kind: 'MESSAGE',
  messageDigest: 'message_digest4',
  source: 'SELLER_PROVIDED_UNVERIFIED',
  topic: TopicEnum.PAYMENTNOTICE,
};
```



