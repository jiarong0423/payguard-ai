# Form Result

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkZvcm1SZXN1bHQ

Form result.


# Class Name

`FormResult`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Item` | `*string` | Optional | Item. |
| `Valid` | `*bool` | Optional | Valid. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    formResult := models.FormResult{
        Item:                 models.ToPointer("item8"),
        Valid:                models.ToPointer(false),
    }

}
```



