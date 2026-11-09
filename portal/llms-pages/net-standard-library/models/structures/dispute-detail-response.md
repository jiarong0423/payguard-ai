# Dispute Detail Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkRpc3B1dGVEZXRhaWxSZXNwb25zZQ

DisputeDetailResponse.


# Class Name

`DisputeDetailResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CreateTime` | `string` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` |
| `DataSourceLabel` | [`DataSourceLabelEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/data-source-label.md) | Required | Data source label. |
| `DisputeAmount` | [`ProviderMoney`](http://localhost:3000/llms-pages/net-standard-library/models/structures/provider-money.md) | Required | ProviderMoney. |
| `DisputeChannel` | [`DisputeDetailResponseDisputeChannel`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-detail-response-dispute-channel.md) | Optional | This is a container for any-of cases. |
| `DisputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `DisputeLifeCycleStage` | [`DisputeLifeCycleStageEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `DisputeState` | [`DisputeDetailResponseDisputeState`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-detail-response-dispute-state.md) | Optional | This is a container for any-of cases. |
| `DisputedTransactions` | [`List<DisputedTransaction>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/disputed-transaction.md) | Required | Disputed transactions.<br><br>**Constraints**: *Maximum Items*: `10` |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceClass` | [`EvidenceClassEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `Evidences` | [`List<DisputeEvidenceRow>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/dispute-evidence-row.md) | Required | Evidences.<br><br>**Constraints**: *Maximum Items*: `20` |
| `ObservedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `PaypalDebugId` | [`DisputeDetailResponsePaypalDebugId`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-detail-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `ProviderSubmission` | [`ProviderSubmissionEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `Readback` | `string` | Required, Constant | Readback.<br><br>**Value**: `"GET_DETAIL"` |
| `Reason` | [`Reason2Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/reason-2.md) | Required | Reason. |
| `SellerResponseDueDate` | [`DisputeDetailResponseSellerResponseDueDate`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-detail-response-seller-response-due-date.md) | Optional | This is a container for any-of cases. |
| `Source` | [`SourceEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/source.md) | Required | Source. |
| `Status` | [`Status3Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/status-3.md) | Required | Status. |
| `UpdateTime` | [`DisputeDetailResponseUpdateTime`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-detail-response-update-time.md) | Optional | This is a container for any-of cases. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

DisputeDetailResponse disputeDetailResponse = new DisputeDetailResponse
{
    CreateTime = "create_time6",
    DataSourceLabel = DataSourceLabelEnum.Sandbox,
    DisputeAmount = new ProviderMoney
    {
        CurrencyCode = "currency_code6",
        MValue = "value0",
    },
    DisputeId = "dispute_id2",
    DisputeLifeCycleStage = DisputeLifeCycleStageEnum.UNKNOWN,
    DisputedTransactions = new List<DisputedTransaction>
    {
        new DisputedTransaction
        {
            SellerTransactionId = "seller_transaction_id2",
            GrossAmount = DisputedTransactionGrossAmount.FromProviderMoney(
                new ProviderMoney
                {
                    CurrencyCode = "currency_code0",
                    MValue = "value6",
                }
            ),
            SellerProtectionEligible = DisputedTransactionSellerProtectionEligible.FromBoolean(true),
            TransactionStatus = DisputedTransactionTransactionStatus.FromString("String7"),
        },
    },
    Environment = "sandbox",
    EvidenceClass = EvidenceClassEnum.SYNTHETICTESTRESPONSE,
    Evidences = new List<DisputeEvidenceRow>
    {
        new DisputeEvidenceRow
        {
            EvidenceType = "evidence_type2",
            Source = Source3Enum.SUBMITTEDBYPARTNER,
            Action = DisputeEvidenceRowAction.FromString("String1"),
            Date = DisputeEvidenceRowDate.FromString("String9"),
        },
    },
    ObservedAt = "observed_at4",
    ProviderSubmission = ProviderSubmissionEnum.NOTPERFORMED,
    Readback = "GET_DETAIL",
    Reason = Reason2Enum.MERCHANDISEORSERVICENOTRECEIVED,
    Source = SourceEnum.PaypalSandbox,
    Status = Status3Enum.CLOSED,
    DisputeChannel = DisputeDetailResponseDisputeChannel.FromString("String5"),
    DisputeState = DisputeDetailResponseDisputeState.FromString("String9"),
    PaypalDebugId = DisputeDetailResponsePaypalDebugId.FromString("String1"),
    SellerResponseDueDate = DisputeDetailResponseSellerResponseDueDate.FromString("String9"),
    UpdateTime = DisputeDetailResponseUpdateTime.FromString("String9"),
};
```



