# Dispute Detail Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkRpc3B1dGVEZXRhaWxSZXNwb25zZQ

DisputeDetailResponse.


# Class Name

`DisputeDetailResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CreateTime` | `String` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` | String getCreateTime() | setCreateTime(String createTime) |
| `DataSourceLabel` | [`DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/data-source-label.md) | Required | Data source label. | DataSourceLabelEnum getDataSourceLabel() | setDataSourceLabel(DataSourceLabelEnum dataSourceLabel) |
| `DisputeAmount` | [`ProviderMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/provider-money.md) | Required | ProviderMoney. | ProviderMoney getDisputeAmount() | setDisputeAmount(ProviderMoney disputeAmount) |
| `DisputeChannel` | [`DisputeDetailResponseDisputeChannel`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/dispute-detail-response-dispute-channel.md) | Optional | This is a container for any-of cases. | DisputeDetailResponseDisputeChannel getDisputeChannel() | setDisputeChannel(DisputeDetailResponseDisputeChannel disputeChannel) |
| `DisputeId` | `String` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` | String getDisputeId() | setDisputeId(String disputeId) |
| `DisputeLifeCycleStage` | [`DisputeLifeCycleStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. | DisputeLifeCycleStageEnum getDisputeLifeCycleStage() | setDisputeLifeCycleStage(DisputeLifeCycleStageEnum disputeLifeCycleStage) |
| `DisputeState` | [`DisputeDetailResponseDisputeState`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/dispute-detail-response-dispute-state.md) | Optional | This is a container for any-of cases. | DisputeDetailResponseDisputeState getDisputeState() | setDisputeState(DisputeDetailResponseDisputeState disputeState) |
| `DisputedTransactions` | [`List<DisputedTransaction>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/disputed-transaction.md) | Required | Disputed transactions.<br><br>**Constraints**: *Maximum Items*: `10` | List<DisputedTransaction> getDisputedTransactions() | setDisputedTransactions(List<DisputedTransaction> disputedTransactions) |
| `Environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` | String getEnvironment() | setEnvironment(String environment) |
| `EvidenceClass` | [`EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/evidence-class.md) | Required | Evidence class. | EvidenceClassEnum getEvidenceClass() | setEvidenceClass(EvidenceClassEnum evidenceClass) |
| `Evidences` | [`List<DisputeEvidenceRow>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/dispute-evidence-row.md) | Required | Evidences.<br><br>**Constraints**: *Maximum Items*: `20` | List<DisputeEvidenceRow> getEvidences() | setEvidences(List<DisputeEvidenceRow> evidences) |
| `ObservedAt` | `String` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` | String getObservedAt() | setObservedAt(String observedAt) |
| `PaypalDebugId` | [`DisputeDetailResponsePaypalDebugId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/dispute-detail-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. | DisputeDetailResponsePaypalDebugId getPaypalDebugId() | setPaypalDebugId(DisputeDetailResponsePaypalDebugId paypalDebugId) |
| `ProviderSubmission` | [`ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/provider-submission.md) | Required | Provider submission. | ProviderSubmissionEnum getProviderSubmission() | setProviderSubmission(ProviderSubmissionEnum providerSubmission) |
| `Readback` | `String` | Required, Constant | Readback.<br><br>**Value**: `"GET_DETAIL"` | String getReadback() | setReadback(String readback) |
| `Reason` | [`Reason2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/reason-2.md) | Required | Reason. | Reason2Enum getReason() | setReason(Reason2Enum reason) |
| `SellerResponseDueDate` | [`DisputeDetailResponseSellerResponseDueDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/dispute-detail-response-seller-response-due-date.md) | Optional | This is a container for any-of cases. | DisputeDetailResponseSellerResponseDueDate getSellerResponseDueDate() | setSellerResponseDueDate(DisputeDetailResponseSellerResponseDueDate sellerResponseDueDate) |
| `Source` | [`SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/source.md) | Required | Source. | SourceEnum getSource() | setSource(SourceEnum source) |
| `Status` | [`Status3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/status-3.md) | Required | Status. | Status3Enum getStatus() | setStatus(Status3Enum status) |
| `UpdateTime` | [`DisputeDetailResponseUpdateTime`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/dispute-detail-response-update-time.md) | Optional | This is a container for any-of cases. | DisputeDetailResponseUpdateTime getUpdateTime() | setUpdateTime(DisputeDetailResponseUpdateTime updateTime) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.DataSourceLabelEnum;
import m18000.m0.m0.m127.models.DisputeDetailResponse;
import m18000.m0.m0.m127.models.DisputeEvidenceRow;
import m18000.m0.m0.m127.models.DisputeLifeCycleStageEnum;
import m18000.m0.m0.m127.models.DisputedTransaction;
import m18000.m0.m0.m127.models.EvidenceClassEnum;
import m18000.m0.m0.m127.models.ProviderMoney;
import m18000.m0.m0.m127.models.ProviderSubmissionEnum;
import m18000.m0.m0.m127.models.Reason2Enum;
import m18000.m0.m0.m127.models.Source3Enum;
import m18000.m0.m0.m127.models.SourceEnum;
import m18000.m0.m0.m127.models.Status3Enum;
import m18000.m0.m0.m127.models.containers.DisputeDetailResponseDisputeChannel;
import m18000.m0.m0.m127.models.containers.DisputeDetailResponseDisputeState;
import m18000.m0.m0.m127.models.containers.DisputeDetailResponsePaypalDebugId;
import m18000.m0.m0.m127.models.containers.DisputeDetailResponseSellerResponseDueDate;
import m18000.m0.m0.m127.models.containers.DisputeDetailResponseUpdateTime;
import m18000.m0.m0.m127.models.containers.DisputeEvidenceRowAction;
import m18000.m0.m0.m127.models.containers.DisputeEvidenceRowDate;
import m18000.m0.m0.m127.models.containers.DisputedTransactionGrossAmount;
import m18000.m0.m0.m127.models.containers.DisputedTransactionSellerProtectionEligible;
import m18000.m0.m0.m127.models.containers.DisputedTransactionTransactionStatus;

DisputeDetailResponse disputeDetailResponse = new DisputeDetailResponse.Builder(
    "create_time6",
    DataSourceLabelEnum.SANDBOX,
    new ProviderMoney.Builder(
        "currency_code6",
        "value0"
    )
    .build(),
    "dispute_id2",
    DisputeLifeCycleStageEnum.UNKNOWN,
    Arrays.asList(
        new DisputedTransaction.Builder(
            "seller_transaction_id2"
        )
        .grossAmount(DisputedTransactionGrossAmount.fromProviderMoney(
                new ProviderMoney.Builder(
                    "currency_code0",
                    "value6"
                )
                .build()
            ))
        .sellerProtectionEligible(DisputedTransactionSellerProtectionEligible.fromBoolean(
                true
            ))
        .transactionStatus(DisputedTransactionTransactionStatus.fromString(
                "String7"
            ))
        .build()
    ),
    "sandbox",
    EvidenceClassEnum.SYNTHETIC_TEST_RESPONSE,
    Arrays.asList(
        new DisputeEvidenceRow.Builder(
            "evidence_type2",
            Source3Enum.SUBMITTED_BY_PARTNER
        )
        .action(DisputeEvidenceRowAction.fromString(
                "String1"
            ))
        .date(DisputeEvidenceRowDate.fromString(
                "String9"
            ))
        .build()
    ),
    "observed_at4",
    ProviderSubmissionEnum.NOT_PERFORMED,
    "GET_DETAIL",
    Reason2Enum.MERCHANDISE_OR_SERVICE_NOT_RECEIVED,
    SourceEnum.PAYPAL_SANDBOX,
    Status3Enum.CLOSED
)
.disputeChannel(DisputeDetailResponseDisputeChannel.fromString(
        "String5"
    ))
.disputeState(DisputeDetailResponseDisputeState.fromString(
        "String9"
    ))
.paypalDebugId(DisputeDetailResponsePaypalDebugId.fromString(
        "String1"
    ))
.sellerResponseDueDate(DisputeDetailResponseSellerResponseDueDate.fromString(
        "String9"
    ))
.updateTime(DisputeDetailResponseUpdateTime.fromString(
        "String9"
    ))
.build();
```



