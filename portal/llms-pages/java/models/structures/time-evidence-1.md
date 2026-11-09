# Time Evidence 1

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZTE

Time evidence.


# Class Name

`TimeEvidence1`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AdvisoryOnly` | `Boolean` | Optional | Advisory only. | Boolean getAdvisoryOnly() | setAdvisoryOnly(Boolean advisoryOnly) |
| `Events` | [`List<TimeEvidence1Events>`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/time-evidence-1-events.md) | Optional | This is List of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` | List<TimeEvidence1Events> getEvents() | setEvents(List<TimeEvidence1Events> events) |
| `Flags` | [`List<FlagEnum>`](http://localhost:3000/llms-pages/java/models/enumerations/flag.md) | Optional | Flags.<br><br>**Constraints**: *Maximum Items*: `4` | List<FlagEnum> getFlags() | setFlags(List<FlagEnum> flags) |
| `GapsSeconds` | [`TimeGaps`](http://localhost:3000/llms-pages/java/models/structures/time-gaps.md) | Optional | TimeGaps. | TimeGaps getGapsSeconds() | setGapsSeconds(TimeGaps gapsSeconds) |
| `Judgement` | [`JudgementEnum`](http://localhost:3000/llms-pages/java/models/enumerations/judgement.md) | Optional | Judgement. | JudgementEnum getJudgement() | setJudgement(JudgementEnum judgement) |
| `SchemaVersion` | [`SchemaVersionEnum`](http://localhost:3000/llms-pages/java/models/enumerations/schema-version.md) | Optional | Schema version. | SchemaVersionEnum getSchemaVersion() | setSchemaVersion(SchemaVersionEnum schemaVersion) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.ChannelEnum;
import m18000.m0.m0.m127.models.DirectionEnum;
import m18000.m0.m0.m127.models.FlagEnum;
import m18000.m0.m0.m127.models.JudgementEnum;
import m18000.m0.m0.m127.models.MessageTimeEvent;
import m18000.m0.m0.m127.models.TimeEvidence1;
import m18000.m0.m0.m127.models.TimeGaps;
import m18000.m0.m0.m127.models.TopicEnum;
import m18000.m0.m0.m127.models.containers.TimeEvidence1Events;
import m18000.m0.m0.m127.models.containers.TimeGapsDeliveryToClaim;
import m18000.m0.m0.m127.models.containers.TimeGapsPaymentToClaim;
import m18000.m0.m0.m127.models.containers.TimeGapsPaymentToDelivery;
import m18000.m0.m0.m127.models.containers.TimeGapsPaymentToOrderRecord;

TimeEvidence1 timeEvidence1 = new TimeEvidence1.Builder()
    .advisoryOnly(false)
    .events(Arrays.asList(
        TimeEvidence1Events.fromMessageTimeEvent(
            new MessageTimeEvent.Builder(
                "at4",
                ChannelEnum.EMAIL,
                DirectionEnum.INBOUND,
                "kind6",
                "message_digest2",
                "source4",
                TopicEnum.ORDER_DETAILS_PROVIDED
            )
            .build()
        ),
        TimeEvidence1Events.fromMessageTimeEvent(
            new MessageTimeEvent.Builder(
                "at4",
                ChannelEnum.EMAIL,
                DirectionEnum.INBOUND,
                "kind6",
                "message_digest2",
                "source4",
                TopicEnum.ORDER_DETAILS_PROVIDED
            )
            .build()
        )
    ))
    .flags(Arrays.asList(
        FlagEnum.ORDER_RECORD_ABSENT,
        FlagEnum.DELIVERY_NOT_RECORDED
    ))
    .gapsSeconds(new TimeGaps.Builder(
        TimeGapsDeliveryToClaim.fromNumber(
            210
        ),
        TimeGapsPaymentToClaim.fromNumber(
            154
        ),
        TimeGapsPaymentToDelivery.fromNumber(
            192
        ),
        TimeGapsPaymentToOrderRecord.fromNumber(
            208
        )
    )
    .build())
    .judgement(JudgementEnum.NOT_MADE)
    .build();
```



