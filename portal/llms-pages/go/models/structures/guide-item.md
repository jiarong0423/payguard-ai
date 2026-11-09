# Guide Item

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlSXRlbQ

GuideItem.


# Class Name

`GuideItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Chunk` | [`models.GuideItemChunk`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-item-chunk.md) | Required | This is a container for any-of cases. |
| `Form` | [`models.GuideItemForm`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-item-form.md) | Required | This is a container for any-of cases. |
| `Id` | `string` | Required | Id. |
| `Label` | `string` | Required | Label. |
| `Source` | [`models.Source8Enum`](http://localhost:3000/llms-pages/go/models/enumerations/source-8.md) | Required | Source. |
| `Status` | [`models.Status9Enum`](http://localhost:3000/llms-pages/go/models/enumerations/status-9.md) | Required | Status. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideItem := models.GuideItem{
        Chunk:  models.GuideItemChunkContainer.FromString("String7"),
        Form:   models.GuideItemFormContainer.FromGuideForm(models.GuideForm{
            Kind:        models.Kind2Enum_CHOICE,
            Options:     []models.GuideOption{
                models.GuideOption{
                    Label: "label2",
                    Value: "value4",
                },
            },
            Placeholder: models.GuideFormPlaceholderContainer.FromString("String9"),
        }),
        Id:     "id0",
        Label:  "label0",
        Source: models.Source8Enum_OFFICIAL,
        Status: models.Status9Enum_UNCLEAR,
    }

}
```



