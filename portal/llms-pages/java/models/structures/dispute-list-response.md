# Dispute List Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkRpc3B1dGVMaXN0UmVzcG9uc2U

DisputeListResponse.


# Class Name

`DisputeListResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `DataSourceLabel` | [`DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/data-source-label.md) | Required | Data source label. | DataSourceLabelEnum getDataSourceLabel() | setDataSourceLabel(DataSourceLabelEnum dataSourceLabel) |
| `Environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` | String getEnvironment() | setEnvironment(String environment) |
| `EvidenceClass` | [`EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/evidence-class.md) | Required | Evidence class. | EvidenceClassEnum getEvidenceClass() | setEvidenceClass(EvidenceClassEnum evidenceClass) |
| `Items` | [`List<DisputeRecord>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/dispute-record.md) | Required | Items.<br><br>**Constraints**: *Maximum Items*: `20` | List<DisputeRecord> getItems() | setItems(List<DisputeRecord> items) |
| `ObservedAt` | `String` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` | String getObservedAt() | setObservedAt(String observedAt) |
| `PaypalDebugId` | [`DisputeListResponsePaypalDebugId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/dispute-list-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. | DisputeListResponsePaypalDebugId getPaypalDebugId() | setPaypalDebugId(DisputeListResponsePaypalDebugId paypalDebugId) |
| `ProviderSubmission` | [`ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/provider-submission.md) | Required | Provider submission. | ProviderSubmissionEnum getProviderSubmission() | setProviderSubmission(ProviderSubmissionEnum providerSubmission) |
| `Readback` | `String` | Required, Constant | Readback.<br><br>**Value**: `"GET_LIST"` | String getReadback() | setReadback(String readback) |
| `Source` | [`SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/source.md) | Required | Source. | SourceEnum getSource() | setSource(SourceEnum source) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.DataSourceLabelEnum;
import m18000.m0.m0.m127.models.DisputeLifeCycleStageEnum;
import m18000.m0.m0.m127.models.DisputeListResponse;
import m18000.m0.m0.m127.models.DisputeRecord;
import m18000.m0.m0.m127.models.EvidenceClassEnum;
import m18000.m0.m0.m127.models.ProviderMoney;
import m18000.m0.m0.m127.models.ProviderSubmissionEnum;
import m18000.m0.m0.m127.models.Reason2Enum;
import m18000.m0.m0.m127.models.SourceEnum;
import m18000.m0.m0.m127.models.Status3Enum;
import m18000.m0.m0.m127.models.containers.DisputeListResponsePaypalDebugId;
import m18000.m0.m0.m127.models.containers.DisputeRecordDisputeState;
import m18000.m0.m0.m127.models.containers.DisputeRecordSellerResponseDueDate;
import m18000.m0.m0.m127.models.containers.DisputeRecordUpdateTime;

DisputeListResponse disputeListResponse = new DisputeListResponse.Builder(
    DataSourceLabelEnum.SANDBOX,
    "sandbox",
    EvidenceClassEnum.SYNTHETIC_TEST_RESPONSE,
    Arrays.asList(
        new DisputeRecord.Builder(
            "create_time4",
            new ProviderMoney.Builder(
                "currency_code6",
                "value0"
            )
            .build(),
            "dispute_id0",
            DisputeLifeCycleStageEnum.PRE_ARBITRATION,
            Reason2Enum.CREDIT_NOT_PROCESSED,
            Status3Enum.UNDER_REVIEW
        )
        .disputeState(DisputeRecordDisputeState.fromString(
                "String1"
            ))
        .sellerResponseDueDate(DisputeRecordSellerResponseDueDate.fromString(
                "String7"
            ))
        .updateTime(DisputeRecordUpdateTime.fromString(
                "String1"
            ))
        .build()
    ),
    "observed_at4",
    ProviderSubmissionEnum.NOT_PERFORMED,
    "GET_LIST",
    SourceEnum.PAYPAL_SANDBOX
)
.paypalDebugId(DisputeListResponsePaypalDebugId.fromString(
        "String1"
    ))
.build();
```



