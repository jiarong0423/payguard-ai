# Guide Gap

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlR2Fw

GuideGap.


# Class Name

`GuideGap`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Conflicting` | `[]string` | Required | Conflicting. |
| `Missing` | `[]string` | Required | Missing. |
| `Partial` | `[]string` | Required | Partial. |
| `Present` | `[]string` | Required | Present. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideGap := models.GuideGap{
        Conflicting: []string{
            "conflicting9",
        },
        Missing:     []string{
            "missing4",
        },
        Partial:     []string{
            "partial4",
            "partial5",
        },
        Present:     []string{
            "present9",
            "present0",
            "present1",
        },
    }

}
```



