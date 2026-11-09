# Generated Brief

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkdlbmVyYXRlZEJyaWVm

GeneratedBrief.


# Class Name

`GeneratedBrief`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CitationIds` | `[]string` | Required | Citation ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3`, *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z0-9-]+$` |
| `EvidencePoints` | `[]string` | Required | Evidence points.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` |
| `MissingEvidence` | `[]string` | Required | Missing evidence.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` |
| `Summary` | `string` | Required | Summary.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1200` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    generatedBrief := models.GeneratedBrief{
        CitationIds:     []string{
            "citation_ids9",
        },
        EvidencePoints:  []string{
            "evidence_points2",
            "evidence_points1",
        },
        MissingEvidence: []string{
            "missing_evidence3",
            "missing_evidence4",
        },
        Summary:         "summary0",
    }

}
```



