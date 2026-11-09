# Dispute Evidence Row

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkRpc3B1dGVFdmlkZW5jZVJvdw

DisputeEvidenceRow.


# Class Name

`DisputeEvidenceRow`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Action` | [`*models.DisputeEvidenceRowAction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/dispute-evidence-row-action.md) | Optional | This is a container for any-of cases. |
| `Date` | [`*models.DisputeEvidenceRowDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/dispute-evidence-row-date.md) | Optional | This is a container for any-of cases. |
| `EvidenceType` | `string` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` |
| `Source` | [`models.Source3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/source-3.md) | Required | Source. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    disputeEvidenceRow := models.DisputeEvidenceRow{
        Action:       models.ToPointer(models.DisputeEvidenceRowActionContainer.FromString("String7")),
        Date:         models.ToPointer(models.DisputeEvidenceRowDateContainer.FromString("String3")),
        EvidenceType: "evidence_type8",
        Source:       models.Source3Enum_REQUESTEDFROMSELLER,
    }

}
```



