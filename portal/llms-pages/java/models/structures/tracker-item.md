# Tracker Item

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlRyYWNrZXJJdGVt

TrackerItem.


# Class Name

`TrackerItem`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Carrier` | [`CarrierEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/carrier.md) | Required | Carrier. | CarrierEnum getCarrier() | setCarrier(CarrierEnum carrier) |
| `CarrierNameOther` | [`TrackerItemCarrierNameOther`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/tracker-item-carrier-name-other.md) | Optional | This is a container for any-of cases. | TrackerItemCarrierNameOther getCarrierNameOther() | setCarrierNameOther(TrackerItemCarrierNameOther carrierNameOther) |
| `Status` | `String` | Required, Constant | Status.<br><br>**Value**: `"SHIPPED"` | String getStatus() | setStatus(String status) |
| `TrackingNumber` | `String` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` | String getTrackingNumber() | setTrackingNumber(String trackingNumber) |
| `TransactionId` | `String` | Required | Transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9*._-]{1,64}$` | String getTransactionId() | setTransactionId(String transactionId) |


# Example

```java
import m18000.m0.m0.m127.models.CarrierEnum;
import m18000.m0.m0.m127.models.TrackerItem;
import m18000.m0.m0.m127.models.containers.TrackerItemCarrierNameOther;

TrackerItem trackerItem = new TrackerItem.Builder(
    CarrierEnum.TW_CHUNGHWA_POST,
    "SHIPPED",
    "tracking_number6",
    "transaction_id6"
)
.carrierNameOther(TrackerItemCarrierNameOther.fromString(
        "String1"
    ))
.build();
```



