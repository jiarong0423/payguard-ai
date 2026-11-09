# Reference Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlc3BvbnNl

ReferenceResponse.


# Class Name

`ReferenceResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `advisoryOnly` | `bool` | Required | Advisory only. | getAdvisoryOnly(): bool | setAdvisoryOnly(bool advisoryOnly): void |
| `corpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getCorpusDigest(): string | setCorpusDigest(string corpusDigest): void |
| `corpusDigests` | [`ReferenceDigests`](http://localhost:3000/llms-pages/php/models/structures/reference-digests.md) | Required | ReferenceDigests. | getCorpusDigests(): ReferenceDigests | setCorpusDigests(ReferenceDigests corpusDigests): void |
| `corpusId` | `string` | Required, Constant | Corpus id.<br><br>**Value**: `'payguard-us-official-references-v2'` | getCorpusId(): string | setCorpusId(string corpusId): void |
| `filtersApplied` | [`ReferenceFilters`](http://localhost:3000/llms-pages/php/models/structures/reference-filters.md) | Required | ReferenceFilters. | getFiltersApplied(): ReferenceFilters | setFiltersApplied(ReferenceFilters filtersApplied): void |
| `limitations` | `string[]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` | getLimitations(): array | setLimitations(array limitations): void |
| `operationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION'` | getOperationalAuthority(): string | setOperationalAuthority(string operationalAuthority): void |
| `results` | [`ReferenceCitation[]`](http://localhost:3000/llms-pages/php/models/structures/reference-citation.md) | Required | Results.<br><br>**Constraints**: *Maximum Items*: `10` | getResults(): array | setResults(array results): void |
| `schemaVersion` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` | getSchemaVersion(): int | setSchemaVersion(int schemaVersion): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'public_reference'` | getSource(): string | setSource(string source): void |
| `status` | [`string(Status13Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/status-13.md) | Required | Status. | getStatus(): string | setStatus(string status): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ReferenceResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\ReferenceDigestsBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\ReferenceFiltersBuilder;
use TradeGlotLocalConsoleLib\Models\CaseStage2Enum;
use TradeGlotLocalConsoleLib\Models\MaterialType4Enum;
use TradeGlotLocalConsoleLib\Models\ThemeEnum;
use TradeGlotLocalConsoleLib\Models\Builders\ReferenceCitationBuilder;
use TradeGlotLocalConsoleLib\Models\CaseOutcomeEnum;
use TradeGlotLocalConsoleLib\Models\CaseStageEnum;
use TradeGlotLocalConsoleLib\Models\DecisionDateStatusEnum;
use TradeGlotLocalConsoleLib\Models\EffectiveDateStatusEnum;
use TradeGlotLocalConsoleLib\Models\MaterialType1Enum;
use TradeGlotLocalConsoleLib\Models\SourceUpdatedDateStatusEnum;
use TradeGlotLocalConsoleLib\Models\Status13Enum;

$referenceResponse = ReferenceResponseBuilder::init(
    false,
    'corpus_digest2',
    ReferenceDigestsBuilder::init(
        'chunks_sha2564',
        'sources_sha2562'
    )->build(),
    ReferenceFiltersBuilder::init(
        'String1',
        CaseStage2Enum::PROCEDURAL_ORDER,
        10,
        [
            MaterialType4Enum::OFFICIAL_POLICY,
            MaterialType4Enum::PUBLIC_COURT_ORDER_COPY
        ],
        28,
        false,
        ThemeEnum::DISPUTE_MEDIATION
    )->build(),
    [
        'limitations5',
        'limitations6'
    ],
    [
        ReferenceCitationBuilder::init(
            CaseOutcomeEnum::SETTLEMENT_APPROVAL_NOT_FINAL_MERITS,
            CaseStageEnum::PROCEDURAL_ORDER,
            'chunk_id2',
            'String5',
            'String9',
            DecisionDateStatusEnum::NOT_APPLICABLE,
            'String5',
            EffectiveDateStatusEnum::DOCUMENT_STATED,
            'jurisdiction_label4',
            'locator8',
            MaterialType1Enum::OFFICIAL_API_REFERENCE,
            128,
            'retrieved_at0',
            'source_id0',
            'source_title8',
            'String9',
            SourceUpdatedDateStatusEnum::DOCUMENT_STATED,
            'text4',
            'text_sha2566',
            'title8',
            'url0'
        )->build()
    ],
    1,
    Status13Enum::REFERENCES_FOUND
)->build();
```



