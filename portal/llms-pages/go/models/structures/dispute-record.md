# Dispute Record

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkRpc3B1dGVSZWNvcmQ

DisputeRecord.


# Class Name

`DisputeRecord`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CreateTime` | `string` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` |
| `DisputeAmount` | [`models.ProviderMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/provider-money.md) | Required | ProviderMoney. |
| `DisputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `DisputeLifeCycleStage` | [`models.DisputeLifeCycleStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `DisputeState` | [`*models.DisputeRecordDisputeState`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/dispute-record-dispute-state.md) | Optional | This is a container for any-of cases. |
| `Reason` | [`models.Reason2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/reason-2.md) | Required | Reason. |
| `SellerResponseDueDate` | [`*models.DisputeRecordSellerResponseDueDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/dispute-record-seller-response-due-date.md) | Optional | This is a container for any-of cases. |
| `Status` | [`models.Status3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/status-3.md) | Required | Status. |
| `UpdateTime` | [`*models.DisputeRecordUpdateTime`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/dispute-record-update-time.md) | Optional | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    disputeRecord := models.DisputeRecord{
        CreateTime:            "create_time0",
        DisputeAmount:         models.ProviderMoney{
            CurrencyCode:         "currency_code6",
            Value:                "value0",
        },
        DisputeId:             "dispute_id6",
        DisputeLifeCycleStage: models.DisputeLifeCycleStageEnum_ARBITRATION,
        DisputeState:          models.ToPointer(models.DisputeRecordDisputeStateContainer.FromString("String7")),
        Reason:                models.Reason2Enum_MERCHANDISEORSERVICENOTRECEIVED,
        SellerResponseDueDate: models.ToPointer(models.DisputeRecordSellerResponseDueDateContainer.FromString("String3")),
        Status:                models.Status3Enum_OPEN,
        UpdateTime:            models.ToPointer(models.DisputeRecordUpdateTimeContainer.FromString("String7")),
    }

}
```



