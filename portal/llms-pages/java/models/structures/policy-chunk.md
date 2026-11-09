# Policy Chunk

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlBvbGljeUNodW5r

PolicyChunk.


# Class Name

`PolicyChunk`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CaseOutcome` | [`PolicyChunkCaseOutcome`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/policy-chunk-case-outcome.md) | Required | This is a container for any-of cases. | PolicyChunkCaseOutcome getCaseOutcome() | setCaseOutcome(PolicyChunkCaseOutcome caseOutcome) |
| `CaseStage` | [`CaseStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/case-stage.md) | Required | Case stage. | CaseStageEnum getCaseStage() | setCaseStage(CaseStageEnum caseStage) |
| `ChunkId` | `String` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` | String getChunkId() | setChunkId(String chunkId) |
| `Jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` | String getJurisdiction() | setJurisdiction(String jurisdiction) |
| `MaterialType` | [`MaterialType1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/material-type-1.md) | Required | Material type. | MaterialType1Enum getMaterialType() | setMaterialType(MaterialType1Enum materialType) |
| `SourceId` | `String` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` | String getSourceId() | setSourceId(String sourceId) |
| `TextSha256` | `String` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getTextSha256() | setTextSha256(String textSha256) |
| `Theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/theme.md) | Required | Theme. | ThemeEnum getTheme() | setTheme(ThemeEnum theme) |


# Example

```java
import m18000.m0.m0.m127.models.CaseOutcomeEnum;
import m18000.m0.m0.m127.models.CaseStageEnum;
import m18000.m0.m0.m127.models.MaterialType1Enum;
import m18000.m0.m0.m127.models.PolicyChunk;
import m18000.m0.m0.m127.models.ThemeEnum;
import m18000.m0.m0.m127.models.containers.PolicyChunkCaseOutcome;

PolicyChunk policyChunk = new PolicyChunk.Builder(
    PolicyChunkCaseOutcome.fromCaseOutcome(
        CaseOutcomeEnum.SETTLEMENT_APPROVAL_NOT_FINAL_MERITS
    ),
    CaseStageEnum.PROCEDURAL_ORDER,
    "chunk_id8",
    "US",
    MaterialType1Enum.OFFICIAL_API_REFERENCE,
    "source_id4",
    "text_sha2562",
    ThemeEnum.SOURCE_COMPLIANCE
)
.build();
```



