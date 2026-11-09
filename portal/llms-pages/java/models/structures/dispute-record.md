# Dispute Record

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkRpc3B1dGVSZWNvcmQ

DisputeRecord.


# Class Name

`DisputeRecord`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CreateTime` | `String` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` | String getCreateTime() | setCreateTime(String createTime) |
| `DisputeAmount` | [`ProviderMoney`](http://localhost:3000/llms-pages/java/models/structures/provider-money.md) | Required | ProviderMoney. | ProviderMoney getDisputeAmount() | setDisputeAmount(ProviderMoney disputeAmount) |
| `DisputeId` | `String` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` | String getDisputeId() | setDisputeId(String disputeId) |
| `DisputeLifeCycleStage` | [`DisputeLifeCycleStageEnum`](http://localhost:3000/llms-pages/java/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. | DisputeLifeCycleStageEnum getDisputeLifeCycleStage() | setDisputeLifeCycleStage(DisputeLifeCycleStageEnum disputeLifeCycleStage) |
| `DisputeState` | [`DisputeRecordDisputeState`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/dispute-record-dispute-state.md) | Optional | This is a container for any-of cases. | DisputeRecordDisputeState getDisputeState() | setDisputeState(DisputeRecordDisputeState disputeState) |
| `Reason` | [`Reason2Enum`](http://localhost:3000/llms-pages/java/models/enumerations/reason-2.md) | Required | Reason. | Reason2Enum getReason() | setReason(Reason2Enum reason) |
| `SellerResponseDueDate` | [`DisputeRecordSellerResponseDueDate`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/dispute-record-seller-response-due-date.md) | Optional | This is a container for any-of cases. | DisputeRecordSellerResponseDueDate getSellerResponseDueDate() | setSellerResponseDueDate(DisputeRecordSellerResponseDueDate sellerResponseDueDate) |
| `Status` | [`Status3Enum`](http://localhost:3000/llms-pages/java/models/enumerations/status-3.md) | Required | Status. | Status3Enum getStatus() | setStatus(Status3Enum status) |
| `UpdateTime` | [`DisputeRecordUpdateTime`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/dispute-record-update-time.md) | Optional | This is a container for any-of cases. | DisputeRecordUpdateTime getUpdateTime() | setUpdateTime(DisputeRecordUpdateTime updateTime) |


# Example

```java
import m18000.m0.m0.m127.models.DisputeLifeCycleStageEnum;
import m18000.m0.m0.m127.models.DisputeRecord;
import m18000.m0.m0.m127.models.ProviderMoney;
import m18000.m0.m0.m127.models.Reason2Enum;
import m18000.m0.m0.m127.models.Status3Enum;
import m18000.m0.m0.m127.models.containers.DisputeRecordDisputeState;
import m18000.m0.m0.m127.models.containers.DisputeRecordSellerResponseDueDate;
import m18000.m0.m0.m127.models.containers.DisputeRecordUpdateTime;

DisputeRecord disputeRecord = new DisputeRecord.Builder(
    "create_time0",
    new ProviderMoney.Builder(
        "currency_code6",
        "value0"
    )
    .build(),
    "dispute_id6",
    DisputeLifeCycleStageEnum.ARBITRATION,
    Reason2Enum.MERCHANDISE_OR_SERVICE_NOT_RECEIVED,
    Status3Enum.OPEN
)
.disputeState(DisputeRecordDisputeState.fromString(
        "String7"
    ))
.sellerResponseDueDate(DisputeRecordSellerResponseDueDate.fromString(
        "String3"
    ))
.updateTime(DisputeRecordUpdateTime.fromString(
        "String7"
    ))
.build();
```



