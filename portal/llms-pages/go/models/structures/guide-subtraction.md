# Guide Subtraction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkd1aWRlU3VidHJhY3Rpb24

GuideSubtraction.


# Class Name

`GuideSubtraction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Left` | `int` | Required | Left. |
| `Needed` | `int` | Required | Needed. |
| `Taken` | `int` | Required | Taken. |
| `Text` | `string` | Required | Text. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideSubtraction := models.GuideSubtraction{
        Left:                 18,
        Needed:               112,
        Taken:                124,
        Text:                 "text8",
    }

}
```



