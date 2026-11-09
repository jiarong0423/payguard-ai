# Time Evidence

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZQ

TimeEvidence.


# Interface Name

`TimeEvidence`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `events` | [`TimeEvidenceEvents[]`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/time-evidence-events.md) | Required | This is Array of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` |
| `flags` | [`FlagEnum[]`](http://localhost:3000/llms-pages/typescript/models/enumerations/flag.md) | Required | Flags.<br><br>**Constraints**: *Maximum Items*: `4` |
| `gapsSeconds` | [`TimeGaps`](http://localhost:3000/llms-pages/typescript/models/structures/time-gaps.md) | Required | TimeGaps. |
| `judgement` | `string` | Required, Constant | Judgement.<br><br>**Value**: `'NOT_MADE'` |
| `schemaVersion` | `string` | Required, Constant | Schema version.<br><br>**Value**: `'payguard.time_evidence.v1'` |


# Example

```ts
import {
  ChannelEnum,
  DirectionEnum,
  FlagEnum,
  TimeEvidence,
  TopicEnum,
} from 'tradeglot-local-consolelib';

const timeEvidence: TimeEvidence = {
  advisoryOnly: 'True',
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
    FlagEnum.DELIVERYAFTERCLAIM,
    FlagEnum.CLAIMTIMEEARLIERTHANPAYMENTTIME
  ],
  gapsSeconds: {
    deliveryToClaim: 210,
    paymentToClaim: 154,
    paymentToDelivery: 192,
    paymentToOrderRecord: 208,
  },
  judgement: 'NOT_MADE',
  schemaVersion: 'payguard.time_evidence.v1',
};
```



