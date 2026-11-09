# Policy Assessment Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlBvbGljeUFzc2Vzc21lbnRSZXNwb25zZQ

PolicyAssessmentResponse.


# Class Name

`PolicyAssessmentResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `bool` | Required | Advisory only. |
| `Chunks` | [`[]models.PolicyChunk`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/policy-chunk.md) | Required | Chunks.<br><br>**Constraints**: *Maximum Items*: `29` |
| `CorpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `CorpusDigests` | [`models.ReferenceDigests`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `CorpusId` | `string` | Required, Constant | Corpus id.<br><br>**Value**: `"payguard-us-official-references-v2"` |
| `Coverage` | [`models.PolicyCoverage`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/policy-coverage.md) | Required | PolicyCoverage. |
| `CurrentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `FiltersApplied` | [`models.PolicyContext`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/policy-context.md) | Required | PolicyContext. |
| `Limitations` | `[]string` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `OperationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` |
| `ReasonCodes` | [`[]models.ReasonCode1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` |
| `RequiresHumanReview` | `bool` | Required | Requires human review. |
| `SchemaVersion` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"public_reference"` |
| `Sources` | [`[]models.PolicySource`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/policy-source.md) | Required | Sources.<br><br>**Constraints**: *Maximum Items*: `16` |
| `Status` | `string` | Required, Constant | Status.<br><br>**Value**: `"INCOMPLETE_POLICY_EVIDENCE"` |
| `Version` | `string` | Required, Constant | Version.<br><br>**Value**: `"payguard.applicability.v1"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    policyAssessmentResponse := models.PolicyAssessmentResponse{
        AdvisoryOnly:               false,
        Chunks:                     []models.PolicyChunk{
            models.PolicyChunk{
                CaseOutcome:  models.PolicyChunkCaseOutcomeContainer.FromCaseOutcome(models.CaseOutcomeEnum_SETTLEMENTAPPROVALNOTFINALMERITS),
                CaseStage:    models.CaseStageEnum_PROCEDURALORDER,
                ChunkId:      "chunk_id6",
                Jurisdiction: "US",
                MaterialType: models.MaterialType1Enum_OFFICIALPOLICY,
                SourceId:     "source_id6",
                TextSha256:   "text_sha2560",
                Theme:        models.ThemeEnum_VELOCITYGUARD,
            },
        },
        CorpusDigest:               "corpus_digest2",
        CorpusDigests:              models.ReferenceDigests{
            ChunksSha256:  "chunks_sha2564",
            SourcesSha256: "sources_sha2562",
        },
        CorpusId:                   "payguard-us-official-references-v2",
        Coverage:                   models.PolicyCoverage{
            Basis:                           "pinned_authored_summaries_only",
            Complete:                        false,
            MissingOfficialPolicyThemes:     []models.MissingOfficialPolicyThemeEnum{
                models.MissingOfficialPolicyThemeEnum_SOURCECOMPLIANCE,
            },
            OfficialPolicyChunkCountByTheme: models.PolicyThemeCounts{
                DisputeMediation: 12,
                SourceCompliance: 29,
                VelocityGuard:    29,
            },
            OfficialPolicySourceIds:         []string{
                "official_policy_source_ids0",
            },
            RegionalSourceCount:             16,
            SelectedChunkCount:              29,
            SelectedSourceCount:             16,
        },
        CurrentPolicyApplicability: "NOT_ESTABLISHED",
        FiltersApplied:             models.PolicyContext{
            AsOf:                  "as_of0",
            Jurisdiction:          "US",
            ObservationMaxAgeDays: 28,
            Theme:                 models.ThemeEnum_DISPUTEMEDIATION,
        },
        Limitations:                []string{
            "limitations5",
            "limitations4",
            "limitations3",
        },
        OperationalAuthority:       "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
        ReasonCodes:                []models.ReasonCode1Enum{
            models.ReasonCode1Enum_CURRENTPOLICYAPPLICABILITYNOTESTABLISHED,
            models.ReasonCode1Enum_FUTUREOBSERVATION,
        },
        RequiresHumanReview:        false,
        SchemaVersion:              1,
        Source:                     "public_reference",
        Sources:                    []models.PolicySource{
            models.PolicySource{
                CitationChunkIds:           []string{
                    "citation_chunk_ids2",
                    "citation_chunk_ids3",
                },
                ContentClass:               "public_reference_summary",
                CurrentPolicyApplicability: "NOT_ESTABLISHED",
                DecisionAcceptanceDeadline: models.PolicySourceDecisionAcceptanceDeadlineContainer.FromString("String5"),
                DecisionDate:               models.PolicySourceDecisionDateContainer.FromString("String9"),
                DecisionDateStatus:         models.DecisionDateStatusEnum_DOCUMENTSTATED,
                EffectiveDate:              models.PolicySourceEffectiveDateContainer.FromString("String7"),
                EffectiveDateStatus:        models.EffectiveDateStatusEnum_DOCUMENTSTATED,
                Jurisdiction:               "jurisdiction0",
                JurisdictionNormalized:     "US",
                MaterialType:               models.MaterialType1Enum_PUBLICCOURTORDERCOPY,
                ObservationAgeBasis:        "saved_retrieved_at_exact_elapsed_time",
                ObservationStatus:          models.ObservationStatusEnum_FUTUREOBSERVATION,
                ReasonCodes:                []models.ReasonCode1Enum{
                    models.ReasonCode1Enum_CURRENTPOLICYAPPLICABILITYNOTESTABLISHED,
                    models.ReasonCode1Enum_FUTUREOBSERVATION,
                },
                Representation:             "authored_paraphrase_not_full_source",
                RetrievedAt:                "retrieved_at0",
                SourceId:                   "source_id0",
                SourceUpdatedDate:          models.PolicySourceSourceUpdatedDateContainer.FromString("String9"),
                SourceUpdatedDateStatus:    models.SourceUpdatedDateStatusEnum_DOCUMENTSTATED,
                Title:                      "title2",
                Url:                        "url0",
            },
        },
        Status:                     "INCOMPLETE_POLICY_EVIDENCE",
        Version:                    "payguard.applicability.v1",
    }

}
```



