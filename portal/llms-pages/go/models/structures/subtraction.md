# Subtraction

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlN1YnRyYWN0aW9u

Subtraction.


# Class Name

`Subtraction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Left` | `*int` | Optional | Left. |
| `Needed` | `*int` | Optional | Needed. |
| `Taken` | `*int` | Optional | Taken. |
| `Text` | `*string` | Optional | Text. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    subtraction := models.Subtraction{
        Left:                 models.ToPointer(232),
        Needed:               models.ToPointer(102),
        Taken:                models.ToPointer(90),
        Text:                 models.ToPointer("text6"),
    }

}
```



