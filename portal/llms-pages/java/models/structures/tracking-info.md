# Tracking Info

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlRyYWNraW5nSW5mbw

TrackingInfo.


# Class Name

`TrackingInfo`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CarrierName` | [`CarrierNameEnum`](http://localhost:3000/llms-pages/java/models/enumerations/carrier-name.md) | Required | Carrier name. | CarrierNameEnum getCarrierName() | setCarrierName(CarrierNameEnum carrierName) |
| `CarrierNameOther` | [`TrackingInfoCarrierNameOther`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/tracking-info-carrier-name-other.md) | Optional | This is a container for any-of cases. | TrackingInfoCarrierNameOther getCarrierNameOther() | setCarrierNameOther(TrackingInfoCarrierNameOther carrierNameOther) |
| `TrackingNumber` | `String` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` | String getTrackingNumber() | setTrackingNumber(String trackingNumber) |


# Example

```java
import m18000.m0.m0.m127.models.CarrierNameEnum;
import m18000.m0.m0.m127.models.TrackingInfo;
import m18000.m0.m0.m127.models.containers.TrackingInfoCarrierNameOther;

TrackingInfo trackingInfo = new TrackingInfo.Builder(
    CarrierNameEnum.TW_CHUNGHWA_POST,
    "tracking_number4"
)
.carrierNameOther(TrackingInfoCarrierNameOther.fromString(
        "String9"
    ))
.build();
```



