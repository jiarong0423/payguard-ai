# Message Time Event

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRk1lc3NhZ2VUaW1lRXZlbnQ

MessageTimeEvent.


# Class Name

`MessageTimeEvent`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `At` | `string` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `Channel` | [`ChannelEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/channel.md) | Required | Channel. |
| `Direction` | [`DirectionEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/direction.md) | Required | Direction. |
| `Kind` | `string` | Required, Constant | Kind.<br><br>**Value**: `"MESSAGE"` |
| `MessageDigest` | `string` | Required | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"SELLER_PROVIDED_UNVERIFIED"` |
| `Topic` | [`TopicEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/topic.md) | Required | Topic. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

MessageTimeEvent messageTimeEvent = new MessageTimeEvent
{
    At = "at6",
    Channel = ChannelEnum.EMAIL,
    Direction = DirectionEnum.INBOUND,
    Kind = "MESSAGE",
    MessageDigest = "message_digest4",
    Source = "SELLER_PROVIDED_UNVERIFIED",
    Topic = TopicEnum.PAYMENTNOTICE,
};
```



