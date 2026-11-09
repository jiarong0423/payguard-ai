# Message Time Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRk1lc3NhZ2VUaW1lRXZlbnQ

MessageTimeEvent.


# Class Name

`MessageTimeEvent`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `At` | `string` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `Channel` | [`models.ChannelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/channel.md) | Required | Channel. |
| `Direction` | [`models.DirectionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/direction.md) | Required | Direction. |
| `Kind` | `string` | Required, Constant | Kind.<br><br>**Value**: `"MESSAGE"` |
| `MessageDigest` | `string` | Required | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"SELLER_PROVIDED_UNVERIFIED"` |
| `Topic` | [`models.TopicEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/topic.md) | Required | Topic. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    messageTimeEvent := models.MessageTimeEvent{
        At:                   "at6",
        Channel:              models.ChannelEnum_EMAIL,
        Direction:            models.DirectionEnum_INBOUND,
        Kind:                 "MESSAGE",
        MessageDigest:        "message_digest4",
        Source:               "SELLER_PROVIDED_UNVERIFIED",
        Topic:                models.TopicEnum_PAYMENTNOTICE,
    }

}
```



