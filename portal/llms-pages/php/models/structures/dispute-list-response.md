# Dispute List Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkRpc3B1dGVMaXN0UmVzcG9uc2U

DisputeListResponse.


# Class Name

`DisputeListResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `dataSourceLabel` | [`string(DataSourceLabelEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/data-source-label.md) | Required | Data source label. | getDataSourceLabel(): string | setDataSourceLabel(string dataSourceLabel): void |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` | getEnvironment(): string | setEnvironment(string environment): void |
| `evidenceClass` | [`string(EvidenceClassEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/evidence-class.md) | Required | Evidence class. | getEvidenceClass(): string | setEvidenceClass(string evidenceClass): void |
| `items` | [`DisputeRecord[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/dispute-record.md) | Required | Items.<br><br>**Constraints**: *Maximum Items*: `20` | getItems(): array | setItems(array items): void |
| `observedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` | getObservedAt(): string | setObservedAt(string observedAt): void |
| `paypalDebugId` | string\|null | Optional | This is a container for any-of cases. | getPaypalDebugId(): ?string | setPaypalDebugId(?string paypalDebugId): void |
| `providerSubmission` | [`string(ProviderSubmissionEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/provider-submission.md) | Required | Provider submission. | getProviderSubmission(): string | setProviderSubmission(string providerSubmission): void |
| `readback` | `string` | Required, Constant | Readback.<br><br>**Value**: `'GET_LIST'` | getReadback(): string | setReadback(string readback): void |
| `source` | [`string(SourceEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/source.md) | Required | Source. | getSource(): string | setSource(string source): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\DisputeListResponseBuilder;
use TradeGlotLocalConsoleLib\Models\DataSourceLabelEnum;
use TradeGlotLocalConsoleLib\Models\EvidenceClassEnum;
use TradeGlotLocalConsoleLib\Models\Builders\DisputeRecordBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\ProviderMoneyBuilder;
use TradeGlotLocalConsoleLib\Models\DisputeLifeCycleStageEnum;
use TradeGlotLocalConsoleLib\Models\Reason2Enum;
use TradeGlotLocalConsoleLib\Models\Status3Enum;
use TradeGlotLocalConsoleLib\Models\ProviderSubmissionEnum;
use TradeGlotLocalConsoleLib\Models\SourceEnum;

$disputeListResponse = DisputeListResponseBuilder::init(
    DataSourceLabelEnum::SANDBOX,
    EvidenceClassEnum::SYNTHETIC_TEST_RESPONSE,
    [
        DisputeRecordBuilder::init(
            'create_time4',
            ProviderMoneyBuilder::init(
                'currency_code6',
                'value0'
            )->build(),
            'dispute_id0',
            DisputeLifeCycleStageEnum::PRE_ARBITRATION,
            Reason2Enum::CREDIT_NOT_PROCESSED,
            Status3Enum::UNDER_REVIEW
        )
            ->disputeState(
                'String1'
            )
            ->sellerResponseDueDate(
                'String7'
            )
            ->updateTime(
                'String1'
            )
            ->build()
    ],
    'observed_at4',
    ProviderSubmissionEnum::NOT_PERFORMED,
    SourceEnum::PAYPAL_SANDBOX
)
    ->paypalDebugId(
        'String1'
    )
    ->build();
```



