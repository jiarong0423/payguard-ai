# Tracker Item

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlRyYWNrZXJJdGVt

TrackerItem.


# Interface Name

`TrackerItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `carrier` | [`CarrierEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/carrier.md) | Required | Carrier. |
| `carrierNameOther` | [`TrackerItemCarrierNameOther \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/tracker-item-carrier-name-other.md) | Optional | This is a container for any-of cases. |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'SHIPPED'` |
| `trackingNumber` | `string` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` |
| `transactionId` | `string` | Required | Transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9*._-]{1,64}$` |


# Example

```ts
import { CarrierEnum, TrackerItem } from 'tradeglot-local-consolelib';

const trackerItem: TrackerItem = {
  carrier: CarrierEnum.TWCHUNGHWAPOST,
  status: 'SHIPPED',
  trackingNumber: 'tracking_number6',
  transactionId: 'transaction_id6',
  carrierNameOther: 'String1',
};
```



