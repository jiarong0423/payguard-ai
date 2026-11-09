# Add Tracking Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkFkZFRyYWNraW5nUmVzcG9uc2U

AddTrackingResponse.


# Class Name

`AddTrackingResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Body` | [`TrackerBatch`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/tracker-batch.md) | Required | TrackerBatch. | TrackerBatch getBody() | setBody(TrackerBatch body) |
| `CaseRef` | `String` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` | String getCaseRef() | setCaseRef(String caseRef) |
| `ConfirmToken` | [`AddTrackingResponseConfirmToken`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/add-tracking-response-confirm-token.md) | Optional | This is a container for any-of cases. | AddTrackingResponseConfirmToken getConfirmToken() | setConfirmToken(AddTrackingResponseConfirmToken confirmToken) |
| `ContentType` | `String` | Required, Constant | Content type.<br><br>**Value**: `"application/json"` | String getContentType() | setContentType(String contentType) |
| `DataSourceLabel` | [`DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/data-source-label.md) | Required | Data source label. | DataSourceLabelEnum getDataSourceLabel() | setDataSourceLabel(DataSourceLabelEnum dataSourceLabel) |
| `DisputeId` | `String` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` | String getDisputeId() | setDisputeId(String disputeId) |
| `Environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` | String getEnvironment() | setEnvironment(String environment) |
| `EvidenceClass` | [`EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/evidence-class.md) | Required | Evidence class. | EvidenceClassEnum getEvidenceClass() | setEvidenceClass(EvidenceClassEnum evidenceClass) |
| `ExternalSend` | [`ExternalSendEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/external-send.md) | Required | External send. | ExternalSendEnum getExternalSend() | setExternalSend(ExternalSendEnum externalSend) |
| `HumanReviewRequired` | `String` | Required, Constant | Human review required.<br><br>**Value**: `"True"` | String getHumanReviewRequired() | setHumanReviewRequired(String humanReviewRequired) |
| `Method` | `String` | Required, Constant | Method.<br><br>**Value**: `"POST"` | String getMethod() | setMethod(String method) |
| `ObservedAt` | `String` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` | String getObservedAt() | setObservedAt(String observedAt) |
| `Path` | `String` | Required, Constant | Path.<br><br>**Value**: `"/v1/shipping/trackers-batch"` | String getPath() | setPath(String path) |
| `PayloadSha256` | [`AddTrackingResponsePayloadSha256`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/add-tracking-response-payload-sha-256.md) | Optional | This is a container for any-of cases. | AddTrackingResponsePayloadSha256 getPayloadSha256() | setPayloadSha256(AddTrackingResponsePayloadSha256 payloadSha256) |
| `PaypalDebugId` | [`AddTrackingResponsePaypalDebugId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/add-tracking-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. | AddTrackingResponsePaypalDebugId getPaypalDebugId() | setPaypalDebugId(AddTrackingResponsePaypalDebugId paypalDebugId) |
| `ProviderSubmission` | [`ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/provider-submission.md) | Required | Provider submission. | ProviderSubmissionEnum getProviderSubmission() | setProviderSubmission(ProviderSubmissionEnum providerSubmission) |
| `Readback` | [`ReadbackEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/readback.md) | Required | Readback. | ReadbackEnum getReadback() | setReadback(ReadbackEnum readback) |
| `SendGuard` | [`SendGuard`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). | SendGuard getSendGuard() | setSendGuard(SendGuard sendGuard) |
| `Source` | [`SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/source.md) | Required | Source. | SourceEnum getSource() | setSource(SourceEnum source) |
| `SubmitFlagEnabled` | `boolean` | Required | Submit flag enabled. | boolean getSubmitFlagEnabled() | setSubmitFlagEnabled(boolean submitFlagEnabled) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.AccountStatusEnum;
import m18000.m0.m0.m127.models.AddTrackingResponse;
import m18000.m0.m0.m127.models.CarrierEnum;
import m18000.m0.m0.m127.models.DataSourceLabelEnum;
import m18000.m0.m0.m127.models.EvidenceClassEnum;
import m18000.m0.m0.m127.models.ExternalSendEnum;
import m18000.m0.m0.m127.models.ProviderMoney;
import m18000.m0.m0.m127.models.ProviderSubmissionEnum;
import m18000.m0.m0.m127.models.ReadbackEnum;
import m18000.m0.m0.m127.models.SendGuard;
import m18000.m0.m0.m127.models.SourceEnum;
import m18000.m0.m0.m127.models.TrackerBatch;
import m18000.m0.m0.m127.models.TrackerItem;
import m18000.m0.m0.m127.models.containers.AddTrackingResponseConfirmToken;
import m18000.m0.m0.m127.models.containers.AddTrackingResponsePayloadSha256;
import m18000.m0.m0.m127.models.containers.AddTrackingResponsePaypalDebugId;
import m18000.m0.m0.m127.models.containers.SendGuardBoundDisputeMasked;
import m18000.m0.m0.m127.models.containers.SendGuardCaseReason;
import m18000.m0.m0.m127.models.containers.SendGuardDisputeAmount;
import m18000.m0.m0.m127.models.containers.SendGuardDisputeReason;
import m18000.m0.m0.m127.models.containers.SendGuardDisputeSellerMasked;
import m18000.m0.m0.m127.models.containers.TrackerItemCarrierNameOther;

AddTrackingResponse addTrackingResponse = new AddTrackingResponse.Builder(
    new TrackerBatch.Builder(
        Arrays.asList(
            new TrackerItem.Builder(
                CarrierEnum.JP_JAPANPOST,
                "SHIPPED",
                "tracking_number0",
                "transaction_id0"
            )
            .carrierNameOther(TrackerItemCarrierNameOther.fromString(
                    "String5"
                ))
            .build()
        )
    )
    .build(),
    "case_ref6",
    "application/json",
    DataSourceLabelEnum.SANDBOX,
    "dispute_id4",
    "sandbox",
    EvidenceClassEnum.AUTHENTIC_SANDBOX_RESPONSE,
    ExternalSendEnum.FROZEN,
    "True",
    "POST",
    "observed_at6",
    "/v1/shipping/trackers-batch",
    ProviderSubmissionEnum.NOT_PERFORMED,
    ReadbackEnum.ADD_TRACKING_PREVIEW,
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
.confirmToken(AddTrackingResponseConfirmToken.fromString(
        "String9"
    ))
.payloadSha256(AddTrackingResponsePayloadSha256.fromString(
        "String9"
    ))
.paypalDebugId(AddTrackingResponsePaypalDebugId.fromString(
        "String9"
    ))
.build();
```



