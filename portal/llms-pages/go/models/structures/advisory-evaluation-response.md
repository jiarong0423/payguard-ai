# Advisory Evaluation Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkFkdmlzb3J5RXZhbHVhdGlvblJlc3BvbnNl

AdvisoryEvaluationResponse.


# Class Name

`AdvisoryEvaluationResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `PIIQuality` | `string` | Required, Constant | PII quality.<br><br>**Value**: `"NOT_EVALUATED"` |
| `AdvisoryOnly` | `bool` | Required | Advisory only. |
| `ClaimCount` | `int` | Required | Claim count.<br><br>**Constraints**: `>= 1`, `<= 20` |
| `ClaimGates` | [`[]models.AdvisoryClaimGate`](http://localhost:3000/llms-pages/go/models/structures/advisory-claim-gate.md) | Required | Claim gates.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `CorpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `CorpusDigests` | [`models.ReferenceDigests`](http://localhost:3000/llms-pages/go/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `CorpusId` | `string` | Required, Constant | Corpus id.<br><br>**Value**: `"payguard-us-official-references-v2"` |
| `Coverage` | [`models.PolicyCoverage`](http://localhost:3000/llms-pages/go/models/structures/policy-coverage.md) | Required | PolicyCoverage. |
| `CurrentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `Limitations` | `[]string` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `ModelGeneration` | `string` | Required, Constant | Model generation.<br><br>**Value**: `"NOT_RUN"` |
| `NaturalLanguageActionAssuranceQuality` | `string` | Required, Constant | Natural language action assurance quality.<br><br>**Value**: `"NOT_EVALUATED"` |
| `OperationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` |
| `PromptInjectionQuality` | `string` | Required, Constant | Prompt injection quality.<br><br>**Value**: `"NOT_EVALUATED"` |
| `RequestedContext` | [`models.PolicyContext`](http://localhost:3000/llms-pages/go/models/structures/policy-context.md) | Required | PolicyContext. |
| `RequiresHumanReview` | `bool` | Required | Requires human review. |
| `SchemaVersion` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `SemanticEntailment` | `string` | Required, Constant | Semantic entailment.<br><br>**Value**: `"NOT_EVALUATED"` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"offline_structured_gate"` |
| `Status` | [`models.StatusEnum`](http://localhost:3000/llms-pages/go/models/enumerations/status.md) | Required | Status. |
| `Version` | `string` | Required, Constant | Version.<br><br>**Value**: `"payguard.advisory_eval.v1"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    advisoryEvaluationResponse := models.AdvisoryEvaluationResponse{
        PIIQuality:                            "NOT_EVALUATED",
        AdvisoryOnly:                          false,
        ClaimCount:                            20,
        ClaimGates:                            []models.AdvisoryClaimGate{
            models.AdvisoryClaimGate{
                ClaimIndex:              19,
                ClaimType:               models.ClaimTypeEnum_POLICYREFERENCE,
                ReasonCodes:             []models.ReasonCodeEnum{
                    models.ReasonCodeEnum_ASSURANCECLAIMFORBIDDEN,
                    models.ReasonCodeEnum_CITATIONUNKNOWN,
                    models.ReasonCodeEnum_CITATIONREGIONMISMATCH,
                },
                Status:                  models.StatusEnum_INCOMPLETEEVIDENCE,
                TrustedCitationChunkIds: []string{
                    "trusted_citation_chunk_ids4",
                    "trusted_citation_chunk_ids5",
                },
            },
        },
        CorpusDigest:                          "corpus_digest4",
        CorpusDigests:                         models.ReferenceDigests{
            ChunksSha256:  "chunks_sha2564",
            SourcesSha256: "sources_sha2562",
        },
        CorpusId:                              "payguard-us-official-references-v2",
        Coverage:                              models.PolicyCoverage{
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
        CurrentPolicyApplicability:            "NOT_ESTABLISHED",
        Limitations:                           []string{
            "limitations3",
            "limitations4",
            "limitations5",
        },
        ModelGeneration:                       "NOT_RUN",
        NaturalLanguageActionAssuranceQuality: "NOT_EVALUATED",
        OperationalAuthority:                  "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
        PromptInjectionQuality:                "NOT_EVALUATED",
        RequestedContext:                      models.PolicyContext{
            AsOf:                  "as_of8",
            Jurisdiction:          "US",
            ObservationMaxAgeDays: 14,
            Theme:                 models.ThemeEnum_DISPUTEMEDIATION,
        },
        RequiresHumanReview:                   false,
        SchemaVersion:                         1,
        SemanticEntailment:                    "NOT_EVALUATED",
        Source:                                "offline_structured_gate",
        Status:                                models.StatusEnum_INCOMPLETEEVIDENCE,
        Version:                               "payguard.advisory_eval.v1",
    }

}
```



