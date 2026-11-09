# Provide Evidence Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlc3BvbnNl

ProvideEvidenceResponse.


# Class Name

`ProvideEvidenceResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CaseRef` | `String` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` | String getCaseRef() | setCaseRef(String caseRef) |
| `ConfirmToken` | [`ProvideEvidenceResponseConfirmToken`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/provide-evidence-response-confirm-token.md) | Optional | This is a container for any-of cases. | ProvideEvidenceResponseConfirmToken getConfirmToken() | setConfirmToken(ProvideEvidenceResponseConfirmToken confirmToken) |
| `ContentType` | `String` | Required, Constant | Content type.<br><br>**Value**: `"multipart/form-data"` | String getContentType() | setContentType(String contentType) |
| `DataSourceLabel` | [`DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/data-source-label.md) | Required | Data source label. | DataSourceLabelEnum getDataSourceLabel() | setDataSourceLabel(DataSourceLabelEnum dataSourceLabel) |
| `DisputeId` | `String` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` | String getDisputeId() | setDisputeId(String disputeId) |
| `Environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` | String getEnvironment() | setEnvironment(String environment) |
| `EvidenceClass` | [`EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/evidence-class.md) | Required | Evidence class. | EvidenceClassEnum getEvidenceClass() | setEvidenceClass(EvidenceClassEnum evidenceClass) |
| `ExternalSend` | [`ExternalSendEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/external-send.md) | Required | External send. | ExternalSendEnum getExternalSend() | setExternalSend(ExternalSendEnum externalSend) |
| `Files` | [`List<MultipartFilePart>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/multipart-file-part.md) | Required | Files.<br><br>**Constraints**: *Maximum Items*: `20` | List<MultipartFilePart> getFiles() | setFiles(List<MultipartFilePart> files) |
| `HumanReviewRequired` | `String` | Required, Constant | Human review required.<br><br>**Value**: `"True"` | String getHumanReviewRequired() | setHumanReviewRequired(String humanReviewRequired) |
| `Input` | [`EvidenceInput`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/evidence-input.md) | Required | EvidenceInput. | EvidenceInput getInput() | setInput(EvidenceInput input) |
| `Method` | `String` | Required, Constant | Method.<br><br>**Value**: `"POST"` | String getMethod() | setMethod(String method) |
| `ObservedAt` | `String` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` | String getObservedAt() | setObservedAt(String observedAt) |
| `Path` | `String` | Required | Path.<br><br>**Constraints**: *Pattern*: `^/v1/customer/disputes/PP-[A-Z0-9][A-Z0-9-]{2,62}/provide-evidence$` | String getPath() | setPath(String path) |
| `PayloadSha256` | [`ProvideEvidenceResponsePayloadSha256`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/provide-evidence-response-payload-sha-256.md) | Optional | This is a container for any-of cases. | ProvideEvidenceResponsePayloadSha256 getPayloadSha256() | setPayloadSha256(ProvideEvidenceResponsePayloadSha256 payloadSha256) |
| `PaypalDebugId` | [`ProvideEvidenceResponsePaypalDebugId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/provide-evidence-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. | ProvideEvidenceResponsePaypalDebugId getPaypalDebugId() | setPaypalDebugId(ProvideEvidenceResponsePaypalDebugId paypalDebugId) |
| `ProviderSubmission` | [`ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/provider-submission.md) | Required | Provider submission. | ProviderSubmissionEnum getProviderSubmission() | setProviderSubmission(ProviderSubmissionEnum providerSubmission) |
| `Readback` | [`Readback1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/readback-1.md) | Required | Readback. | Readback1Enum getReadback() | setReadback(Readback1Enum readback) |
| `SendGuard` | [`SendGuard`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). | SendGuard getSendGuard() | setSendGuard(SendGuard sendGuard) |
| `SentFiles` | [`ProvideEvidenceResponseSentFiles`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/provide-evidence-response-sent-files.md) | Optional | This is a container for any-of cases. | ProvideEvidenceResponseSentFiles getSentFiles() | setSentFiles(ProvideEvidenceResponseSentFiles sentFiles) |
| `Source` | [`SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/source.md) | Required | Source. | SourceEnum getSource() | setSource(SourceEnum source) |
| `SubmitFlagEnabled` | `boolean` | Required | Submit flag enabled. | boolean getSubmitFlagEnabled() | setSubmitFlagEnabled(boolean submitFlagEnabled) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.AccountStatusEnum;
import m18000.m0.m0.m127.models.CarrierNameEnum;
import m18000.m0.m0.m127.models.ContentTypeEnum;
import m18000.m0.m0.m127.models.DataSourceLabelEnum;
import m18000.m0.m0.m127.models.EvidenceClassEnum;
import m18000.m0.m0.m127.models.EvidenceInfo;
import m18000.m0.m0.m127.models.EvidenceInput;
import m18000.m0.m0.m127.models.EvidenceInputItem;
import m18000.m0.m0.m127.models.ExternalSendEnum;
import m18000.m0.m0.m127.models.MultipartFilePart;
import m18000.m0.m0.m127.models.ProvideEvidenceResponse;
import m18000.m0.m0.m127.models.ProviderMoney;
import m18000.m0.m0.m127.models.ProviderSubmissionEnum;
import m18000.m0.m0.m127.models.Readback1Enum;
import m18000.m0.m0.m127.models.SendGuard;
import m18000.m0.m0.m127.models.SentFileFingerprint;
import m18000.m0.m0.m127.models.SourceEnum;
import m18000.m0.m0.m127.models.TrackingInfo;
import m18000.m0.m0.m127.models.containers.ProvideEvidenceResponseConfirmToken;
import m18000.m0.m0.m127.models.containers.ProvideEvidenceResponsePayloadSha256;
import m18000.m0.m0.m127.models.containers.ProvideEvidenceResponsePaypalDebugId;
import m18000.m0.m0.m127.models.containers.ProvideEvidenceResponseSentFiles;
import m18000.m0.m0.m127.models.containers.SendGuardBoundDisputeMasked;
import m18000.m0.m0.m127.models.containers.SendGuardCaseReason;
import m18000.m0.m0.m127.models.containers.SendGuardDisputeAmount;
import m18000.m0.m0.m127.models.containers.SendGuardDisputeReason;
import m18000.m0.m0.m127.models.containers.SendGuardDisputeSellerMasked;
import m18000.m0.m0.m127.models.containers.TrackingInfoCarrierNameOther;

ProvideEvidenceResponse provideEvidenceResponse = new ProvideEvidenceResponse.Builder(
    "case_ref2",
    "multipart/form-data",
    DataSourceLabelEnum.SANDBOX,
    "dispute_id0",
    "sandbox",
    EvidenceClassEnum.AUTHENTIC_SANDBOX_RESPONSE,
    ExternalSendEnum.FROZEN,
    Arrays.asList(
        new MultipartFilePart.Builder(
            68,
            ContentTypeEnum.ENUM_IMAGEPNG,
            "filename6",
            "name4"
        )
        .build()
    ),
    "True",
    new EvidenceInput.Builder(
        Arrays.asList(
            new EvidenceInputItem.Builder(
                new EvidenceInfo.Builder(
                    Arrays.asList(
                        new TrackingInfo.Builder(
                            CarrierNameEnum.DHL,
                            "tracking_number6"
                        )
                        .carrierNameOther(TrackingInfoCarrierNameOther.fromString(
                                "String1"
                            ))
                        .build()
                    )
                )
                .build(),
                "evidence_type2",
                "notes2"
            )
            .build()
        )
    )
    .build(),
    "POST",
    "observed_at2",
    "path2",
    ProviderSubmissionEnum.NOT_PERFORMED,
    Readback1Enum.PROVIDE_EVIDENCE_PREVIEW,
    new SendGuard.Builder(
        AccountStatusEnum.MATCH,
        "case_ref6",
        "dispute_masked0"
    )
    .boundDisputeMasked(SendGuardBoundDisputeMasked.fromString(
            "String3"
        ))
    .caseReason(SendGuardCaseReason.fromString(
            "String7"
        ))
    .disputeAmount(SendGuardDisputeAmount.fromProviderMoney(
            new ProviderMoney.Builder(
                "currency_code0",
                "value6"
            )
            .build()
        ))
    .disputeReason(SendGuardDisputeReason.fromString(
            "String9"
        ))
    .disputeSellerMasked(SendGuardDisputeSellerMasked.fromString(
            "String1"
        ))
    .build(),
    SourceEnum.PAYPAL_SANDBOX,
    false
)
.confirmToken(ProvideEvidenceResponseConfirmToken.fromString(
        "String9"
    ))
.payloadSha256(ProvideEvidenceResponsePayloadSha256.fromString(
        "String9"
    ))
.paypalDebugId(ProvideEvidenceResponsePaypalDebugId.fromString(
        "String9"
    ))
.sentFiles(ProvideEvidenceResponseSentFiles.fromListOfSentFileFingerprint(
        Arrays.asList(
            new SentFileFingerprint.Builder(
                196,
                ContentTypeEnum.ENUM_IMAGEPNG,
                "filename6",
                "sha2566"
            )
            .build(),
            new SentFileFingerprint.Builder(
                196,
                ContentTypeEnum.ENUM_IMAGEPNG,
                "filename6",
                "sha2566"
            )
            .build(),
            new SentFileFingerprint.Builder(
                196,
                ContentTypeEnum.ENUM_IMAGEPNG,
                "filename6",
                "sha2566"
            )
            .build()
        )
    ))
.build();
```



