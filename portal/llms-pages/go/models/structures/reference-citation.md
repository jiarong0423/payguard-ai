# Reference Citation

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlJlZmVyZW5jZUNpdGF0aW9u

ReferenceCitation.


# Class Name

`ReferenceCitation`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CaseOutcome` | [`models.ReferenceCitationCaseOutcome`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/reference-citation-case-outcome.md) | Required | This is a container for any-of cases. |
| `CaseStage` | [`models.CaseStageEnum`](http://localhost:3000/llms-pages/go/models/enumerations/case-stage.md) | Required | Case stage. |
| `ChunkId` | `string` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `DecisionAcceptanceDeadline` | [`models.ReferenceCitationDecisionAcceptanceDeadline`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/reference-citation-decision-acceptance-deadline.md) | Required | This is a container for any-of cases. |
| `DecisionDate` | [`models.ReferenceCitationDecisionDate`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/reference-citation-decision-date.md) | Required | This is a container for any-of cases. |
| `DecisionDateStatus` | [`models.DecisionDateStatusEnum`](http://localhost:3000/llms-pages/go/models/enumerations/decision-date-status.md) | Required | Decision date status. |
| `EffectiveDate` | [`models.ReferenceCitationEffectiveDate`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/reference-citation-effective-date.md) | Required | This is a container for any-of cases. |
| `EffectiveDateStatus` | [`models.EffectiveDateStatusEnum`](http://localhost:3000/llms-pages/go/models/enumerations/effective-date-status.md) | Required | Effective date status. |
| `Jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `JurisdictionLabel` | `string` | Required | Jurisdiction label.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `Locator` | `string` | Required | Locator.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `MaterialType` | [`models.MaterialType1Enum`](http://localhost:3000/llms-pages/go/models/enumerations/material-type-1.md) | Required | Material type. |
| `RelevanceScore` | `int` | Required | Relevance score.<br><br>**Constraints**: `>= 1`, `<= 128` |
| `RetrievedAt` | `string` | Required | Retrieved at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `SourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128` |
| `SourceTitle` | `string` | Required | Source title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `SourceUpdatedDate` | [`models.ReferenceCitationSourceUpdatedDate`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/reference-citation-source-updated-date.md) | Required | This is a container for any-of cases. |
| `SourceUpdatedDateStatus` | [`models.SourceUpdatedDateStatusEnum`](http://localhost:3000/llms-pages/go/models/enumerations/source-updated-date-status.md) | Required | Source updated date status. |
| `Text` | `string` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `TextSha256` | `string` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `Title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `Url` | `string` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    referenceCitation := models.ReferenceCitation{
        CaseOutcome:                models.ReferenceCitationCaseOutcomeContainer.FromCaseOutcome(models.CaseOutcomeEnum_SETTLEMENTAPPROVALNOTFINALMERITS),
        CaseStage:                  models.CaseStageEnum_PROCEDURALORDER,
        ChunkId:                    "chunk_id0",
        DecisionAcceptanceDeadline: models.ReferenceCitationDecisionAcceptanceDeadlineContainer.FromString("String7"),
        DecisionDate:               models.ReferenceCitationDecisionDateContainer.FromString("String1"),
        DecisionDateStatus:         models.DecisionDateStatusEnum_NOTAPPLICABLE,
        EffectiveDate:              models.ReferenceCitationEffectiveDateContainer.FromString("String9"),
        EffectiveDateStatus:        models.EffectiveDateStatusEnum_DOCUMENTSTATED,
        Jurisdiction:               "US",
        JurisdictionLabel:          "jurisdiction_label6",
        Locator:                    "locator0",
        MaterialType:               models.MaterialType1Enum_OFFICIALAPIREFERENCE,
        RelevanceScore:             128,
        RetrievedAt:                "retrieved_at2",
        SourceId:                   "source_id2",
        SourceTitle:                "source_title4",
        SourceUpdatedDate:          models.ReferenceCitationSourceUpdatedDateContainer.FromString("String1"),
        SourceUpdatedDateStatus:    models.SourceUpdatedDateStatusEnum_DOCUMENTSTATED,
        Text:                       "text8",
        TextSha256:                 "text_sha2566",
        Title:                      "title4",
        Url:                        "url2",
    }

}
```



