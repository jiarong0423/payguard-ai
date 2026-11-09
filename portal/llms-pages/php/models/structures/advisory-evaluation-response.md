# Advisory Evaluation Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkFkdmlzb3J5RXZhbHVhdGlvblJlc3BvbnNl

AdvisoryEvaluationResponse.


# Class Name

`AdvisoryEvaluationResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `pIIQuality` | `string` | Required, Constant | PII quality.<br><br>**Value**: `'NOT_EVALUATED'` | getPIIQuality(): string | setPIIQuality(string pIIQuality): void |
| `advisoryOnly` | `bool` | Required | Advisory only. | getAdvisoryOnly(): bool | setAdvisoryOnly(bool advisoryOnly): void |
| `claimCount` | `int` | Required | Claim count.<br><br>**Constraints**: `>= 1`, `<= 20` | getClaimCount(): int | setClaimCount(int claimCount): void |
| `claimGates` | [`AdvisoryClaimGate[]`](http://localhost:3000/llms-pages/php/models/structures/advisory-claim-gate.md) | Required | Claim gates.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` | getClaimGates(): array | setClaimGates(array claimGates): void |
| `corpusDigest` | `string` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getCorpusDigest(): string | setCorpusDigest(string corpusDigest): void |
| `corpusDigests` | [`ReferenceDigests`](http://localhost:3000/llms-pages/php/models/structures/reference-digests.md) | Required | ReferenceDigests. | getCorpusDigests(): ReferenceDigests | setCorpusDigests(ReferenceDigests corpusDigests): void |
| `corpusId` | `string` | Required, Constant | Corpus id.<br><br>**Value**: `'payguard-us-official-references-v2'` | getCorpusId(): string | setCorpusId(string corpusId): void |
| `coverage` | [`PolicyCoverage`](http://localhost:3000/llms-pages/php/models/structures/policy-coverage.md) | Required | PolicyCoverage. | getCoverage(): PolicyCoverage | setCoverage(PolicyCoverage coverage): void |
| `currentPolicyApplicability` | `string` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` | getCurrentPolicyApplicability(): string | setCurrentPolicyApplicability(string currentPolicyApplicability): void |
| `limitations` | `string[]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` | getLimitations(): array | setLimitations(array limitations): void |
| `modelGeneration` | `string` | Required, Constant | Model generation.<br><br>**Value**: `'NOT_RUN'` | getModelGeneration(): string | setModelGeneration(string modelGeneration): void |
| `naturalLanguageActionAssuranceQuality` | `string` | Required, Constant | Natural language action assurance quality.<br><br>**Value**: `'NOT_EVALUATED'` | getNaturalLanguageActionAssuranceQuality(): string | setNaturalLanguageActionAssuranceQuality(string naturalLanguageActionAssuranceQuality): void |
| `operationalAuthority` | `string` | Required, Constant | Operational authority.<br><br>**Value**: `'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION'` | getOperationalAuthority(): string | setOperationalAuthority(string operationalAuthority): void |
| `promptInjectionQuality` | `string` | Required, Constant | Prompt injection quality.<br><br>**Value**: `'NOT_EVALUATED'` | getPromptInjectionQuality(): string | setPromptInjectionQuality(string promptInjectionQuality): void |
| `requestedContext` | [`PolicyContext`](http://localhost:3000/llms-pages/php/models/structures/policy-context.md) | Required | PolicyContext. | getRequestedContext(): PolicyContext | setRequestedContext(PolicyContext requestedContext): void |
| `requiresHumanReview` | `bool` | Required | Requires human review. | getRequiresHumanReview(): bool | setRequiresHumanReview(bool requiresHumanReview): void |
| `schemaVersion` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` | getSchemaVersion(): int | setSchemaVersion(int schemaVersion): void |
| `semanticEntailment` | `string` | Required, Constant | Semantic entailment.<br><br>**Value**: `'NOT_EVALUATED'` | getSemanticEntailment(): string | setSemanticEntailment(string semanticEntailment): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'offline_structured_gate'` | getSource(): string | setSource(string source): void |
| `status` | [`string(StatusEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/status.md) | Required | Status. | getStatus(): string | setStatus(string status): void |
| `version` | `string` | Required, Constant | Version.<br><br>**Value**: `'payguard.advisory_eval.v1'` | getVersion(): string | setVersion(string version): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AdvisoryEvaluationResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\AdvisoryClaimGateBuilder;
use TradeGlotLocalConsoleLib\Models\ClaimTypeEnum;
use TradeGlotLocalConsoleLib\Models\ReasonCodeEnum;
use TradeGlotLocalConsoleLib\Models\StatusEnum;
use TradeGlotLocalConsoleLib\Models\Builders\ReferenceDigestsBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\PolicyCoverageBuilder;
use TradeGlotLocalConsoleLib\Models\MissingOfficialPolicyThemeEnum;
use TradeGlotLocalConsoleLib\Models\Builders\PolicyThemeCountsBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\PolicyContextBuilder;
use TradeGlotLocalConsoleLib\Models\ThemeEnum;

$advisoryEvaluationResponse = AdvisoryEvaluationResponseBuilder::init(
    false,
    20,
    [
        AdvisoryClaimGateBuilder::init(
            19,
            ClaimTypeEnum::POLICY_REFERENCE,
            [
                ReasonCodeEnum::ASSURANCE_CLAIM_FORBIDDEN,
                ReasonCodeEnum::CITATION_UNKNOWN,
                ReasonCodeEnum::CITATION_REGION_MISMATCH
            ],
            StatusEnum::INCOMPLETE_EVIDENCE,
            [
                'trusted_citation_chunk_ids4',
                'trusted_citation_chunk_ids5'
            ]
        )->build()
    ],
    'corpus_digest4',
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
    [
        'limitations3',
        'limitations4',
        'limitations5'
    ],
    PolicyContextBuilder::init(
        'as_of8',
        14,
        ThemeEnum::DISPUTE_MEDIATION
    )->build(),
    false,
    1,
    StatusEnum::INCOMPLETE_EVIDENCE
)->build();
```



