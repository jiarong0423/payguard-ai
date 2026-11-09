# Ai Brief Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkFpQnJpZWZSZXNwb25zZQ

AiBriefResponse.


# Class Name

`AiBriefResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `AiGenerated` | `string` | Required, Constant | Ai generated.<br><br>**Value**: `"True"` |
| `Brief` | [`GeneratedBrief`](http://localhost:3000/llms-pages/net-standard-library/models/structures/generated-brief.md) | Required | GeneratedBrief. |
| `ComplianceDecision` | `string` | Required, Constant | Compliance decision.<br><br>**Value**: `"NOT_MADE"` |
| `ContextDigest` | `string` | Required | Context digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `CorpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `CurrentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `ExecutionEvidence` | [`ExecutionEvidenceEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/execution-evidence.md) | Required | Execution evidence. |
| `ExternalActionAuthorized` | `string` | Required, Constant | External action authorized.<br><br>**Value**: `"False"` |
| `FixtureId` | [`FixtureIdEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/fixture-id.md) | Required | Fixture id. |
| `HumanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `"True"` |
| `Limitations` | `List<string>` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `3`, *Maximum Items*: `3` |
| `Model` | [`ModelEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/model.md) | Required | Model. |
| `PromptContractDigest` | `string` | Required | Prompt contract digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `PromptContractId` | `string` | Required, Constant | Prompt contract id.<br><br>**Value**: `"payguard-bounded-advisory-v3"` |
| `SchemaVersion` | `string` | Required, Constant | Schema version.<br><br>**Value**: `"1.0"` |
| `SemanticEntailment` | `string` | Required, Constant | Semantic entailment.<br><br>**Value**: `"NOT_EVALUATED"` |
| `Stage` | [`StageEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/stage.md) | Required | Stage. |
| `Status` | `string` | Required, Constant | Status.<br><br>**Value**: `"completed"` |
| `WorkflowTransitionAuthorized` | `string` | Required, Constant | Workflow transition authorized.<br><br>**Value**: `"False"` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;

AiBriefResponse aiBriefResponse = new AiBriefResponse
{
    AdvisoryOnly = "True",
    AiGenerated = "True",
    Brief = new GeneratedBrief
    {
        CitationIds = new List<string>
        {
            "citation_ids5",
            "citation_ids6",
            "citation_ids7",
        },
        EvidencePoints = new List<string>
        {
            "evidence_points6",
            "evidence_points7",
        },
        MissingEvidence = new List<string>
        {
            "missing_evidence9",
        },
        Summary = "summary6",
    },
    ComplianceDecision = "NOT_MADE",
    ContextDigest = "context_digest2",
    CorpusDigest = "corpus_digest8",
    CurrentPolicyApplicability = "NOT_ESTABLISHED",
    ExecutionEvidence = ExecutionEvidenceEnum.OPERATORLIVERESPONSE,
    ExternalActionAuthorized = "False",
    FixtureId = FixtureIdEnum.Payguardfixedsyntheticbriefv1,
    HumanReviewRequired = "True",
    Limitations = new List<string>
    {
        "limitations1",
    },
    Model = ModelEnum.EnumGemini38flash,
    PromptContractDigest = "prompt_contract_digest8",
    PromptContractId = "payguard-bounded-advisory-v3",
    SchemaVersion = "1.0",
    SemanticEntailment = "NOT_EVALUATED",
    Stage = StageEnum.DisputeMediation,
    Status = "completed",
    WorkflowTransitionAuthorized = "False",
};
```



