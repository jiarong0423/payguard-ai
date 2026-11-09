# Guide Review Row

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3Um93

GuideReviewRow.


# Class Name

`GuideReviewRow`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Item` | `string` | Required | Item. |
| `Source` | [`models.Source9Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/source-9.md) | Required | Source. |
| `Value` | `string` | Required | Value.<br><br>**Constraints**: *Maximum Length*: `120` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideReviewRow := models.GuideReviewRow{
        Item:   "item6",
        Source: models.Source9Enum_WORDS,
        Value:  "value6",
    }

}
```



