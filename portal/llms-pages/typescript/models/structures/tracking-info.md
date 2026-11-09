# Tracking Info

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlRyYWNraW5nSW5mbw

TrackingInfo.


# Interface Name

`TrackingInfo`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `carrierName` | [`CarrierNameEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/carrier-name.md) | Required | Carrier name. |
| `carrierNameOther` | [`TrackingInfoCarrierNameOther \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/tracking-info-carrier-name-other.md) | Optional | This is a container for any-of cases. |
| `trackingNumber` | `string` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` |


# Example

```ts
import { CarrierNameEnum, TrackingInfo } from 'tradeglot-local-consolelib';

const trackingInfo: TrackingInfo = {
  carrierName: CarrierNameEnum.TWCHUNGHWAPOST,
  trackingNumber: 'tracking_number4',
  carrierNameOther: 'String9',
};
```



