# Provide Evidence Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlc3BvbnNl

ProvideEvidenceResponse.


# Class Name

`ProvideEvidenceResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `caseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` | getCaseRef(): string | setCaseRef(string caseRef): void |
| `confirmToken` | string\|null | Optional | This is a container for any-of cases. | getConfirmToken(): ?string | setConfirmToken(?string confirmToken): void |
| `contentType` | `string` | Required, Constant | Content type.<br><br>**Value**: `'multipart/form-data'` | getContentType(): string | setContentType(string contentType): void |
| `dataSourceLabel` | [`string(DataSourceLabelEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/data-source-label.md) | Required | Data source label. | getDataSourceLabel(): string | setDataSourceLabel(string dataSourceLabel): void |
| `disputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` | getDisputeId(): string | setDisputeId(string disputeId): void |
| `environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `'sandbox'` | getEnvironment(): string | setEnvironment(string environment): void |
| `evidenceClass` | [`string(EvidenceClassEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/evidence-class.md) | Required | Evidence class. | getEvidenceClass(): string | setEvidenceClass(string evidenceClass): void |
| `externalSend` | [`string(ExternalSendEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/external-send.md) | Required | External send. | getExternalSend(): string | setExternalSend(string externalSend): void |
| `files` | [`MultipartFilePart[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/multipart-file-part.md) | Required | Files.<br><br>**Constraints**: *Maximum Items*: `20` | getFiles(): array | setFiles(array files): void |
| `humanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `'True'` | getHumanReviewRequired(): string | setHumanReviewRequired(string humanReviewRequired): void |
| `input` | [`EvidenceInput`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/evidence-input.md) | Required | EvidenceInput. | getInput(): EvidenceInput | setInput(EvidenceInput input): void |
| `method` | `string` | Required, Constant | Method.<br><br>**Value**: `'POST'` | getMethod(): string | setMethod(string method): void |
| `observedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` | getObservedAt(): string | setObservedAt(string observedAt): void |
| `path` | `string` | Required | Path.<br><br>**Constraints**: *Pattern*: `^/v1/customer/disputes/PP-[A-Z0-9][A-Z0-9-]{2,62}/provide-evidence$` | getPath(): string | setPath(string path): void |
| `payloadSha256` | string\|null | Optional | This is a container for any-of cases. | getPayloadSha256(): ?string | setPayloadSha256(?string payloadSha256): void |
| `paypalDebugId` | string\|null | Optional | This is a container for any-of cases. | getPaypalDebugId(): ?string | setPaypalDebugId(?string paypalDebugId): void |
| `providerSubmission` | [`string(ProviderSubmissionEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/provider-submission.md) | Required | Provider submission. | getProviderSubmission(): string | setProviderSubmission(string providerSubmission): void |
| `readback` | [`string(Readback1Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/readback-1.md) | Required | Readback. | getReadback(): string | setReadback(string readback): void |
| `sendGuard` | [`SendGuard`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). | getSendGuard(): SendGuard | setSendGuard(SendGuard sendGuard): void |
| `sentFiles` | [SentFileFingerprint](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/sent-file-fingerprint.md)[]\|null | Optional | This is a container for any-of cases. | getSentFiles(): ?array | setSentFiles(?array sentFiles): void |
| `source` | [`string(SourceEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/source.md) | Required | Source. | getSource(): string | setSource(string source): void |
| `submitFlagEnabled` | `bool` | Required | Submit flag enabled. | getSubmitFlagEnabled(): bool | setSubmitFlagEnabled(bool submitFlagEnabled): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ProvideEvidenceResponseBuilder;
use TradeGlotLocalConsoleLib\Models\DataSourceLabelEnum;
use TradeGlotLocalConsoleLib\Models\EvidenceClassEnum;
use TradeGlotLocalConsoleLib\Models\ExternalSendEnum;
use TradeGlotLocalConsoleLib\Models\Builders\MultipartFilePartBuilder;
use TradeGlotLocalConsoleLib\Models\ContentTypeEnum;
use TradeGlotLocalConsoleLib\Models\Builders\EvidenceInputBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\EvidenceInputItemBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\EvidenceInfoBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\TrackingInfoBuilder;
use TradeGlotLocalConsoleLib\Models\CarrierNameEnum;
use TradeGlotLocalConsoleLib\Models\ProviderSubmissionEnum;
use TradeGlotLocalConsoleLib\Models\Readback1Enum;
use TradeGlotLocalConsoleLib\Models\Builders\SendGuardBuilder;
use TradeGlotLocalConsoleLib\Models\AccountStatusEnum;
use TradeGlotLocalConsoleLib\Models\Builders\ProviderMoneyBuilder;
use TradeGlotLocalConsoleLib\Models\SourceEnum;
use TradeGlotLocalConsoleLib\Models\Builders\SentFileFingerprintBuilder;

$provideEvidenceResponse = ProvideEvidenceResponseBuilder::init(
    'case_ref2',
    DataSourceLabelEnum::SANDBOX,
    'dispute_id0',
    EvidenceClassEnum::AUTHENTIC_SANDBOX_RESPONSE,
    ExternalSendEnum::FROZEN,
    [
        MultipartFilePartBuilder::init(
            68,
            ContentTypeEnum::ENUM_IMAGEPNG,
            'filename6',
            'name4'
        )->build()
    ],
    EvidenceInputBuilder::init(
        [
            EvidenceInputItemBuilder::init(
                EvidenceInfoBuilder::init(
                    [
                        TrackingInfoBuilder::init(
                            CarrierNameEnum::DHL,
                            'tracking_number6'
                        )
                            ->carrierNameOther(
                                'String1'
                            )
                            ->build()
                    ]
                )->build(),
                'evidence_type2',
                'notes2'
            )->build()
        ]
    )->build(),
    'observed_at2',
    'path2',
    ProviderSubmissionEnum::NOT_PERFORMED,
    Readback1Enum::PROVIDE_EVIDENCE_PREVIEW,
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
    ->sentFiles(
        [
            SentFileFingerprintBuilder::init(
                196,
                ContentTypeEnum::ENUM_IMAGEPNG,
                'filename6',
                'sha2566'
            )->build(),
            SentFileFingerprintBuilder::init(
                196,
                ContentTypeEnum::ENUM_IMAGEPNG,
                'filename6',
                'sha2566'
            )->build(),
            SentFileFingerprintBuilder::init(
                196,
                ContentTypeEnum::ENUM_IMAGEPNG,
                'filename6',
                'sha2566'
            )->build()
        ]
    )->build();
```



