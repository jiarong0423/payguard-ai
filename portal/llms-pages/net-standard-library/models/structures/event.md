# Event

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkV2ZW50


# Class Name

`Event`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `At` | `string` | Optional | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `Channel` | [`ChannelEnum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/channel.md) | Optional | Channel. |
| `Direction` | [`DirectionEnum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/direction.md) | Optional | Direction. |
| `Kind` | [`Kind1Enum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/kind-1.md) | Optional | Kind. |
| `MessageDigest` | `string` | Optional | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` |
| `Source` | [`Source6Enum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/source-6.md) | Optional | Source. |
| `Topic` | [`TopicEnum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/topic.md) | Optional | Topic. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

Event mEvent = new Event
{
    At = "at0",
    Channel = ChannelEnum.EMAIL,
    Direction = DirectionEnum.INBOUND,
    Kind = Kind1Enum.MESSAGE,
    MessageDigest = "message_digest8",
};
```



