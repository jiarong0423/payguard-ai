# Dispute Routing

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkRpc3B1dGVSb3V0aW5n

DisputeRouting.


# Class Name

`DisputeRouting`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `availableActions` | `string[]` | Required | Available actions.<br><br>**Constraints**: *Maximum Items*: `20` | getAvailableActions(): array | setAvailableActions(array availableActions): void |
| `disputeLifeCycleStage` | [`string(DisputeLifeCycleStageEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. | getDisputeLifeCycleStage(): string | setDisputeLifeCycleStage(string disputeLifeCycleStage): void |
| `dueState` | [`string(DueStateEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/due-state.md) | Required | Due state. | getDueState(): string | setDueState(string dueState): void |
| `humanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `'True'` | getHumanReviewRequired(): string | setHumanReviewRequired(string humanReviewRequired): void |
| `overallState` | [`string(OverallStateEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/overall-state.md) | Required | Overall state. | getOverallState(): string | setOverallState(string overallState): void |
| `providerSubmission` | `string` | Required, Constant | Provider submission.<br><br>**Value**: `'NOT_PERFORMED'` | getProviderSubmission(): string | setProviderSubmission(string providerSubmission): void |
| `reason` | [`string(Reason2Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/reason-2.md) | Required | Reason. | getReason(): string | setReason(string reason): void |
| `requirements` | [`DisputeRequirement[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/dispute-requirement.md) | Required | Requirements.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` | getRequirements(): array | setRequirements(array requirements): void |
| `schemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` | getSchemaVersion(): int | setSchemaVersion(int schemaVersion): void |
| `sellerResponseDueDate` | `string` | Required | Seller response due date.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` | getSellerResponseDueDate(): string | setSellerResponseDueDate(string sellerResponseDueDate): void |
| `snapshotClass` | `string` | Required, Constant | Snapshot class.<br><br>**Value**: `'SYNTHETIC_PROVIDER_FIXTURE'` | getSnapshotClass(): string | setSnapshotClass(string snapshotClass): void |
| `status` | [`string(Status3Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/status-3.md) | Required | Status. | getStatus(): string | setStatus(string status): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\DisputeRoutingBuilder;
use TradeGlotLocalConsoleLib\Models\DisputeLifeCycleStageEnum;
use TradeGlotLocalConsoleLib\Models\DueStateEnum;
use TradeGlotLocalConsoleLib\Models\OverallStateEnum;
use TradeGlotLocalConsoleLib\Models\Reason2Enum;
use TradeGlotLocalConsoleLib\Models\Builders\DisputeRequirementBuilder;
use TradeGlotLocalConsoleLib\Models\RequirementStateEnum;
use TradeGlotLocalConsoleLib\Models\Status3Enum;

$disputeRouting = DisputeRoutingBuilder::init(
    [
        'available_actions4',
        'available_actions5'
    ],
    DisputeLifeCycleStageEnum::ARBITRATION,
    DueStateEnum::OPEN,
    OverallStateEnum::DUE_DATE_EXPIRED,
    Reason2Enum::UNAUTHORISED,
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
    'seller_response_due_date2',
    Status3Enum::WAITING_FOR_SELLER_RESPONSE
)->build();
```



