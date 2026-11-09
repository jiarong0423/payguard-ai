# Policy Source

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlBvbGljeVNvdXJjZQ

PolicySource.


# Interface Name

`PolicySource`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `citationChunkIds` | `string[]` | Required | Citation chunk ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `29`, *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `contentClass` | `string` | Required, Constant | Content class.<br><br>**Value**: `'public_reference_summary'` |
| `currentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` |
| `decisionAcceptanceDeadline` | [`PolicySourceDecisionAcceptanceDeadline`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/policy-source-decision-acceptance-deadline.md) | Required | This is a container for any-of cases. |
| `decisionDate` | [`PolicySourceDecisionDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/policy-source-decision-date.md) | Required | This is a container for any-of cases. |
| `decisionDateStatus` | [`DecisionDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/decision-date-status.md) | Required | Decision date status. |
| `effectiveDate` | [`PolicySourceEffectiveDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/policy-source-effective-date.md) | Required | This is a container for any-of cases. |
| `effectiveDateStatus` | [`EffectiveDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/effective-date-status.md) | Required | Effective date status. |
| `jurisdiction` | `string` | Required | Jurisdiction.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `jurisdictionNormalized` | `string` | Required, Constant | Jurisdiction normalized.<br><br>**Value**: `'US'` |
| `materialType` | [`MaterialType1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/material-type-1.md) | Required | Material type. |
| `observationAgeBasis` | `string` | Required, Constant | Observation age basis.<br><br>**Value**: `'saved_retrieved_at_exact_elapsed_time'` |
| `observationStatus` | [`ObservationStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/observation-status.md) | Required | Observation status. |
| `reasonCodes` | [`ReasonCode1Enum[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` |
| `representation` | `string` | Required, Constant | Representation.<br><br>**Value**: `'authored_paraphrase_not_full_source'` |
| `retrievedAt` | `string` | Required | Retrieved at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `sourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `sourceUpdatedDate` | [`PolicySourceSourceUpdatedDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/policy-source-source-updated-date.md) | Required | This is a container for any-of cases. |
| `sourceUpdatedDateStatus` | [`SourceUpdatedDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/source-updated-date-status.md) | Required | Source updated date status. |
| `title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `url` | `string` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```ts
import {
  DecisionDateStatusEnum,
  EffectiveDateStatusEnum,
  MaterialType1Enum,
  ObservationStatusEnum,
  PolicySource,
  ReasonCode1Enum,
  SourceUpdatedDateStatusEnum,
} from 'tradeglot-local-consolelib';

const policySource: PolicySource = {
  citationChunkIds: [
    'citation_chunk_ids4'
  ],
  contentClass: 'public_reference_summary',
  currentPolicyApplicability: 'NOT_ESTABLISHED',
  decisionAcceptanceDeadline: 'String7',
  decisionDate: 'String1',
  decisionDateStatus: DecisionDateStatusEnum.NOTAPPLICABLE,
  effectiveDate: 'String3',
  effectiveDateStatus: EffectiveDateStatusEnum.DOCUMENTSTATED,
  jurisdiction: 'jurisdiction2',
  jurisdictionNormalized: 'US',
  materialType: MaterialType1Enum.OfficialApiReference,
  observationAgeBasis: 'saved_retrieved_at_exact_elapsed_time',
  observationStatus: ObservationStatusEnum.STALEOBSERVATION,
  reasonCodes: [
    ReasonCode1Enum.STALEOBSERVATION
  ],
  representation: 'authored_paraphrase_not_full_source',
  retrievedAt: 'retrieved_at2',
  sourceId: 'source_id2',
  sourceUpdatedDate: 'String1',
  sourceUpdatedDateStatus: SourceUpdatedDateStatusEnum.DOCUMENTSTATED,
  title: 'title6',
  url: 'url2',
};
```



