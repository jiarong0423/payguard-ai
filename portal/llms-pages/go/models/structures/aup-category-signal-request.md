# Aup Category Signal Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVxdWVzdA

AupCategorySignalRequest.


# Class Name

`AupCategorySignalRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Description` | `string` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` |
| `EvaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    aupCategorySignalRequest := models.AupCategorySignalRequest{
        Description:  "description0",
        EvaluationId: "evaluation_id4",
    }

}
```



