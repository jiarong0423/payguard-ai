# Guide Field Result

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlRmllbGRSZXN1bHQ

GuideFieldResult.


# Class Name

`GuideFieldResult`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Deferred` | `bool` | Required | Deferred. |
| `Item` | `string` | Required | Item. |
| `Valid` | `bool` | Required | Valid. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideFieldResult := models.GuideFieldResult{
        Deferred: false,
        Item:     "item8",
        Valid:    false,
    }

}
```



