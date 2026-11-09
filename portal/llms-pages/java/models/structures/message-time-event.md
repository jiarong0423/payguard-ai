# Message Time Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRk1lc3NhZ2VUaW1lRXZlbnQ

MessageTimeEvent.


# Class Name

`MessageTimeEvent`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `At` | `String` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` | String getAt() | setAt(String at) |
| `Channel` | [`ChannelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/channel.md) | Required | Channel. | ChannelEnum getChannel() | setChannel(ChannelEnum channel) |
| `Direction` | [`DirectionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/direction.md) | Required | Direction. | DirectionEnum getDirection() | setDirection(DirectionEnum direction) |
| `Kind` | `String` | Required, Constant | Kind.<br><br>**Value**: `"MESSAGE"` | String getKind() | setKind(String kind) |
| `MessageDigest` | `String` | Required | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` | String getMessageDigest() | setMessageDigest(String messageDigest) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"SELLER_PROVIDED_UNVERIFIED"` | String getSource() | setSource(String source) |
| `Topic` | [`TopicEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/topic.md) | Required | Topic. | TopicEnum getTopic() | setTopic(TopicEnum topic) |


# Example

```java
import m18000.m0.m0.m127.models.ChannelEnum;
import m18000.m0.m0.m127.models.DirectionEnum;
import m18000.m0.m0.m127.models.MessageTimeEvent;
import m18000.m0.m0.m127.models.TopicEnum;

MessageTimeEvent messageTimeEvent = new MessageTimeEvent.Builder(
    "at6",
    ChannelEnum.EMAIL,
    DirectionEnum.INBOUND,
    "MESSAGE",
    "message_digest4",
    "SELLER_PROVIDED_UNVERIFIED",
    TopicEnum.PAYMENT_NOTICE
)
.build();
```



