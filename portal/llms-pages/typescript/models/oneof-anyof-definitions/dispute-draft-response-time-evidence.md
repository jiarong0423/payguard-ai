# Dispute Draft Response Time Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNlVGltZUV2aWRlbmNl


# Class Name

`DisputeDraftResponseTimeEvidence`


# Cases

| Type |
|  --- |
| [`TimeEvidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/time-evidence.md) |


# TimeEvidence

## Initialization Code

### Example

```ts
const value: DisputeDraftResponseTimeEvidence = {
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
    }
  ],
  flags: [
    FlagEnum.ORDERRECORDABSENT,
    FlagEnum.DELIVERYNOTRECORDED,
    FlagEnum.DELIVERYAFTERCLAIM
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



