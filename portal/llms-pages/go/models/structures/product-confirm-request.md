# Product Confirm Request

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVxdWVzdA

ProductConfirmRequest.


# Class Name

`ProductConfirmRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` |
| `EvaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `ProductId` | [`models.ProductConfirmRequestProductId`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/product-confirm-request-product-id.md) | Required | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    productConfirmRequest := models.ProductConfirmRequest{
        Description:  "description6",
        EvaluationId: "evaluation_id8",
        ProductId:    models.ProductConfirmRequestProductIdContainer.FromString("String1"),
    }

}
```



