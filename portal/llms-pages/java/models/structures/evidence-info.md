# Evidence Info

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5mbw

EvidenceInfo.


# Class Name

`EvidenceInfo`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `TrackingInfo` | [`List<TrackingInfo>`](http://localhost:3000/llms-pages/java/models/structures/tracking-info.md) | Required | Tracking info.<br><br>**Constraints**: *Maximum Items*: `10` | List<TrackingInfo> getTrackingInfo() | setTrackingInfo(List<TrackingInfo> trackingInfo) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.CarrierNameEnum;
import m18000.m0.m0.m127.models.EvidenceInfo;
import m18000.m0.m0.m127.models.TrackingInfo;
import m18000.m0.m0.m127.models.containers.TrackingInfoCarrierNameOther;

EvidenceInfo evidenceInfo = new EvidenceInfo.Builder(
    Arrays.asList(
        new TrackingInfo.Builder(
            CarrierNameEnum.DHL,
            "tracking_number6"
        )
        .carrierNameOther(TrackingInfoCarrierNameOther.fromString(
                "String1"
            ))
        .build()
    )
)
.build();
```



