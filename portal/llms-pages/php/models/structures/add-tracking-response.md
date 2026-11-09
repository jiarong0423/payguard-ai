# Add Tracking Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkFkZFRyYWNraW5nUmVzcG9uc2U

AddTrackingResponse.


# Class Name

`AddTrackingResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `body` | [`TrackerBatch`](http://localhost:3000/llms-pages/php/models/structures/tracker-batch.md) | Required | TrackerBatch. | getBody(): TrackerBatch | setBody(TrackerBatch body): void |
| `caseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` | getCaseRef(): string | setCaseRef(string caseRef): void |
| `confirmToken` | string\|null | Optional | This is a container for any-of cases. | getConfirmToken(): ?string | setConfirmToken(?string confirmToken): void |
| `contentType` | `string` | Required, Constant | Content type.<br><br>**Value**: `'application/json'` | getContentType(): string | setContentType(string contentType): void |
| `dataSourceLabel` | [`string(DataSourceLabelEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/data-source-label.md) | Required | Data source label. | getDataSourceLabel(): string | setDataSourceLabel(string dataSourceLabel): void |
| `disputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` | getDisputeId(): string | setDisputeId(string disputeId): void |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` | getEnvironment(): string | setEnvironment(string environment): void |
| `evidenceClass` | [`string(EvidenceClassEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/evidence-class.md) | Required | Evidence class. | getEvidenceClass(): string | setEvidenceClass(string evidenceClass): void |
| `externalSend` | [`string(ExternalSendEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/external-send.md) | Required | External send. | getExternalSend(): string | setExternalSend(string externalSend): void |
| `humanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `'True'` | getHumanReviewRequired(): string | setHumanReviewRequired(string humanReviewRequired): void |
| `method` | `string` | Required, Constant | Method.<br><br>**Value**: `'POST'` | getMethod(): string | setMethod(string method): void |
| `observedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` | getObservedAt(): string | setObservedAt(string observedAt): void |
| `path` | `string` | Required, Constant | Path.<br><br>**Value**: `'/v1/shipping/trackers-batch'` | getPath(): string | setPath(string path): void |
| `payloadSha256` | string\|null | Optional | This is a container for any-of cases. | getPayloadSha256(): ?string | setPayloadSha256(?string payloadSha256): void |
| `paypalDebugId` | string\|null | Optional | This is a container for any-of cases. | getPaypalDebugId(): ?string | setPaypalDebugId(?string paypalDebugId): void |
| `providerSubmission` | [`string(ProviderSubmissionEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/provider-submission.md) | Required | Provider submission. | getProviderSubmission(): string | setProviderSubmission(string providerSubmission): void |
| `readback` | [`string(ReadbackEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/readback.md) | Required | Readback. | getReadback(): string | setReadback(string readback): void |
| `sendGuard` | [`SendGuard`](http://localhost:3000/llms-pages/php/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). | getSendGuard(): SendGuard | setSendGuard(SendGuard sendGuard): void |
| `source` | [`string(SourceEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/source.md) | Required | Source. | getSource(): string | setSource(string source): void |
| `submitFlagEnabled` | `bool` | Required | Submit flag enabled. | getSubmitFlagEnabled(): bool | setSubmitFlagEnabled(bool submitFlagEnabled): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AddTrackingResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\TrackerBatchBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\TrackerItemBuilder;
use TradeGlotLocalConsoleLib\Models\CarrierEnum;
use TradeGlotLocalConsoleLib\Models\DataSourceLabelEnum;
use TradeGlotLocalConsoleLib\Models\EvidenceClassEnum;
use TradeGlotLocalConsoleLib\Models\ExternalSendEnum;
use TradeGlotLocalConsoleLib\Models\ProviderSubmissionEnum;
use TradeGlotLocalConsoleLib\Models\ReadbackEnum;
use TradeGlotLocalConsoleLib\Models\Builders\SendGuardBuilder;
use TradeGlotLocalConsoleLib\Models\AccountStatusEnum;
use TradeGlotLocalConsoleLib\Models\Builders\ProviderMoneyBuilder;
use TradeGlotLocalConsoleLib\Models\SourceEnum;

$addTrackingResponse = AddTrackingResponseBuilder::init(
    TrackerBatchBuilder::init(
        [
            TrackerItemBuilder::init(
                CarrierEnum::JP_JAPANPOST,
                'tracking_number0',
                'transaction_id0'
            )
                ->carrierNameOther(
                    'String5'
                )
                ->build()
        ]
    )->build(),
    'case_ref6',
    DataSourceLabelEnum::SANDBOX,
    'dispute_id4',
    EvidenceClassEnum::AUTHENTIC_SANDBOX_RESPONSE,
    ExternalSendEnum::FROZEN,
    'observed_at6',
    ProviderSubmissionEnum::NOT_PERFORMED,
    ReadbackEnum::ADD_TRACKING_PREVIEW,
    SendGuardBuilder::init(
        AccountStatusEnum::MATCH,
        'case_ref6',
        'dispute_masked0'
    )
        ->boundDisputeMasked(
            'String3'
        )
        ->caseReason(
            'String7'
        )
        ->disputeAmount(
            ProviderMoneyBuilder::init(
                'currency_code0',
                'value6'
            )->build()
        )
        ->disputeReason(
            'String9'
        )
        ->disputeSellerMasked(
            'String1'
        )
        ->build(),
    SourceEnum::PAYPAL_SANDBOX,
    false
)
    ->confirmToken(
        'String9'
    )
    ->payloadSha256(
        'String9'
    )
    ->paypalDebugId(
        'String9'
    )
    ->build();
```



