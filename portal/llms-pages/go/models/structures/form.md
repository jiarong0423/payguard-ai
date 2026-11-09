# Form

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkZvcm0

Form.


# Class Name

`Form`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Kind` | [`*models.Kind2Enum`](http://localhost:3000/llms-pages/go/models/enumerations/kind-2.md) | Optional | Kind. |
| `Options` | [`[]models.GuideOption`](http://localhost:3000/llms-pages/go/models/structures/guide-option.md) | Optional | Options. |
| `Placeholder` | [`*models.FormPlaceholder`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/form-placeholder.md) | Optional | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    form := models.Form{
        Kind:                 models.ToPointer(models.Kind2Enum_TEXT),
        Options:              []models.GuideOption{
            models.GuideOption{
                Label: "label2",
                Value: "value4",
            },
            models.GuideOption{
                Label: "label2",
                Value: "value4",
            },
            models.GuideOption{
                Label: "label2",
                Value: "value4",
            },
        },
        Placeholder:          models.ToPointer(models.FormPlaceholderContainer.FromString("String9")),
    }

}
```



