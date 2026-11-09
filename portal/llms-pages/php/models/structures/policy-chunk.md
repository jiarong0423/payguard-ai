# Policy Chunk

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlBvbGljeUNodW5r

PolicyChunk.


# Class Name

`PolicyChunk`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `caseOutcome` | string([CaseOutcomeEnum](http://localhost:3000/llms-pages/php/models/enumerations/case-outcome.md)) | Required | This is a container for any-of cases. | getCaseOutcome(): string | setCaseOutcome(string caseOutcome): void |
| `caseStage` | [`string(CaseStageEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/case-stage.md) | Required | Case stage. | getCaseStage(): string | setCaseStage(string caseStage): void |
| `chunkId` | `string` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` | getChunkId(): string | setChunkId(string chunkId): void |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` | getJurisdiction(): string | setJurisdiction(string jurisdiction): void |
| `materialType` | [`string(MaterialType1Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/material-type-1.md) | Required | Material type. | getMaterialType(): string | setMaterialType(string materialType): void |
| `sourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` | getSourceId(): string | setSourceId(string sourceId): void |
| `textSha256` | `string` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getTextSha256(): string | setTextSha256(string textSha256): void |
| `theme` | [`string(ThemeEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/theme.md) | Required | Theme. | getTheme(): string | setTheme(string theme): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\PolicyChunkBuilder;
use TradeGlotLocalConsoleLib\Models\CaseOutcomeEnum;
use TradeGlotLocalConsoleLib\Models\CaseStageEnum;
use TradeGlotLocalConsoleLib\Models\MaterialType1Enum;
use TradeGlotLocalConsoleLib\Models\ThemeEnum;

$policyChunk = PolicyChunkBuilder::init(
    CaseOutcomeEnum::SETTLEMENT_APPROVAL_NOT_FINAL_MERITS,
    CaseStageEnum::PROCEDURAL_ORDER,
    'chunk_id8',
    MaterialType1Enum::OFFICIAL_API_REFERENCE,
    'source_id4',
    'text_sha2562',
    ThemeEnum::SOURCE_COMPLIANCE
)->build();
```



