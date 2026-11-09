# Category Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkNhdGVnb3J5U2lnbmFs

CategorySignal.


# Class Name

`CategorySignal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Category` | [`models.CategorySignalCategory`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/category-signal-category.md) | Required | This is a container for any-of cases. |
| `Confidence` | [`models.CategorySignalConfidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/category-signal-confidence.md) | Required | This is a container for any-of cases. |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"channel3"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    categorySignal := models.CategorySignal{
        Category:             models.CategorySignalCategoryContainer.FromString("String1"),
        Confidence:           models.CategorySignalConfidenceContainer.FromConfidence(models.ConfidenceEnum_HIGH),
        Source:               "channel3",
    }

}
```



