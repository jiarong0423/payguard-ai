# Approve Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkFwcHJvdmVSZXF1ZXN0

ApproveRequest.


# Class Name

`ApproveRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `DraftDigest` | `string` | Required | Draft digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    approveRequest := models.ApproveRequest{
        DraftDigest: "draft_digest6",
    }

}
```



