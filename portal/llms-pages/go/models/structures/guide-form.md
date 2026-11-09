# Guide Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkd1aWRlRm9ybQ

GuideForm.


# Class Name

`GuideForm`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Kind` | [`models.Kind2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/kind-2.md) | Required | Kind. |
| `Options` | [`[]models.GuideOption`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/guide-option.md) | Required | Options. |
| `Placeholder` | [`models.GuideFormPlaceholder`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/guide-form-placeholder.md) | Required | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideForm := models.GuideForm{
        Kind:        models.Kind2Enum_CHOICE,
        Options:     []models.GuideOption{
            models.GuideOption{
                Label: "label2",
                Value: "value4",
            },
        },
        Placeholder: models.GuideFormPlaceholderContainer.FromString("String3"),
    }

}
```



