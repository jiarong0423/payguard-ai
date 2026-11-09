# Signal

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlNpZ25hbA

Signal.


# Class Name

`Signal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Category` | [`*models.SignalCategory`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/signal-category.md) | Optional | This is a container for any-of cases. |
| `Confidence` | [`*models.SignalConfidence`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/signal-confidence.md) | Optional | This is a container for any-of cases. |
| `Source` | [`*models.Source2Enum`](http://localhost:3000/llms-pages/go/models/enumerations/source-2.md) | Optional | Source. |


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



