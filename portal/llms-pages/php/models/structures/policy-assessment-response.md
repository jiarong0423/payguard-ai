# Policy Assessment Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlBvbGljeUFzc2Vzc21lbnRSZXNwb25zZQ

PolicyAssessmentResponse.


# Class Name

`PolicyAssessmentResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `advisoryOnly` | `bool` | Required | Advisory only. | getAdvisoryOnly(): bool | setAdvisoryOnly(bool advisoryOnly): void |
| `chunks` | [`PolicyChunk[]`](http://localhost:3000/llms-pages/php/models/structures/policy-chunk.md) | Required | Chunks.<br><br>**Constraints**: *Maximum Items*: `29` | getChunks(): array | setChunks(array chunks): void |
| `corpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getCorpusDigest(): string | setCorpusDigest(string corpusDigest): void |
| `corpusDigests` | [`ReferenceDigests`](http://localhost:3000/llms-pages/php/models/structures/reference-digests.md) | Required | ReferenceDigests. | getCorpusDigests(): ReferenceDigests | setCorpusDigests(ReferenceDigests corpusDigests): void |
| `corpusId` | `string` | Required, Constant | Corpus id.<br><br>**Value**: `'payguard-us-official-references-v2'` | getCorpusId(): string | setCorpusId(string corpusId): void |
| `coverage` | [`PolicyCoverage`](http://localhost:3000/llms-pages/php/models/structures/policy-coverage.md) | Required | PolicyCoverage. | getCoverage(): PolicyCoverage | setCoverage(PolicyCoverage coverage): void |
| `currentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` | getCurrentPolicyApplicability(): string | setCurrentPolicyApplicability(string currentPolicyApplicability): void |
| `filtersApplied` | [`PolicyContext`](http://localhost:3000/llms-pages/php/models/structures/policy-context.md) | Required | PolicyContext. | getFiltersApplied(): PolicyContext | setFiltersApplied(PolicyContext filtersApplied): void |
| `limitations` | `string[]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` | getLimitations(): array | setLimitations(array limitations): void |
| `operationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION'` | getOperationalAuthority(): string | setOperationalAuthority(string operationalAuthority): void |
| `reasonCodes` | [`string(ReasonCode1Enum)[]`](http://localhost:3000/llms-pages/php/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` | getReasonCodes(): array | setReasonCodes(array reasonCodes): void |
| `requiresHumanReview` | `bool` | Required | Requires human review. | getRequiresHumanReview(): bool | setRequiresHumanReview(bool requiresHumanReview): void |
| `schemaVersion` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` | getSchemaVersion(): int | setSchemaVersion(int schemaVersion): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'public_reference'` | getSource(): string | setSource(string source): void |
| `sources` | [`PolicySource[]`](http://localhost:3000/llms-pages/php/models/structures/policy-source.md) | Required | Sources.<br><br>**Constraints**: *Maximum Items*: `16` | getSources(): array | setSources(array sources): void |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'INCOMPLETE_POLICY_EVIDENCE'` | getStatus(): string | setStatus(string status): void |
| `version` | `string` | Required, Constant | Version.<br><br>**Value**: `'payguard.applicability.v1'` | getVersion(): string | setVersion(string version): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\PolicyAssessmentResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\PolicyChunkBuilder;
use TradeGlotLocalConsoleLib\Models\CaseOutcomeEnum;
use TradeGlotLocalConsoleLib\Models\CaseStageEnum;
use TradeGlotLocalConsoleLib\Models\MaterialType1Enum;
use TradeGlotLocalConsoleLib\Models\ThemeEnum;
use TradeGlotLocalConsoleLib\Models\Builders\ReferenceDigestsBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\PolicyCoverageBuilder;
use TradeGlotLocalConsoleLib\Models\MissingOfficialPolicyThemeEnum;
use TradeGlotLocalConsoleLib\Models\Builders\PolicyThemeCountsBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\PolicyContextBuilder;
use TradeGlotLocalConsoleLib\Models\ReasonCode1Enum;
use TradeGlotLocalConsoleLib\Models\Builders\PolicySourceBuilder;
use TradeGlotLocalConsoleLib\Models\DecisionDateStatusEnum;
use TradeGlotLocalConsoleLib\Models\EffectiveDateStatusEnum;
use TradeGlotLocalConsoleLib\Models\ObservationStatusEnum;
use TradeGlotLocalConsoleLib\Models\SourceUpdatedDateStatusEnum;

$policyAssessmentResponse = PolicyAssessmentResponseBuilder::init(
    false,
    [
        PolicyChunkBuilder::init(
            CaseOutcomeEnum::SETTLEMENT_APPROVAL_NOT_FINAL_MERITS,
            CaseStageEnum::PROCEDURAL_ORDER,
            'chunk_id6',
            MaterialType1Enum::OFFICIAL_POLICY,
            'source_id6',
            'text_sha2560',
            ThemeEnum::VELOCITY_GUARD
        )->build()
    ],
    'corpus_digest2',
    ReferenceDigestsBuilder::init(
        'chunks_sha2564',
        'sources_sha2562'
    )->build(),
    PolicyCoverageBuilder::init(
        false,
        [
            MissingOfficialPolicyThemeEnum::SOURCE_COMPLIANCE
        ],
        PolicyThemeCountsBuilder::init(
            12,
            29,
            29
        )->build(),
        [
            'official_policy_source_ids0'
        ],
        16,
        29,
        16
    )->build(),
    PolicyContextBuilder::init(
        'as_of0',
        28,
        ThemeEnum::DISPUTE_MEDIATION
    )->build(),
    [
        'limitations5',
        'limitations4',
        'limitations3'
    ],
    [
        ReasonCode1Enum::CURRENT_POLICY_APPLICABILITY_NOT_ESTABLISHED,
        ReasonCode1Enum::FUTURE_OBSERVATION
    ],
    false,
    1,
    [
        PolicySourceBuilder::init(
            [
                'citation_chunk_ids2',
                'citation_chunk_ids3'
            ],
            'String5',
            'String9',
            DecisionDateStatusEnum::DOCUMENT_STATED,
            'String7',
            EffectiveDateStatusEnum::DOCUMENT_STATED,
            'jurisdiction0',
            MaterialType1Enum::PUBLIC_COURT_ORDER_COPY,
            ObservationStatusEnum::FUTURE_OBSERVATION,
            [
                ReasonCode1Enum::CURRENT_POLICY_APPLICABILITY_NOT_ESTABLISHED,
                ReasonCode1Enum::FUTURE_OBSERVATION
            ],
            'retrieved_at0',
            'source_id0',
            'String9',
            SourceUpdatedDateStatusEnum::DOCUMENT_STATED,
            'title2',
            'url0'
        )->build()
    ]
)->build();
```



