# Time Evidence Events

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZUV2ZW50cw


# Class Name

`TimeEvidenceEvents`


# Cases

| Type |
|  --- |
| [`MessageTimeEvent`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/message-time-event.md) |
| [`TimeEvent`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/time-event.md) |


# MessageTimeEvent

## Initialization Code

### Example

```ts
const value: TimeEvidenceEvents = {
  at: 'at4',
  channel: ChannelEnum.EMAIL,
  direction: DirectionEnum.INBOUND,
  kind: 'MESSAGE',
  messageDigest: 'message_digest2',
  source: 'SELLER_PROVIDED_UNVERIFIED',
  topic: TopicEnum.ORDERDETAILSPROVIDED,
};
```


# TimeEvent

## Initialization Code

### Example

```ts
const value: TimeEvidenceEvents = {
  at: 'at2',
  kind: KindEnum.DELIVERY,
  source: Source5Enum.PROVIDER,
};
```



