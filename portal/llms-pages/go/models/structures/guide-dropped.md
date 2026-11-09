# Guide Dropped

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkd1aWRlRHJvcHBlZA

GuideDropped.


# Class Name

`GuideDropped`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Item` | `string` | Required | Item. |
| `Reason` | [`models.Reason6Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/reason-6.md) | Required | Reason. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideDropped := models.GuideDropped{
        Item:   "item6",
        Reason: models.Reason6Enum_OTHERPARTY,
    }

}
```



