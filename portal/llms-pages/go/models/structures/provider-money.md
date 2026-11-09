# Provider Money

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlByb3ZpZGVyTW9uZXk

ProviderMoney.


# Class Name

`ProviderMoney`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CurrencyCode` | `string` | Required | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `Value` | `string` | Required | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    providerMoney := models.ProviderMoney{
        CurrencyCode:         "currency_code4",
        Value:                "value0",
    }

}
```



