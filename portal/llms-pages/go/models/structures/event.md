# Event

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkV2ZW50


# Class Name

`Event`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `At` | `*string` | Optional | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `Channel` | [`*models.ChannelEnum`](http://localhost:3000/llms-pages/go/models/enumerations/channel.md) | Optional | Channel. |
| `Direction` | [`*models.DirectionEnum`](http://localhost:3000/llms-pages/go/models/enumerations/direction.md) | Optional | Direction. |
| `Kind` | [`*models.Kind1Enum`](http://localhost:3000/llms-pages/go/models/enumerations/kind-1.md) | Optional | Kind. |
| `MessageDigest` | `*string` | Optional | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` |
| `Source` | [`*models.Source6Enum`](http://localhost:3000/llms-pages/go/models/enumerations/source-6.md) | Optional | Source. |
| `Topic` | [`*models.TopicEnum`](http://localhost:3000/llms-pages/go/models/enumerations/topic.md) | Optional | Topic. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    event := models.Event{
        At:                   models.ToPointer("at6"),
        Channel:              models.ToPointer(models.ChannelEnum_EMAIL),
        Direction:            models.ToPointer(models.DirectionEnum_INBOUND),
        Kind:                 models.ToPointer(models.Kind1Enum_MESSAGE),
        MessageDigest:        models.ToPointer("message_digest6"),
    }

}
```



