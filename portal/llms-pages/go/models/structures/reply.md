# Reply

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlJlcGx5

Reply.


# Class Name

`Reply`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Chooser` | [`*models.ChooserEnum`](http://localhost:3000/llms-pages/go/models/enumerations/chooser.md) | Optional | Chooser. |
| `Dropped` | [`[]models.GuideDropped`](http://localhost:3000/llms-pages/go/models/structures/guide-dropped.md) | Optional | Dropped. |
| `FallbackReason` | [`*models.ReplyFallbackReason`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/reply-fallback-reason.md) | Optional | This is a container for any-of cases. |
| `StateChanged` | `*bool` | Optional | State changed. |
| `Template` | [`*models.TemplateEnum`](http://localhost:3000/llms-pages/go/models/enumerations/template.md) | Optional | Template. |
| `Text` | `*string` | Optional | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    reply := models.Reply{
        Chooser:              models.ToPointer(models.ChooserEnum_KEYWORD),
        Dropped:              []models.GuideDropped{
            models.GuideDropped{
                Item:   "item2",
                Reason: models.Reason6Enum_OTHERPARTY,
            },
            models.GuideDropped{
                Item:   "item2",
                Reason: models.Reason6Enum_OTHERPARTY,
            },
        },
        FallbackReason:       models.ToPointer(models.ReplyFallbackReasonContainer.FromFallbackReason(models.FallbackReasonEnum_PROVIDERERROR)),
        StateChanged:         models.ToPointer(false),
        Template:             models.ToPointer(models.TemplateEnum_SUBTRACTION),
    }

}
```



