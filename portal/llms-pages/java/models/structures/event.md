# Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkV2ZW50


# Class Name

`Event`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `At` | `String` | Optional | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` | String getAt() | setAt(String at) |
| `Channel` | [`ChannelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/channel.md) | Optional | Channel. | ChannelEnum getChannel() | setChannel(ChannelEnum channel) |
| `Direction` | [`DirectionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/direction.md) | Optional | Direction. | DirectionEnum getDirection() | setDirection(DirectionEnum direction) |
| `Kind` | [`Kind1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/kind-1.md) | Optional | Kind. | Kind1Enum getKind() | setKind(Kind1Enum kind) |
| `MessageDigest` | `String` | Optional | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` | String getMessageDigest() | setMessageDigest(String messageDigest) |
| `Source` | [`Source6Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/source-6.md) | Optional | Source. | Source6Enum getSource() | setSource(Source6Enum source) |
| `Topic` | [`TopicEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/topic.md) | Optional | Topic. | TopicEnum getTopic() | setTopic(TopicEnum topic) |


# Example

```java
import m18000.m0.m0.m127.models.ChannelEnum;
import m18000.m0.m0.m127.models.DirectionEnum;
import m18000.m0.m0.m127.models.Event;
import m18000.m0.m0.m127.models.Kind1Enum;

Event event = new Event.Builder()
    .at("at6")
    .channel(ChannelEnum.EMAIL)
    .direction(DirectionEnum.INBOUND)
    .kind(Kind1Enum.MESSAGE)
    .messageDigest("message_digest6")
    .build();
```



