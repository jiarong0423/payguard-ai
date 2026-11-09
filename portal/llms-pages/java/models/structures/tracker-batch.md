# Tracker Batch

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlRyYWNrZXJCYXRjaA

TrackerBatch.


# Class Name

`TrackerBatch`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Trackers` | [`List<TrackerItem>`](http://localhost:3000/llms-pages/java/models/structures/tracker-item.md) | Required | Trackers.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `1` | List<TrackerItem> getTrackers() | setTrackers(List<TrackerItem> trackers) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.CarrierEnum;
import m18000.m0.m0.m127.models.TrackerBatch;
import m18000.m0.m0.m127.models.TrackerItem;
import m18000.m0.m0.m127.models.containers.TrackerItemCarrierNameOther;

TrackerBatch trackerBatch = new TrackerBatch.Builder(
    Arrays.asList(
        new TrackerItem.Builder(
            CarrierEnum.JP_JAPANPOST,
            "SHIPPED",
            "tracking_number0",
            "transaction_id0"
        )
        .carrierNameOther(TrackerItemCarrierNameOther.fromString(
                "String5"
            ))
        .build()
    )
)
.build();
```



