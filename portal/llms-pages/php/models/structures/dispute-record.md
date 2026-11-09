# Dispute Record

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkRpc3B1dGVSZWNvcmQ

DisputeRecord.


# Class Name

`DisputeRecord`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `createTime` | `string` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` | getCreateTime(): string | setCreateTime(string createTime): void |
| `disputeAmount` | [`ProviderMoney`](http://localhost:3000/llms-pages/php/models/structures/provider-money.md) | Required | ProviderMoney. | getDisputeAmount(): ProviderMoney | setDisputeAmount(ProviderMoney disputeAmount): void |
| `disputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` | getDisputeId(): string | setDisputeId(string disputeId): void |
| `disputeLifeCycleStage` | [`string(DisputeLifeCycleStageEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. | getDisputeLifeCycleStage(): string | setDisputeLifeCycleStage(string disputeLifeCycleStage): void |
| `disputeState` | string\|null | Optional | This is a container for any-of cases. | getDisputeState(): ?string | setDisputeState(?string disputeState): void |
| `reason` | [`string(Reason2Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/reason-2.md) | Required | Reason. | getReason(): string | setReason(string reason): void |
| `sellerResponseDueDate` | string\|null | Optional | This is a container for any-of cases. | getSellerResponseDueDate(): ?string | setSellerResponseDueDate(?string sellerResponseDueDate): void |
| `status` | [`string(Status3Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/status-3.md) | Required | Status. | getStatus(): string | setStatus(string status): void |
| `updateTime` | string\|null | Optional | This is a container for any-of cases. | getUpdateTime(): ?string | setUpdateTime(?string updateTime): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\DisputeRecordBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\ProviderMoneyBuilder;
use TradeGlotLocalConsoleLib\Models\DisputeLifeCycleStageEnum;
use TradeGlotLocalConsoleLib\Models\Reason2Enum;
use TradeGlotLocalConsoleLib\Models\Status3Enum;

$disputeRecord = DisputeRecordBuilder::init(
    'create_time0',
    ProviderMoneyBuilder::init(
        'currency_code6',
        'value0'
    )->build(),
    'dispute_id6',
    DisputeLifeCycleStageEnum::ARBITRATION,
    Reason2Enum::MERCHANDISE_OR_SERVICE_NOT_RECEIVED,
    Status3Enum::OPEN
)
    ->disputeState(
        'String7'
    )
    ->sellerResponseDueDate(
        'String3'
    )
    ->updateTime(
        'String7'
    )
    ->build();
```



