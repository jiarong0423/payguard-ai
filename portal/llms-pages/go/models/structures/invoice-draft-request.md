# Invoice Draft Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkludm9pY2VEcmFmdFJlcXVlc3Q

InvoiceDraftRequest.


# Class Name

`InvoiceDraftRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Amount` | `string` | Required | Amount.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,9}(?:\.[0-9]{1,2})?$` |
| `Currency` | [`models.CurrencyEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/currency.md) | Required | Currency. |
| `Description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` |
| `PayloadDigest` | `string` | Required | Payload digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `ReviewToken` | `string` | Required | Review token.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    invoiceDraftRequest := models.InvoiceDraftRequest{
        Amount:        "amount6",
        Currency:      models.CurrencyEnum_JPY,
        Description:   "description4",
        PayloadDigest: "payload_digest6",
        ReviewToken:   "review_token2",
    }

}
```



