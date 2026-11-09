# Ai Brief Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkFpQnJpZWZSZXNwb25zZQ

AiBriefResponse.


# Class Name

`AiBriefResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AdvisoryOnly` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` | String getAdvisoryOnly() | setAdvisoryOnly(String advisoryOnly) |
| `AiGenerated` | `String` | Required, Constant | Ai generated.<br><br>**Value**: `"True"` | String getAiGenerated() | setAiGenerated(String aiGenerated) |
| `Brief` | [`GeneratedBrief`](http://localhost:3000/llms-pages/java/models/structures/generated-brief.md) | Required | GeneratedBrief. | GeneratedBrief getBrief() | setBrief(GeneratedBrief brief) |
| `ComplianceDecision` | `String` | Required, Constant | Compliance decision.<br><br>**Value**: `"NOT_MADE"` | String getComplianceDecision() | setComplianceDecision(String complianceDecision) |
| `ContextDigest` | `String` | Required | Context digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getContextDigest() | setContextDigest(String contextDigest) |
| `CorpusDigest` | `String` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getCorpusDigest() | setCorpusDigest(String corpusDigest) |
| `CurrentPolicyApplicability` | `String` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` | String getCurrentPolicyApplicability() | setCurrentPolicyApplicability(String currentPolicyApplicability) |
| `ExecutionEvidence` | [`ExecutionEvidenceEnum`](http://localhost:3000/llms-pages/java/models/enumerations/execution-evidence.md) | Required | Execution evidence. | ExecutionEvidenceEnum getExecutionEvidence() | setExecutionEvidence(ExecutionEvidenceEnum executionEvidence) |
| `ExternalActionAuthorized` | `String` | Required, Constant | External action authorized.<br><br>**Value**: `"False"` | String getExternalActionAuthorized() | setExternalActionAuthorized(String externalActionAuthorized) |
| `FixtureId` | [`FixtureIdEnum`](http://localhost:3000/llms-pages/java/models/enumerations/fixture-id.md) | Required | Fixture id. | FixtureIdEnum getFixtureId() | setFixtureId(FixtureIdEnum fixtureId) |
| `HumanReviewRequired` | `String` | Required, Constant | Human review required.<br><br>**Value**: `"True"` | String getHumanReviewRequired() | setHumanReviewRequired(String humanReviewRequired) |
| `Limitations` | `List<String>` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `3`, *Maximum Items*: `3` | List<String> getLimitations() | setLimitations(List<String> limitations) |
| `Model` | [`ModelEnum`](http://localhost:3000/llms-pages/java/models/enumerations/model.md) | Required | Model. | ModelEnum getModel() | setModel(ModelEnum model) |
| `PromptContractDigest` | `String` | Required | Prompt contract digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getPromptContractDigest() | setPromptContractDigest(String promptContractDigest) |
| `PromptContractId` | `String` | Required, Constant | Prompt contract id.<br><br>**Value**: `"payguard-bounded-advisory-v3"` | String getPromptContractId() | setPromptContractId(String promptContractId) |
| `SchemaVersion` | `String` | Required, Constant | Schema version.<br><br>**Value**: `"1.0"` | String getSchemaVersion() | setSchemaVersion(String schemaVersion) |
| `SemanticEntailment` | `String` | Required, Constant | Semantic entailment.<br><br>**Value**: `"NOT_EVALUATED"` | String getSemanticEntailment() | setSemanticEntailment(String semanticEntailment) |
| `Stage` | [`StageEnum`](http://localhost:3000/llms-pages/java/models/enumerations/stage.md) | Required | Stage. | StageEnum getStage() | setStage(StageEnum stage) |
| `Status` | `String` | Required, Constant | Status.<br><br>**Value**: `"completed"` | String getStatus() | setStatus(String status) |
| `WorkflowTransitionAuthorized` | `String` | Required, Constant | Workflow transition authorized.<br><br>**Value**: `"False"` | String getWorkflowTransitionAuthorized() | setWorkflowTransitionAuthorized(String workflowTransitionAuthorized) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.AiBriefResponse;
import m18000.m0.m0.m127.models.ExecutionEvidenceEnum;
import m18000.m0.m0.m127.models.FixtureIdEnum;
import m18000.m0.m0.m127.models.GeneratedBrief;
import m18000.m0.m0.m127.models.ModelEnum;
import m18000.m0.m0.m127.models.StageEnum;

AiBriefResponse aiBriefResponse = new AiBriefResponse.Builder(
    "True",
    "True",
    new GeneratedBrief.Builder(
        Arrays.asList(
            "citation_ids5",
            "citation_ids6",
            "citation_ids7"
        ),
        Arrays.asList(
            "evidence_points6",
            "evidence_points7"
        ),
        Arrays.asList(
            "missing_evidence9"
        ),
        "summary6"
    )
    .build(),
    "NOT_MADE",
    "context_digest2",
    "corpus_digest8",
    "NOT_ESTABLISHED",
    ExecutionEvidenceEnum.OPERATOR_LIVE_RESPONSE,
    "False",
    FixtureIdEnum.PAYGUARDFIXEDSYNTHETICBRIEFV1,
    "True",
    Arrays.asList(
        "limitations1"
    ),
    ModelEnum.ENUM_GEMINI38FLASH,
    "prompt_contract_digest8",
    "payguard-bounded-advisory-v3",
    "1.0",
    "NOT_EVALUATED",
    StageEnum.DISPUTE_MEDIATION,
    "completed",
    "False"
)
.build();
```



