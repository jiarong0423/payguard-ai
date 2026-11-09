# Scenario

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlNjZW5hcmlv

Scenario.


# Class Name

`Scenario`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Burst` | `bool` | Required | Burst. |
| `Dispute` | `bool` | Required | Dispute. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    scenario := models.Scenario{
        Burst:   false,
        Dispute: false,
    }

}
```



