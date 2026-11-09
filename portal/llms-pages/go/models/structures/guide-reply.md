# Guide Reply

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlUmVwbHk

GuideReply.


# Class Name

`GuideReply`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Chooser` | [`models.ChooserEnum`](http://localhost:3000/llms-pages/go/models/enumerations/chooser.md) | Required | Chooser. |
| `Dropped` | [`[]models.GuideDropped`](http://localhost:3000/llms-pages/go/models/structures/guide-dropped.md) | Required | Dropped. |
| `FallbackReason` | [`models.GuideReplyFallbackReason`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-reply-fallback-reason.md) | Required | This is a container for any-of cases. |
| `StateChanged` | `bool` | Required | State changed. |
| `Template` | [`models.TemplateEnum`](http://localhost:3000/llms-pages/go/models/enumerations/template.md) | Required | Template. |
| `Text` | `string` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideReply := models.GuideReply{
        Chooser:        models.ChooserEnum_NONE,
        Dropped:        []models.GuideDropped{
            models.GuideDropped{
                Item:   "item2",
                Reason: models.Reason6Enum_OTHERPARTY,
            },
        },
        FallbackReason: models.GuideReplyFallbackReasonContainer.FromFallbackReason(models.FallbackReasonEnum_LATE),
        StateChanged:   false,
        Template:       models.TemplateEnum_NOGUARANTEE,
        Text:           "text6",
    }

}
```



