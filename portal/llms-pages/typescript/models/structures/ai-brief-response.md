# Ai Brief Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkFpQnJpZWZSZXNwb25zZQ

AiBriefResponse.


# Interface Name

`AiBriefResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `aiGenerated` | `string` | Required, Constant | Ai generated.<br><br>**Value**: `'True'` |
| `brief` | [`GeneratedBrief`](http://localhost:3000/llms-pages/typescript/models/structures/generated-brief.md) | Required | GeneratedBrief. |
| `complianceDecision` | `string` | Required, Constant | Compliance decision.<br><br>**Value**: `'NOT_MADE'` |
| `contextDigest` | `string` | Required | Context digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `corpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `currentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` |
| `executionEvidence` | [`ExecutionEvidenceEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/execution-evidence.md) | Required | Execution evidence. |
| `externalActionAuthorized` | `string` | Required, Constant | External action authorized.<br><br>**Value**: `'False'` |
| `fixtureId` | [`FixtureIdEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/fixture-id.md) | Required | Fixture id. |
| `humanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `'True'` |
| `limitations` | `string[]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `3`, *Maximum Items*: `3` |
| `model` | [`ModelEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/model.md) | Required | Model. |
| `promptContractDigest` | `string` | Required | Prompt contract digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `promptContractId` | `string` | Required, Constant | Prompt contract id.<br><br>**Value**: `'payguard-bounded-advisory-v3'` |
| `schemaVersion` | `string` | Required, Constant | Schema version.<br><br>**Value**: `'1.0'` |
| `semanticEntailment` | `string` | Required, Constant | Semantic entailment.<br><br>**Value**: `'NOT_EVALUATED'` |
| `stage` | [`StageEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/stage.md) | Required | Stage. |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'completed'` |
| `workflowTransitionAuthorized` | `string` | Required, Constant | Workflow transition authorized.<br><br>**Value**: `'False'` |


# Example

```ts
import {
  AiBriefResponse,
  ExecutionEvidenceEnum,
  FixtureIdEnum,
  ModelEnum,
  StageEnum,
} from 'tradeglot-local-consolelib';

const aiBriefResponse: AiBriefResponse = {
  advisoryOnly: 'True',
  aiGenerated: 'True',
  brief: {
    citationIds: [
      'citation_ids5',
      'citation_ids6',
      'citation_ids7'
    ],
    evidencePoints: [
      'evidence_points6',
      'evidence_points7'
    ],
    missingEvidence: [
      'missing_evidence9'
    ],
    summary: 'summary6',
  },
  complianceDecision: 'NOT_MADE',
  contextDigest: 'context_digest2',
  corpusDigest: 'corpus_digest8',
  currentPolicyApplicability: 'NOT_ESTABLISHED',
  executionEvidence: ExecutionEvidenceEnum.OPERATORLIVERESPONSE,
  externalActionAuthorized: 'False',
  fixtureId: FixtureIdEnum.Payguardfixedsyntheticbriefv1,
  humanReviewRequired: 'True',
  limitations: [
    'limitations1'
  ],
  model: ModelEnum.EnumGemini38flash,
  promptContractDigest: 'prompt_contract_digest8',
  promptContractId: 'payguard-bounded-advisory-v3',
  schemaVersion: '1.0',
  semanticEntailment: 'NOT_EVALUATED',
  stage: StageEnum.DisputeMediation,
  status: 'completed',
  workflowTransitionAuthorized: 'False',
};
```



