# Guide Review Row

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3Um93

GuideReviewRow.


# Class Name

`GuideReviewRow`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Item` | `string` | Required | Item. |
| `Source` | [`models.Source9Enum`](http://localhost:3000/llms-pages/go/models/enumerations/source-9.md) | Required | Source. |
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



