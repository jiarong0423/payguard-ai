# Time Evidence

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZQ

TimeEvidence.


# Class Name

`TimeEvidence`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AdvisoryOnly` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` | String getAdvisoryOnly() | setAdvisoryOnly(String advisoryOnly) |
| `Events` | [`List<TimeEvidenceEvents>`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/time-evidence-events.md) | Required | This is List of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` | List<TimeEvidenceEvents> getEvents() | setEvents(List<TimeEvidenceEvents> events) |
| `Flags` | [`List<FlagEnum>`](http://localhost:3000/llms-pages/java/models/enumerations/flag.md) | Required | Flags.<br><br>**Constraints**: *Maximum Items*: `4` | List<FlagEnum> getFlags() | setFlags(List<FlagEnum> flags) |
| `GapsSeconds` | [`TimeGaps`](http://localhost:3000/llms-pages/java/models/structures/time-gaps.md) | Required | TimeGaps. | TimeGaps getGapsSeconds() | setGapsSeconds(TimeGaps gapsSeconds) |
| `Judgement` | `String` | Required, Constant | Judgement.<br><br>**Value**: `"NOT_MADE"` | String getJudgement() | setJudgement(String judgement) |
| `SchemaVersion` | `String` | Required, Constant | Schema version.<br><br>**Value**: `"payguard.time_evidence.v1"` | String getSchemaVersion() | setSchemaVersion(String schemaVersion) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.ChannelEnum;
import m18000.m0.m0.m127.models.DirectionEnum;
import m18000.m0.m0.m127.models.FlagEnum;
import m18000.m0.m0.m127.models.MessageTimeEvent;
import m18000.m0.m0.m127.models.TimeEvidence;
import m18000.m0.m0.m127.models.TimeGaps;
import m18000.m0.m0.m127.models.TopicEnum;
import m18000.m0.m0.m127.models.containers.TimeEvidenceEvents;
import m18000.m0.m0.m127.models.containers.TimeGapsDeliveryToClaim;
import m18000.m0.m0.m127.models.containers.TimeGapsPaymentToClaim;
import m18000.m0.m0.m127.models.containers.TimeGapsPaymentToDelivery;
import m18000.m0.m0.m127.models.containers.TimeGapsPaymentToOrderRecord;

TimeEvidence timeEvidence = new TimeEvidence.Builder(
    "True",
    Arrays.asList(
        TimeEvidenceEvents.fromMessageTimeEvent(
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
        TimeEvidenceEvents.fromMessageTimeEvent(
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
        TimeEvidenceEvents.fromMessageTimeEvent(
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
    ),
    Arrays.asList(
        FlagEnum.DELIVERY_AFTER_CLAIM,
        FlagEnum.CLAIM_TIME_EARLIER_THAN_PAYMENT_TIME
    ),
    new TimeGaps.Builder(
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
    .build(),
    "NOT_MADE",
    "payguard.time_evidence.v1"
)
.build();
```



