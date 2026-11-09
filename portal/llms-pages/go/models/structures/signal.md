# Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlNpZ25hbA

Signal.


# Class Name

`Signal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Category` | [`*models.SignalCategory`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/signal-category.md) | Optional | This is a container for any-of cases. |
| `Confidence` | [`*models.SignalConfidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/signal-confidence.md) | Optional | This is a container for any-of cases. |
| `Source` | [`*models.Source2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/source-2.md) | Optional | Source. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    signal := models.Signal{
        Category:             models.ToPointer(models.SignalCategoryContainer.FromString("String1")),
        Confidence:           models.ToPointer(models.SignalConfidenceContainer.FromConfidence(models.ConfidenceEnum_HIGH)),
        Source:               models.ToPointer(models.Source2Enum_CHANNEL3),
    }

}
```



