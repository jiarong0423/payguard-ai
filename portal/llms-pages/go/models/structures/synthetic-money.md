# Synthetic Money

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlN5bnRoZXRpY01vbmV5

Same shape as the PayPal Disputes `dispute_amount` (ProviderMoney below); values are synthetic.


# Class Name

`SyntheticMoney`


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
    syntheticMoney := models.SyntheticMoney{
        CurrencyCode: "currency_code8",
        Value:        "value4",
    }

}
```



