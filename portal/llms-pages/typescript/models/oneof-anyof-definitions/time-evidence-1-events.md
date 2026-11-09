# Time Evidence 1 Events

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZTFFdmVudHM


# Class Name

`TimeEvidence1Events`


# Cases

| Type |
|  --- |
| [`MessageTimeEvent`](http://localhost:3000/llms-pages/typescript/models/structures/message-time-event.md) |
| [`TimeEvent`](http://localhost:3000/llms-pages/typescript/models/structures/time-event.md) |


# MessageTimeEvent

## Initialization Code

### Example

```ts
const value: TimeEvidence1Events = {
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
const value: TimeEvidence1Events = {
  at: 'at2',
  kind: KindEnum.DELIVERY,
  source: Source5Enum.PROVIDER,
};
```



