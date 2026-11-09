# Dispute Draft Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNl

DisputeDraftResponse.


# Class Name

`DisputeDraftResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` | getAdvisoryOnly(): string | setAdvisoryOnly(string advisoryOnly): void |
| `caseRef` | `string` | Required | Case ref. | getCaseRef(): string | setCaseRef(string caseRef): void |
| `documentRedaction` | [`DocumentRedaction`](http://localhost:3000/llms-pages/php/models/structures/document-redaction.md) | Required | DocumentRedaction. | getDocumentRedaction(): DocumentRedaction | setDocumentRedaction(DocumentRedaction documentRedaction): void |
| `draftDigest` | `string` | Required | Draft digest. | getDraftDigest(): string | setDraftDigest(string draftDigest): void |
| `evidence` | [`Evidence`](http://localhost:3000/llms-pages/php/models/structures/evidence.md) | Required | Evidence. | getEvidence(): Evidence | setEvidence(Evidence evidence): void |
| `identityRedaction` | [`IdentityRedaction`](http://localhost:3000/llms-pages/php/models/structures/identity-redaction.md) | Required | IdentityRedaction. | getIdentityRedaction(): IdentityRedaction | setIdentityRedaction(IdentityRedaction identityRedaction): void |
| `limitations` | `string[]` | Required | Limitations. | getLimitations(): array | setLimitations(array limitations): void |
| `policyVersion` | `string` | Required | Policy version. | getPolicyVersion(): string | setPolicyVersion(string policyVersion): void |
| `recommendation` | `string` | Required | Recommendation. | getRecommendation(): string | setRecommendation(string recommendation): void |
| `restrictedOriginalSummary` | [`RestrictedOriginalSummary`](http://localhost:3000/llms-pages/php/models/structures/restricted-original-summary.md) | Required | RestrictedOriginalSummary. | getRestrictedOriginalSummary(): RestrictedOriginalSummary | setRestrictedOriginalSummary(RestrictedOriginalSummary restrictedOriginalSummary): void |
| `reviewReasons` | `string[]` | Required | Review reasons. | getReviewReasons(): array | setReviewReasons(array reviewReasons): void |
| `routing` | [`DisputeRouting`](http://localhost:3000/llms-pages/php/models/structures/dispute-routing.md) | Required | DisputeRouting. | getRouting(): DisputeRouting | setRouting(DisputeRouting routing): void |
| `scenarioMatch` | [`ScenarioMatch`](http://localhost:3000/llms-pages/php/models/structures/scenario-match.md) | Required | ScenarioMatch. | getScenarioMatch(): ScenarioMatch | setScenarioMatch(ScenarioMatch scenarioMatch): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` | getSource(): string | setSource(string source): void |
| `status` | [`string(Status5Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/status-5.md) | Required | Status. | getStatus(): string | setStatus(string status): void |
| `timeEvidence` | [TimeEvidence](http://localhost:3000/llms-pages/php/models/structures/time-evidence.md)\|null | Optional | This is a container for any-of cases. | getTimeEvidence(): ?TimeEvidence | setTimeEvidence(?TimeEvidence timeEvidence): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\DisputeDraftResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\DocumentRedactionBuilder;
use TradeGlotLocalConsoleLib\Models\TypeEnum;
use TradeGlotLocalConsoleLib\Models\Builders\EvidenceBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\IdentityRedactionBuilder;
use TradeGlotLocalConsoleLib\Models\FieldEnum;
use TradeGlotLocalConsoleLib\Models\Builders\IdentityTokensBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\RestrictedOriginalSummaryBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\DisputeRoutingBuilder;
use TradeGlotLocalConsoleLib\Models\DisputeLifeCycleStageEnum;
use TradeGlotLocalConsoleLib\Models\DueStateEnum;
use TradeGlotLocalConsoleLib\Models\OverallStateEnum;
use TradeGlotLocalConsoleLib\Models\Reason2Enum;
use TradeGlotLocalConsoleLib\Models\Builders\DisputeRequirementBuilder;
use TradeGlotLocalConsoleLib\Models\RequirementStateEnum;
use TradeGlotLocalConsoleLib\Models\Status3Enum;
use TradeGlotLocalConsoleLib\Models\Builders\ScenarioMatchBuilder;
use TradeGlotLocalConsoleLib\Models\IntakeStatusEnum;
use TradeGlotLocalConsoleLib\Models\Builders\DisputeScenarioBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\ScenarioCitationBuilder;
use TradeGlotLocalConsoleLib\Models\MaterialTypeEnum;
use TradeGlotLocalConsoleLib\Models\Status5Enum;
use TradeGlotLocalConsoleLib\Models\Builders\TimeEvidenceBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\MessageTimeEventBuilder;
use TradeGlotLocalConsoleLib\Models\ChannelEnum;
use TradeGlotLocalConsoleLib\Models\DirectionEnum;
use TradeGlotLocalConsoleLib\Models\TopicEnum;
use TradeGlotLocalConsoleLib\Models\FlagEnum;
use TradeGlotLocalConsoleLib\Models\Builders\TimeGapsBuilder;

$disputeDraftResponse = DisputeDraftResponseBuilder::init(
    'case_ref8',
    DocumentRedactionBuilder::init(
        [
            'key0' => 128
        ],
        [
            'limitations9',
            'limitations8',
            'limitations7'
        ],
        'redacted_text8',
        128,
        [
            TypeEnum::MANUAL
        ]
    )->build(),
    'draft_digest4',
    EvidenceBuilder::init()
        ->carrierStatus(
            'String5'
        )
        ->deliveredAt(
            'String1'
        )
        ->openedAt(
            'String1'
        )
        ->orderCreatedAt(
            'String3'
        )
        ->reason(
            'String3'
        )
        ->build(),
    IdentityRedactionBuilder::init(
        [
            FieldEnum::ADDRESS,
            FieldEnum::EMAIL,
            FieldEnum::NAME
        ],
        IdentityTokensBuilder::init(
            'address_token0',
            'email_token2',
            'name_token0'
        )->build()
    )->build(),
    [
        'limitations1'
    ],
    'policy_version2',
    'recommendation0',
    RestrictedOriginalSummaryBuilder::init(
        20,
        96
    )->build(),
    [
        'review_reasons3',
        'review_reasons4',
        'review_reasons5'
    ],
    DisputeRoutingBuilder::init(
        [
            'available_actions6'
        ],
        DisputeLifeCycleStageEnum::INQUIRY,
        DueStateEnum::OPEN,
        OverallStateEnum::NEEDS_INPUT,
        Reason2Enum::OTHER,
        [
            DisputeRequirementBuilder::init(
                20,
                false,
                60,
                'provider_evidence_type0',
                'request_id8',
                RequirementStateEnum::CONTEXT_ONLY,
                'source2'
            )
                ->action(
                    'String5'
                )
                ->evidenceType(
                    'String3'
                )
                ->build()
        ],
        'seller_response_due_date4',
        Status3Enum::WAITING_FOR_SELLER_RESPONSE
    )->build(),
    ScenarioMatchBuilder::init(
        IntakeStatusEnum::READY_FOR_LOCAL_RULES,
        DisputeScenarioBuilder::init(
            [
                ScenarioCitationBuilder::init(
                    'chunk_id0',
                    'locator0',
                    MaterialTypeEnum::OFFICIAL_API_REFERENCE,
                    'source_id2',
                    'text_sha2564',
                    'title4',
                    'url2'
                )->build()
            ],
            [
                'limitations3'
            ]
        )->build()
    )->build(),
    Status5Enum::MANUAL_REVIEW
)
    ->timeEvidence(
        TimeEvidenceBuilder::init(
            [
                MessageTimeEventBuilder::init(
                    'at4',
                    ChannelEnum::EMAIL,
                    DirectionEnum::INBOUND,
                    'message_digest2',
                    TopicEnum::ORDER_DETAILS_PROVIDED
                )->build()
            ],
            [
                FlagEnum::ORDER_RECORD_ABSENT,
                FlagEnum::DELIVERY_NOT_RECORDED,
                FlagEnum::DELIVERY_AFTER_CLAIM
            ],
            TimeGapsBuilder::init(
                210,
                154,
                192,
                208
            )->build()
        )->build()
    )->build();
```



