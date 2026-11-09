# Guide Field

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkd1aWRlRmllbGQ

GuideField.


# Class Name

`GuideField`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Item` | `string` | Required | Item.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z_]+$` |
| `Value` | `string` | Required | Value.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `120` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideField := models.GuideField{
        Item:  "item8",
        Value: "value8",
    }

}
```



