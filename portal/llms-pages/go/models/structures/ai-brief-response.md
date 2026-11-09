# Ai Brief Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkFpQnJpZWZSZXNwb25zZQ

AiBriefResponse.


# Class Name

`AiBriefResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `AiGenerated` | `string` | Required, Constant | Ai generated.<br><br>**Value**: `"True"` |
| `Brief` | [`models.GeneratedBrief`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/generated-brief.md) | Required | GeneratedBrief. |
| `ComplianceDecision` | `string` | Required, Constant | Compliance decision.<br><br>**Value**: `"NOT_MADE"` |
| `ContextDigest` | `string` | Required | Context digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `CorpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `CurrentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `ExecutionEvidence` | [`models.ExecutionEvidenceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/execution-evidence.md) | Required | Execution evidence. |
| `ExternalActionAuthorized` | `string` | Required, Constant | External action authorized.<br><br>**Value**: `"False"` |
| `FixtureId` | [`models.FixtureIdEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/fixture-id.md) | Required | Fixture id. |
| `HumanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `"True"` |
| `Limitations` | `[]string` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `3`, *Maximum Items*: `3` |
| `Model` | [`models.ModelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/model.md) | Required | Model. |
| `PromptContractDigest` | `string` | Required | Prompt contract digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `PromptContractId` | `string` | Required, Constant | Prompt contract id.<br><br>**Value**: `"payguard-bounded-advisory-v3"` |
| `SchemaVersion` | `string` | Required, Constant | Schema version.<br><br>**Value**: `"1.0"` |
| `SemanticEntailment` | `string` | Required, Constant | Semantic entailment.<br><br>**Value**: `"NOT_EVALUATED"` |
| `Stage` | [`models.StageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/stage.md) | Required | Stage. |
| `Status` | `string` | Required, Constant | Status.<br><br>**Value**: `"completed"` |
| `WorkflowTransitionAuthorized` | `string` | Required, Constant | Workflow transition authorized.<br><br>**Value**: `"False"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    aiBriefResponse := models.AiBriefResponse{
        AdvisoryOnly:                 "True",
        AiGenerated:                  "True",
        Brief:                        models.GeneratedBrief{
            CitationIds:     []string{
                "citation_ids5",
                "citation_ids6",
                "citation_ids7",
            },
            EvidencePoints:  []string{
                "evidence_points6",
                "evidence_points7",
            },
            MissingEvidence: []string{
                "missing_evidence9",
            },
            Summary:         "summary6",
        },
        ComplianceDecision:           "NOT_MADE",
        ContextDigest:                "context_digest2",
        CorpusDigest:                 "corpus_digest8",
        CurrentPolicyApplicability:   "NOT_ESTABLISHED",
        ExecutionEvidence:            models.ExecutionEvidenceEnum_OPERATORLIVERESPONSE,
        ExternalActionAuthorized:     "False",
        FixtureId:                    models.FixtureIdEnum_PAYGUARDFIXEDSYNTHETICBRIEFV1,
        HumanReviewRequired:          "True",
        Limitations:                  []string{
            "limitations1",
        },
        Model:                        models.ModelEnum_ENUMGEMINI38FLASH,
        PromptContractDigest:         "prompt_contract_digest8",
        PromptContractId:             "payguard-bounded-advisory-v3",
        SchemaVersion:                "1.0",
        SemanticEntailment:           "NOT_EVALUATED",
        Stage:                        models.StageEnum_DISPUTEMEDIATION,
        Status:                       "completed",
        WorkflowTransitionAuthorized: "False",
    }

}
```



