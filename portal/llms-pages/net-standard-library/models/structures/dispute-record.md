# Dispute Record

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkRpc3B1dGVSZWNvcmQ

DisputeRecord.


# Class Name

`DisputeRecord`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CreateTime` | `string` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` |
| `DisputeAmount` | [`ProviderMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/provider-money.md) | Required | ProviderMoney. |
| `DisputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `DisputeLifeCycleStage` | [`DisputeLifeCycleStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `DisputeState` | [`DisputeRecordDisputeState`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-record-dispute-state.md) | Optional | This is a container for any-of cases. |
| `Reason` | [`Reason2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/reason-2.md) | Required | Reason. |
| `SellerResponseDueDate` | [`DisputeRecordSellerResponseDueDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-record-seller-response-due-date.md) | Optional | This is a container for any-of cases. |
| `Status` | [`Status3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/status-3.md) | Required | Status. |
| `UpdateTime` | [`DisputeRecordUpdateTime`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-record-update-time.md) | Optional | This is a container for any-of cases. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

DisputeRecord disputeRecord = new DisputeRecord
{
    CreateTime = "create_time0",
    DisputeAmount = new ProviderMoney
    {
        CurrencyCode = "currency_code6",
        MValue = "value0",
    },
    DisputeId = "dispute_id6",
    DisputeLifeCycleStage = DisputeLifeCycleStageEnum.ARBITRATION,
    Reason = Reason2Enum.MERCHANDISEORSERVICENOTRECEIVED,
    Status = Status3Enum.OPEN,
    DisputeState = DisputeRecordDisputeState.FromString("String7"),
    SellerResponseDueDate = DisputeRecordSellerResponseDueDate.FromString("String3"),
    UpdateTime = DisputeRecordUpdateTime.FromString("String7"),
};
```



