# Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkZvcm0

Form.


# Class Name

`Form`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Kind` | [`*models.Kind2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/kind-2.md) | Optional | Kind. |
| `Options` | [`[]models.GuideOption`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/guide-option.md) | Optional | Options. |
| `Placeholder` | [`*models.FormPlaceholder`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/form-placeholder.md) | Optional | This is a container for any-of cases. |


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



