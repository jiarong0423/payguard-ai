# Tracker Batch

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlRyYWNrZXJCYXRjaA

TrackerBatch.


# Interface Name

`TrackerBatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `trackers` | [`TrackerItem[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/tracker-item.md) | Required | Trackers.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `1` |


# Example

```ts
import { CarrierEnum, TrackerBatch } from 'tradeglot-local-consolelib';

const trackerBatch: TrackerBatch = {
  trackers: [
    {
      carrier: CarrierEnum.JPJAPANPOST,
      status: 'SHIPPED',
      trackingNumber: 'tracking_number0',
      transactionId: 'transaction_id0',
      carrierNameOther: 'String5',
    }
  ],
};
```



