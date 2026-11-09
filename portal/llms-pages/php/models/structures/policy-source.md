# Policy Source

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlBvbGljeVNvdXJjZQ

PolicySource.


# Class Name

`PolicySource`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `citationChunkIds` | `string[]` | Required | Citation chunk ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `29`, *Pattern*: `^[A-Z0-9-]{1,128}$` | getCitationChunkIds(): array | setCitationChunkIds(array citationChunkIds): void |
| `contentClass` | `string` | Required, Constant | Content class.<br><br>**Value**: `'public_reference_summary'` | getContentClass(): string | setContentClass(string contentClass): void |
| `currentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` | getCurrentPolicyApplicability(): string | setCurrentPolicyApplicability(string currentPolicyApplicability): void |
| `decisionAcceptanceDeadline` | string | Required | This is a container for any-of cases. | getDecisionAcceptanceDeadline(): string | setDecisionAcceptanceDeadline(string decisionAcceptanceDeadline): void |
| `decisionDate` | string | Required | This is a container for any-of cases. | getDecisionDate(): string | setDecisionDate(string decisionDate): void |
| `decisionDateStatus` | [`string(DecisionDateStatusEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/decision-date-status.md) | Required | Decision date status. | getDecisionDateStatus(): string | setDecisionDateStatus(string decisionDateStatus): void |
| `effectiveDate` | string | Required | This is a container for any-of cases. | getEffectiveDate(): string | setEffectiveDate(string effectiveDate): void |
| `effectiveDateStatus` | [`string(EffectiveDateStatusEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/effective-date-status.md) | Required | Effective date status. | getEffectiveDateStatus(): string | setEffectiveDateStatus(string effectiveDateStatus): void |
| `jurisdiction` | `string` | Required | Jurisdiction.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` | getJurisdiction(): string | setJurisdiction(string jurisdiction): void |
| `jurisdictionNormalized` | `string` | Required, Constant | Jurisdiction normalized.<br><br>**Value**: `'US'` | getJurisdictionNormalized(): string | setJurisdictionNormalized(string jurisdictionNormalized): void |
| `materialType` | [`string(MaterialType1Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/material-type-1.md) | Required | Material type. | getMaterialType(): string | setMaterialType(string materialType): void |
| `observationAgeBasis` | `string` | Required, Constant | Observation age basis.<br><br>**Value**: `'saved_retrieved_at_exact_elapsed_time'` | getObservationAgeBasis(): string | setObservationAgeBasis(string observationAgeBasis): void |
| `observationStatus` | [`string(ObservationStatusEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/observation-status.md) | Required | Observation status. | getObservationStatus(): string | setObservationStatus(string observationStatus): void |
| `reasonCodes` | [`string(ReasonCode1Enum)[]`](http://localhost:3000/llms-pages/php/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` | getReasonCodes(): array | setReasonCodes(array reasonCodes): void |
| `representation` | `string` | Required, Constant | Representation.<br><br>**Value**: `'authored_paraphrase_not_full_source'` | getRepresentation(): string | setRepresentation(string representation): void |
| `retrievedAt` | `string` | Required | Retrieved at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` | getRetrievedAt(): string | setRetrievedAt(string retrievedAt): void |
| `sourceId` | `string` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` | getSourceId(): string | setSourceId(string sourceId): void |
| `sourceUpdatedDate` | string | Required | This is a container for any-of cases. | getSourceUpdatedDate(): string | setSourceUpdatedDate(string sourceUpdatedDate): void |
| `sourceUpdatedDateStatus` | [`string(SourceUpdatedDateStatusEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/source-updated-date-status.md) | Required | Source updated date status. | getSourceUpdatedDateStatus(): string | setSourceUpdatedDateStatus(string sourceUpdatedDateStatus): void |
| `title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` | getTitle(): string | setTitle(string title): void |
| `url` | `string` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` | getUrl(): string | setUrl(string url): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\PolicySourceBuilder;
use TradeGlotLocalConsoleLib\Models\DecisionDateStatusEnum;
use TradeGlotLocalConsoleLib\Models\EffectiveDateStatusEnum;
use TradeGlotLocalConsoleLib\Models\MaterialType1Enum;
use TradeGlotLocalConsoleLib\Models\ObservationStatusEnum;
use TradeGlotLocalConsoleLib\Models\ReasonCode1Enum;
use TradeGlotLocalConsoleLib\Models\SourceUpdatedDateStatusEnum;

$policySource = PolicySourceBuilder::init(
    [
        'citation_chunk_ids4'
    ],
    'String7',
    'String1',
    DecisionDateStatusEnum::NOT_APPLICABLE,
    'String3',
    EffectiveDateStatusEnum::DOCUMENT_STATED,
    'jurisdiction2',
    MaterialType1Enum::OFFICIAL_API_REFERENCE,
    ObservationStatusEnum::STALE_OBSERVATION,
    [
        ReasonCode1Enum::STALE_OBSERVATION
    ],
    'retrieved_at2',
    'source_id2',
    'String1',
    SourceUpdatedDateStatusEnum::DOCUMENT_STATED,
    'title6',
    'url2'
)->build();
```



