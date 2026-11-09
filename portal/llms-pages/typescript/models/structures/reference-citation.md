# Reference Citation

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlJlZmVyZW5jZUNpdGF0aW9u

ReferenceCitation.


# Interface Name

`ReferenceCitation`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseOutcome` | [`ReferenceCitationCaseOutcome`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/reference-citation-case-outcome.md) | Required | This is a container for any-of cases. |
| `caseStage` | [`CaseStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/case-stage.md) | Required | Case stage. |
| `chunkId` | `string` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `decisionAcceptanceDeadline` | [`ReferenceCitationDecisionAcceptanceDeadline`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/reference-citation-decision-acceptance-deadline.md) | Required | This is a container for any-of cases. |
| `decisionDate` | [`ReferenceCitationDecisionDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/reference-citation-decision-date.md) | Required | This is a container for any-of cases. |
| `decisionDateStatus` | [`DecisionDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/decision-date-status.md) | Required | Decision date status. |
| `effectiveDate` | [`ReferenceCitationEffectiveDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/reference-citation-effective-date.md) | Required | This is a container for any-of cases. |
| `effectiveDateStatus` | [`EffectiveDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/effective-date-status.md) | Required | Effective date status. |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `jurisdictionLabel` | `string` | Required | Jurisdiction label.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `locator` | `string` | Required | Locator.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `materialType` | [`MaterialType1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/material-type-1.md) | Required | Material type. |
| `relevanceScore` | `number` | Required | Relevance score.<br><br>**Constraints**: `>= 1`, `<= 128` |
| `retrievedAt` | `string` | Required | Retrieved at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `sourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128` |
| `sourceTitle` | `string` | Required | Source title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `sourceUpdatedDate` | [`ReferenceCitationSourceUpdatedDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/reference-citation-source-updated-date.md) | Required | This is a container for any-of cases. |
| `sourceUpdatedDateStatus` | [`SourceUpdatedDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/source-updated-date-status.md) | Required | Source updated date status. |
| `text` | `string` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `textSha256` | `string` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `url` | `string` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```ts
import {
  CaseOutcomeEnum,
  CaseStageEnum,
  DecisionDateStatusEnum,
  EffectiveDateStatusEnum,
  MaterialType1Enum,
  ReferenceCitation,
  SourceUpdatedDateStatusEnum,
} from 'tradeglot-local-consolelib';

const referenceCitation: ReferenceCitation = {
  caseOutcome: CaseOutcomeEnum.SETTLEMENTAPPROVALNOTFINALMERITS,
  caseStage: CaseStageEnum.ProceduralOrder,
  chunkId: 'chunk_id0',
  decisionAcceptanceDeadline: 'String7',
  decisionDate: 'String1',
  decisionDateStatus: DecisionDateStatusEnum.NOTAPPLICABLE,
  effectiveDate: 'String9',
  effectiveDateStatus: EffectiveDateStatusEnum.DOCUMENTSTATED,
  jurisdiction: 'US',
  jurisdictionLabel: 'jurisdiction_label6',
  locator: 'locator0',
  materialType: MaterialType1Enum.OfficialApiReference,
  relevanceScore: 128,
  retrievedAt: 'retrieved_at2',
  sourceId: 'source_id2',
  sourceTitle: 'source_title4',
  sourceUpdatedDate: 'String1',
  sourceUpdatedDateStatus: SourceUpdatedDateStatusEnum.DOCUMENTSTATED,
  text: 'text8',
  textSha256: 'text_sha2566',
  title: 'title4',
  url: 'url2',
};
```



