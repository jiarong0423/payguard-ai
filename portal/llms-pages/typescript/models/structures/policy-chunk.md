# Policy Chunk

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlBvbGljeUNodW5r

PolicyChunk.


# Interface Name

`PolicyChunk`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseOutcome` | [`PolicyChunkCaseOutcome`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/policy-chunk-case-outcome.md) | Required | This is a container for any-of cases. |
| `caseStage` | [`CaseStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/case-stage.md) | Required | Case stage. |
| `chunkId` | `string` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `materialType` | [`MaterialType1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/material-type-1.md) | Required | Material type. |
| `sourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `textSha256` | `string` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/theme.md) | Required | Theme. |


# Example

```ts
import {
  CaseOutcomeEnum,
  CaseStageEnum,
  MaterialType1Enum,
  PolicyChunk,
  ThemeEnum,
} from 'tradeglot-local-consolelib';

const policyChunk: PolicyChunk = {
  caseOutcome: CaseOutcomeEnum.SETTLEMENTAPPROVALNOTFINALMERITS,
  caseStage: CaseStageEnum.ProceduralOrder,
  chunkId: 'chunk_id8',
  jurisdiction: 'US',
  materialType: MaterialType1Enum.OfficialApiReference,
  sourceId: 'source_id4',
  textSha256: 'text_sha2562',
  theme: ThemeEnum.SourceCompliance,
};
```



