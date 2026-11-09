# Guide Form Result

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlc3VsdA

GuideFormResult.


# Class Name

`GuideFormResult`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Item` | `string` | Required | Item. |
| `Valid` | `bool` | Required | Valid. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideFormResult := models.GuideFormResult{
        Item:  "item2",
        Valid: false,
    }

}
```



