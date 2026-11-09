# Policy Chunk

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlBvbGljeUNodW5r

PolicyChunk.


# Class Name

`PolicyChunk`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CaseOutcome` | [`PolicyChunkCaseOutcome`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/policy-chunk-case-outcome.md) | Required | This is a container for any-of cases. |
| `CaseStage` | [`CaseStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/case-stage.md) | Required | Case stage. |
| `ChunkId` | `string` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `Jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `MaterialType` | [`MaterialType1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/material-type-1.md) | Required | Material type. |
| `SourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `TextSha256` | `string` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `Theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/theme.md) | Required | Theme. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

PolicyChunk policyChunk = new PolicyChunk
{
    CaseOutcome = PolicyChunkCaseOutcome.FromCaseOutcome(CaseOutcomeEnum.SETTLEMENTAPPROVALNOTFINALMERITS),
    CaseStage = CaseStageEnum.ProceduralOrder,
    ChunkId = "chunk_id8",
    Jurisdiction = "US",
    MaterialType = MaterialType1Enum.OfficialApiReference,
    SourceId = "source_id4",
    TextSha256 = "text_sha2562",
    Theme = ThemeEnum.SourceCompliance,
};
```



