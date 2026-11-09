# Dispute Amount

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkRpc3B1dGVBbW91bnQ

Dispute amount.


# Class Name

`DisputeAmount`


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
    disputeAmount := models.DisputeAmount{
        CurrencyCode:         models.ToPointer("currency_code0"),
        Value:                models.ToPointer("value6"),
    }

}
```



