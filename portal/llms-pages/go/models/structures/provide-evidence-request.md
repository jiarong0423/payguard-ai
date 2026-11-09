# Provide Evidence Request

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlcXVlc3Q

ProvideEvidenceRequest.


# Class Name

`ProvideEvidenceRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CaseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `ConfirmToken` | [`*models.ProvideEvidenceRequestConfirmToken`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/provide-evidence-request-confirm-token.md) | Optional | This is a container for any-of cases. |
| `DisputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `Submit` | `*bool` | Optional | Submit.<br><br>**Default**: `false` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    provideEvidenceRequest := models.ProvideEvidenceRequest{
        CaseRef:      "case_ref0",
        ConfirmToken: models.ToPointer(models.ProvideEvidenceRequestConfirmTokenContainer.FromString("String7")),
        DisputeId:    "dispute_id8",
        Submit:       models.ToPointer(false),
    }

}
```



