# Reference Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlc3BvbnNl

ReferenceResponse.


# Class Name

`ReferenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `bool` | Required | Advisory only. |
| `CorpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `CorpusDigests` | [`models.ReferenceDigests`](http://localhost:3000/llms-pages/go/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `CorpusId` | `string` | Required, Constant | Corpus id.<br><br>**Value**: `"payguard-us-official-references-v2"` |
| `FiltersApplied` | [`models.ReferenceFilters`](http://localhost:3000/llms-pages/go/models/structures/reference-filters.md) | Required | ReferenceFilters. |
| `Limitations` | `[]string` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `OperationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` |
| `Results` | [`[]models.ReferenceCitation`](http://localhost:3000/llms-pages/go/models/structures/reference-citation.md) | Required | Results.<br><br>**Constraints**: *Maximum Items*: `10` |
| `SchemaVersion` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"public_reference"` |
| `Status` | [`models.Status13Enum`](http://localhost:3000/llms-pages/go/models/enumerations/status-13.md) | Required | Status. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    referenceResponse := models.ReferenceResponse{
        AdvisoryOnly:         false,
        CorpusDigest:         "corpus_digest2",
        CorpusDigests:        models.ReferenceDigests{
            ChunksSha256:  "chunks_sha2564",
            SourcesSha256: "sources_sha2562",
        },
        CorpusId:             "payguard-us-official-references-v2",
        FiltersApplied:       models.ReferenceFilters{
            AgeBasis:               "source_updated_date_utc_calendar",
            AsOf:                   models.ReferenceFiltersAsOfContainer.FromString("String1"),
            CaseStage:              models.CaseStage2Enum_PROCEDURALORDER,
            Jurisdiction:           "US",
            Limit:                  10,
            MaterialTypes:          []models.MaterialType4Enum{
                models.MaterialType4Enum_OFFICIALPOLICY,
                models.MaterialType4Enum_PUBLICCOURTORDERCOPY,
            },
            MaxSourceAgeDays:       models.ReferenceFiltersMaxSourceAgeDaysContainer.FromNumber(28),
            RequireKnownSourceDate: false,
            Theme:                  models.ThemeEnum_DISPUTEMEDIATION,
        },
        Limitations:          []string{
            "limitations5",
            "limitations6",
        },
        OperationalAuthority: "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
        Results:              []models.ReferenceCitation{
            models.ReferenceCitation{
                CaseOutcome:                models.ReferenceCitationCaseOutcomeContainer.FromCaseOutcome(models.CaseOutcomeEnum_SETTLEMENTAPPROVALNOTFINALMERITS),
                CaseStage:                  models.CaseStageEnum_PROCEDURALORDER,
                ChunkId:                    "chunk_id2",
                DecisionAcceptanceDeadline: models.ReferenceCitationDecisionAcceptanceDeadlineContainer.FromString("String5"),
                DecisionDate:               models.ReferenceCitationDecisionDateContainer.FromString("String9"),
                DecisionDateStatus:         models.DecisionDateStatusEnum_NOTAPPLICABLE,
                EffectiveDate:              models.ReferenceCitationEffectiveDateContainer.FromString("String5"),
                EffectiveDateStatus:        models.EffectiveDateStatusEnum_DOCUMENTSTATED,
                Jurisdiction:               "US",
                JurisdictionLabel:          "jurisdiction_label4",
                Locator:                    "locator8",
                MaterialType:               models.MaterialType1Enum_OFFICIALAPIREFERENCE,
                RelevanceScore:             128,
                RetrievedAt:                "retrieved_at0",
                SourceId:                   "source_id0",
                SourceTitle:                "source_title8",
                SourceUpdatedDate:          models.ReferenceCitationSourceUpdatedDateContainer.FromString("String9"),
                SourceUpdatedDateStatus:    models.SourceUpdatedDateStatusEnum_DOCUMENTSTATED,
                Text:                       "text4",
                TextSha256:                 "text_sha2566",
                Title:                      "title8",
                Url:                        "url0",
            },
        },
        SchemaVersion:        1,
        Source:               "public_reference",
        Status:               models.Status13Enum_REFERENCESFOUND,
    }

}
```



