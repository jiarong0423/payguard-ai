# Ai Brief Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkFpQnJpZWZSZXNwb25zZQ

AiBriefResponse.


# Class Name

`AiBriefResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` | getAdvisoryOnly(): string | setAdvisoryOnly(string advisoryOnly): void |
| `aiGenerated` | `string` | Required, Constant | Ai generated.<br><br>**Value**: `'True'` | getAiGenerated(): string | setAiGenerated(string aiGenerated): void |
| `brief` | [`GeneratedBrief`](http://localhost:3000/llms-pages/php/models/structures/generated-brief.md) | Required | GeneratedBrief. | getBrief(): GeneratedBrief | setBrief(GeneratedBrief brief): void |
| `complianceDecision` | `string` | Required, Constant | Compliance decision.<br><br>**Value**: `'NOT_MADE'` | getComplianceDecision(): string | setComplianceDecision(string complianceDecision): void |
| `contextDigest` | `string` | Required | Context digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getContextDigest(): string | setContextDigest(string contextDigest): void |
| `corpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getCorpusDigest(): string | setCorpusDigest(string corpusDigest): void |
| `currentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` | getCurrentPolicyApplicability(): string | setCurrentPolicyApplicability(string currentPolicyApplicability): void |
| `executionEvidence` | [`string(ExecutionEvidenceEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/execution-evidence.md) | Required | Execution evidence. | getExecutionEvidence(): string | setExecutionEvidence(string executionEvidence): void |
| `externalActionAuthorized` | `string` | Required, Constant | External action authorized.<br><br>**Value**: `'False'` | getExternalActionAuthorized(): string | setExternalActionAuthorized(string externalActionAuthorized): void |
| `fixtureId` | [`string(FixtureIdEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/fixture-id.md) | Required | Fixture id. | getFixtureId(): string | setFixtureId(string fixtureId): void |
| `humanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `'True'` | getHumanReviewRequired(): string | setHumanReviewRequired(string humanReviewRequired): void |
| `limitations` | `string[]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `3`, *Maximum Items*: `3` | getLimitations(): array | setLimitations(array limitations): void |
| `model` | [`string(ModelEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/model.md) | Required | Model. | getModel(): string | setModel(string model): void |
| `promptContractDigest` | `string` | Required | Prompt contract digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getPromptContractDigest(): string | setPromptContractDigest(string promptContractDigest): void |
| `promptContractId` | `string` | Required, Constant | Prompt contract id.<br><br>**Value**: `'payguard-bounded-advisory-v3'` | getPromptContractId(): string | setPromptContractId(string promptContractId): void |
| `schemaVersion` | `string` | Required, Constant | Schema version.<br><br>**Value**: `'1.0'` | getSchemaVersion(): string | setSchemaVersion(string schemaVersion): void |
| `semanticEntailment` | `string` | Required, Constant | Semantic entailment.<br><br>**Value**: `'NOT_EVALUATED'` | getSemanticEntailment(): string | setSemanticEntailment(string semanticEntailment): void |
| `stage` | [`string(StageEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/stage.md) | Required | Stage. | getStage(): string | setStage(string stage): void |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'completed'` | getStatus(): string | setStatus(string status): void |
| `workflowTransitionAuthorized` | `string` | Required, Constant | Workflow transition authorized.<br><br>**Value**: `'False'` | getWorkflowTransitionAuthorized(): string | setWorkflowTransitionAuthorized(string workflowTransitionAuthorized): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AiBriefResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\GeneratedBriefBuilder;
use TradeGlotLocalConsoleLib\Models\ExecutionEvidenceEnum;
use TradeGlotLocalConsoleLib\Models\FixtureIdEnum;
use TradeGlotLocalConsoleLib\Models\ModelEnum;
use TradeGlotLocalConsoleLib\Models\StageEnum;

$aiBriefResponse = AiBriefResponseBuilder::init(
    GeneratedBriefBuilder::init(
        [
            'citation_ids5',
            'citation_ids6',
            'citation_ids7'
        ],
        [
            'evidence_points6',
            'evidence_points7'
        ],
        [
            'missing_evidence9'
        ],
        'summary6'
    )->build(),
    'context_digest2',
    'corpus_digest8',
    ExecutionEvidenceEnum::OPERATOR_LIVE_RESPONSE,
    FixtureIdEnum::PAYGUARDFIXEDSYNTHETICBRIEFV1,
    [
        'limitations1'
    ],
    ModelEnum::ENUM_GEMINI38FLASH,
    'prompt_contract_digest8',
    StageEnum::DISPUTE_MEDIATION
)->build();
```



