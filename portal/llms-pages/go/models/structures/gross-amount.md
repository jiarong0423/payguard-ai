# Gross Amount

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkdyb3NzQW1vdW50

Gross amount.


# Class Name

`GrossAmount`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CurrencyCode` | `*string` | Optional | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `Value` | `*string` | Optional | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    grossAmount := models.GrossAmount{
        CurrencyCode:         models.ToPointer("currency_code6"),
        Value:                models.ToPointer("value2"),
    }

}
```



