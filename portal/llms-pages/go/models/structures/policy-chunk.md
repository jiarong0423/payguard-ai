# Policy Chunk

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlBvbGljeUNodW5r

PolicyChunk.


# Class Name

`PolicyChunk`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CaseOutcome` | [`models.PolicyChunkCaseOutcome`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/policy-chunk-case-outcome.md) | Required | This is a container for any-of cases. |
| `CaseStage` | [`models.CaseStageEnum`](http://localhost:3000/llms-pages/go/models/enumerations/case-stage.md) | Required | Case stage. |
| `ChunkId` | `string` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `Jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `MaterialType` | [`models.MaterialType1Enum`](http://localhost:3000/llms-pages/go/models/enumerations/material-type-1.md) | Required | Material type. |
| `SourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `TextSha256` | `string` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `Theme` | [`models.ThemeEnum`](http://localhost:3000/llms-pages/go/models/enumerations/theme.md) | Required | Theme. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    policyChunk := models.PolicyChunk{
        CaseOutcome:  models.PolicyChunkCaseOutcomeContainer.FromCaseOutcome(models.CaseOutcomeEnum_SETTLEMENTAPPROVALNOTFINALMERITS),
        CaseStage:    models.CaseStageEnum_PROCEDURALORDER,
        ChunkId:      "chunk_id8",
        Jurisdiction: "US",
        MaterialType: models.MaterialType1Enum_OFFICIALAPIREFERENCE,
        SourceId:     "source_id4",
        TextSha256:   "text_sha2562",
        Theme:        models.ThemeEnum_SOURCECOMPLIANCE,
    }

}
```



