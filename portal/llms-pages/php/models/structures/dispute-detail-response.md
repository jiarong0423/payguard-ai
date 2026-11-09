# Dispute Detail Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkRpc3B1dGVEZXRhaWxSZXNwb25zZQ

DisputeDetailResponse.


# Class Name

`DisputeDetailResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `createTime` | `string` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` | getCreateTime(): string | setCreateTime(string createTime): void |
| `dataSourceLabel` | [`string(DataSourceLabelEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/data-source-label.md) | Required | Data source label. | getDataSourceLabel(): string | setDataSourceLabel(string dataSourceLabel): void |
| `disputeAmount` | [`ProviderMoney`](http://localhost:3000/llms-pages/php/models/structures/provider-money.md) | Required | ProviderMoney. | getDisputeAmount(): ProviderMoney | setDisputeAmount(ProviderMoney disputeAmount): void |
| `disputeChannel` | string\|null | Optional | This is a container for any-of cases. | getDisputeChannel(): ?string | setDisputeChannel(?string disputeChannel): void |
| `disputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` | getDisputeId(): string | setDisputeId(string disputeId): void |
| `disputeLifeCycleStage` | [`string(DisputeLifeCycleStageEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. | getDisputeLifeCycleStage(): string | setDisputeLifeCycleStage(string disputeLifeCycleStage): void |
| `disputeState` | string\|null | Optional | This is a container for any-of cases. | getDisputeState(): ?string | setDisputeState(?string disputeState): void |
| `disputedTransactions` | [`DisputedTransaction[]`](http://localhost:3000/llms-pages/php/models/structures/disputed-transaction.md) | Required | Disputed transactions.<br><br>**Constraints**: *Maximum Items*: `10` | getDisputedTransactions(): array | setDisputedTransactions(array disputedTransactions): void |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` | getEnvironment(): string | setEnvironment(string environment): void |
| `evidenceClass` | [`string(EvidenceClassEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/evidence-class.md) | Required | Evidence class. | getEvidenceClass(): string | setEvidenceClass(string evidenceClass): void |
| `evidences` | [`DisputeEvidenceRow[]`](http://localhost:3000/llms-pages/php/models/structures/dispute-evidence-row.md) | Required | Evidences.<br><br>**Constraints**: *Maximum Items*: `20` | getEvidences(): array | setEvidences(array evidences): void |
| `observedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` | getObservedAt(): string | setObservedAt(string observedAt): void |
| `paypalDebugId` | string\|null | Optional | This is a container for any-of cases. | getPaypalDebugId(): ?string | setPaypalDebugId(?string paypalDebugId): void |
| `providerSubmission` | [`string(ProviderSubmissionEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/provider-submission.md) | Required | Provider submission. | getProviderSubmission(): string | setProviderSubmission(string providerSubmission): void |
| `readback` | `string` | Required, Constant | Readback.<br><br>**Value**: `'GET_DETAIL'` | getReadback(): string | setReadback(string readback): void |
| `reason` | [`string(Reason2Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/reason-2.md) | Required | Reason. | getReason(): string | setReason(string reason): void |
| `sellerResponseDueDate` | string\|null | Optional | This is a container for any-of cases. | getSellerResponseDueDate(): ?string | setSellerResponseDueDate(?string sellerResponseDueDate): void |
| `source` | [`string(SourceEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/source.md) | Required | Source. | getSource(): string | setSource(string source): void |
| `status` | [`string(Status3Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/status-3.md) | Required | Status. | getStatus(): string | setStatus(string status): void |
| `updateTime` | string\|null | Optional | This is a container for any-of cases. | getUpdateTime(): ?string | setUpdateTime(?string updateTime): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\DisputeDetailResponseBuilder;
use TradeGlotLocalConsoleLib\Models\DataSourceLabelEnum;
use TradeGlotLocalConsoleLib\Models\Builders\ProviderMoneyBuilder;
use TradeGlotLocalConsoleLib\Models\DisputeLifeCycleStageEnum;
use TradeGlotLocalConsoleLib\Models\Builders\DisputedTransactionBuilder;
use TradeGlotLocalConsoleLib\Models\EvidenceClassEnum;
use TradeGlotLocalConsoleLib\Models\Builders\DisputeEvidenceRowBuilder;
use TradeGlotLocalConsoleLib\Models\Source3Enum;
use TradeGlotLocalConsoleLib\Models\ProviderSubmissionEnum;
use TradeGlotLocalConsoleLib\Models\Reason2Enum;
use TradeGlotLocalConsoleLib\Models\SourceEnum;
use TradeGlotLocalConsoleLib\Models\Status3Enum;

$disputeDetailResponse = DisputeDetailResponseBuilder::init(
    'create_time6',
    DataSourceLabelEnum::SANDBOX,
    ProviderMoneyBuilder::init(
        'currency_code6',
        'value0'
    )->build(),
    'dispute_id2',
    DisputeLifeCycleStageEnum::UNKNOWN,
    [
        DisputedTransactionBuilder::init(
            'seller_transaction_id2'
        )
            ->grossAmount(
                ProviderMoneyBuilder::init(
                    'currency_code0',
                    'value6'
                )->build()
            )
            ->sellerProtectionEligible(
                true
            )
            ->transactionStatus(
                'String7'
            )
            ->build()
    ],
    EvidenceClassEnum::SYNTHETIC_TEST_RESPONSE,
    [
        DisputeEvidenceRowBuilder::init(
            'evidence_type2',
            Source3Enum::SUBMITTED_BY_PARTNER
        )
            ->action(
                'String1'
            )
            ->date(
                'String9'
            )
            ->build()
    ],
    'observed_at4',
    ProviderSubmissionEnum::NOT_PERFORMED,
    Reason2Enum::MERCHANDISE_OR_SERVICE_NOT_RECEIVED,
    SourceEnum::PAYPAL_SANDBOX,
    Status3Enum::CLOSED
)
    ->disputeChannel(
        'String5'
    )
    ->disputeState(
        'String9'
    )
    ->paypalDebugId(
        'String1'
    )
    ->sellerResponseDueDate(
        'String9'
    )
    ->updateTime(
        'String9'
    )
    ->build();
```



