# Reference Citation

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlJlZmVyZW5jZUNpdGF0aW9u

ReferenceCitation.


# Class Name

`ReferenceCitation`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `caseOutcome` | string([CaseOutcomeEnum](http://localhost:3000/llms-pages/php/models/enumerations/case-outcome.md)) | Required | This is a container for any-of cases. | getCaseOutcome(): string | setCaseOutcome(string caseOutcome): void |
| `caseStage` | [`string(CaseStageEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/case-stage.md) | Required | Case stage. | getCaseStage(): string | setCaseStage(string caseStage): void |
| `chunkId` | `string` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` | getChunkId(): string | setChunkId(string chunkId): void |
| `decisionAcceptanceDeadline` | string | Required | This is a container for any-of cases. | getDecisionAcceptanceDeadline(): string | setDecisionAcceptanceDeadline(string decisionAcceptanceDeadline): void |
| `decisionDate` | string | Required | This is a container for any-of cases. | getDecisionDate(): string | setDecisionDate(string decisionDate): void |
| `decisionDateStatus` | [`string(DecisionDateStatusEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/decision-date-status.md) | Required | Decision date status. | getDecisionDateStatus(): string | setDecisionDateStatus(string decisionDateStatus): void |
| `effectiveDate` | string | Required | This is a container for any-of cases. | getEffectiveDate(): string | setEffectiveDate(string effectiveDate): void |
| `effectiveDateStatus` | [`string(EffectiveDateStatusEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/effective-date-status.md) | Required | Effective date status. | getEffectiveDateStatus(): string | setEffectiveDateStatus(string effectiveDateStatus): void |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` | getJurisdiction(): string | setJurisdiction(string jurisdiction): void |
| `jurisdictionLabel` | `string` | Required | Jurisdiction label.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` | getJurisdictionLabel(): string | setJurisdictionLabel(string jurisdictionLabel): void |
| `locator` | `string` | Required | Locator.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` | getLocator(): string | setLocator(string locator): void |
| `materialType` | [`string(MaterialType1Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/material-type-1.md) | Required | Material type. | getMaterialType(): string | setMaterialType(string materialType): void |
| `relevanceScore` | `int` | Required | Relevance score.<br><br>**Constraints**: `>= 1`, `<= 128` | getRelevanceScore(): int | setRelevanceScore(int relevanceScore): void |
| `retrievedAt` | `string` | Required | Retrieved at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` | getRetrievedAt(): string | setRetrievedAt(string retrievedAt): void |
| `sourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128` | getSourceId(): string | setSourceId(string sourceId): void |
| `sourceTitle` | `string` | Required | Source title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` | getSourceTitle(): string | setSourceTitle(string sourceTitle): void |
| `sourceUpdatedDate` | string | Required | This is a container for any-of cases. | getSourceUpdatedDate(): string | setSourceUpdatedDate(string sourceUpdatedDate): void |
| `sourceUpdatedDateStatus` | [`string(SourceUpdatedDateStatusEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/source-updated-date-status.md) | Required | Source updated date status. | getSourceUpdatedDateStatus(): string | setSourceUpdatedDateStatus(string sourceUpdatedDateStatus): void |
| `text` | `string` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` | getText(): string | setText(string text): void |
| `textSha256` | `string` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getTextSha256(): string | setTextSha256(string textSha256): void |
| `title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` | getTitle(): string | setTitle(string title): void |
| `url` | `string` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` | getUrl(): string | setUrl(string url): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ReferenceCitationBuilder;
use TradeGlotLocalConsoleLib\Models\CaseOutcomeEnum;
use TradeGlotLocalConsoleLib\Models\CaseStageEnum;
use TradeGlotLocalConsoleLib\Models\DecisionDateStatusEnum;
use TradeGlotLocalConsoleLib\Models\EffectiveDateStatusEnum;
use TradeGlotLocalConsoleLib\Models\MaterialType1Enum;
use TradeGlotLocalConsoleLib\Models\SourceUpdatedDateStatusEnum;

$referenceCitation = ReferenceCitationBuilder::init(
    CaseOutcomeEnum::SETTLEMENT_APPROVAL_NOT_FINAL_MERITS,
    CaseStageEnum::PROCEDURAL_ORDER,
    'chunk_id0',
    'String7',
    'String1',
    DecisionDateStatusEnum::NOT_APPLICABLE,
    'String9',
    EffectiveDateStatusEnum::DOCUMENT_STATED,
    'jurisdiction_label6',
    'locator0',
    MaterialType1Enum::OFFICIAL_API_REFERENCE,
    128,
    'retrieved_at2',
    'source_id2',
    'source_title4',
    'String1',
    SourceUpdatedDateStatusEnum::DOCUMENT_STATED,
    'text8',
    'text_sha2566',
    'title4',
    'url2'
)->build();
```



