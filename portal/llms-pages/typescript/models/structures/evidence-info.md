# Evidence Info

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5mbw

EvidenceInfo.


# Interface Name

`EvidenceInfo`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `trackingInfo` | [`TrackingInfo[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/tracking-info.md) | Required | Tracking info.<br><br>**Constraints**: *Maximum Items*: `10` |


# Example

```ts
import { CarrierNameEnum, EvidenceInfo } from 'tradeglot-local-consolelib';

const evidenceInfo: EvidenceInfo = {
  trackingInfo: [
    {
      carrierName: CarrierNameEnum.DHL,
      trackingNumber: 'tracking_number6',
      carrierNameOther: 'String1',
    }
  ],
};
```



