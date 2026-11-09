# Add Tracking Request

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkFkZFRyYWNraW5nUmVxdWVzdA

AddTrackingRequest.


# Class Name

`AddTrackingRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CaseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `ConfirmToken` | [`*models.AddTrackingRequestConfirmToken`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/add-tracking-request-confirm-token.md) | Optional | This is a container for any-of cases. |
| `DisputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `Submit` | `*bool` | Optional | Submit.<br><br>**Default**: `false` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    addTrackingRequest := models.AddTrackingRequest{
        CaseRef:      "case_ref4",
        ConfirmToken: models.ToPointer(models.AddTrackingRequestConfirmTokenContainer.FromString("String1")),
        DisputeId:    "dispute_id2",
        Submit:       models.ToPointer(false),
    }

}
```



