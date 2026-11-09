# Evidence Info

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5mbw

EvidenceInfo.


# Interface Name

`EvidenceInfo`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `trackingInfo` | [`TrackingInfo[]`](http://localhost:3000/llms-pages/typescript/models/structures/tracking-info.md) | Required | Tracking info.<br><br>**Constraints**: *Maximum Items*: `10` |


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



