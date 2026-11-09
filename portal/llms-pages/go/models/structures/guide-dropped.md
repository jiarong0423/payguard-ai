# Guide Dropped

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlRHJvcHBlZA

GuideDropped.


# Class Name

`GuideDropped`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Item` | `string` | Required | Item. |
| `Reason` | [`models.Reason6Enum`](http://localhost:3000/llms-pages/go/models/enumerations/reason-6.md) | Required | Reason. |


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



