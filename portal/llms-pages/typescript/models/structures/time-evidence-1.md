# Time Evidence 1

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZTE

Time evidence.


# Interface Name

`TimeEvidence1`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisoryOnly` | `boolean \| undefined` | Optional | Advisory only. |
| `events` | [`TimeEvidence1Events[] \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/time-evidence-1-events.md) | Optional | This is Array of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` |
| `flags` | [`FlagEnum[] \| undefined`](http://localhost:3000/llms-pages/typescript/models/enumerations/flag.md) | Optional | Flags.<br><br>**Constraints**: *Maximum Items*: `4` |
| `gapsSeconds` | [`TimeGaps \| undefined`](http://localhost:3000/llms-pages/typescript/models/structures/time-gaps.md) | Optional | TimeGaps. |
| `judgement` | [`JudgementEnum \| undefined`](http://localhost:3000/llms-pages/typescript/models/enumerations/judgement.md) | Optional | Judgement. |
| `schemaVersion` | [`SchemaVersionEnum \| undefined`](http://localhost:3000/llms-pages/typescript/models/enumerations/schema-version.md) | Optional | Schema version. |


# Example

```ts
import {
  ChannelEnum,
  DirectionEnum,
  FlagEnum,
  JudgementEnum,
  TimeEvidence1,
  TopicEnum,
} from 'tradeglot-local-consolelib';

const timeEvidence1: TimeEvidence1 = {
  advisoryOnly: false,
  events: [
    {
      at: 'at4',
      channel: ChannelEnum.EMAIL,
      direction: DirectionEnum.INBOUND,
      kind: 'kind6',
      messageDigest: 'message_digest2',
      source: 'source4',
      topic: TopicEnum.ORDERDETAILSPROVIDED,
    },
    {
      at: 'at4',
      channel: ChannelEnum.EMAIL,
      direction: DirectionEnum.INBOUND,
      kind: 'kind6',
      messageDigest: 'message_digest2',
      source: 'source4',
      topic: TopicEnum.ORDERDETAILSPROVIDED,
    }
  ],
  flags: [
    FlagEnum.ORDERRECORDABSENT,
    FlagEnum.DELIVERYNOTRECORDED
  ],
  gapsSeconds: {
    deliveryToClaim: 210,
    paymentToClaim: 154,
    paymentToDelivery: 192,
    paymentToOrderRecord: 208,
  },
  judgement: JudgementEnum.NOTMADE,
};
```



