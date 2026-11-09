# Dispute List Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkRpc3B1dGVMaXN0UmVzcG9uc2U

DisputeListResponse.


# Class Name

`DisputeListResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `DataSourceLabel` | [`DataSourceLabelEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/data-source-label.md) | Required | Data source label. |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceClass` | [`EvidenceClassEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `Items` | [`List<DisputeRecord>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/dispute-record.md) | Required | Items.<br><br>**Constraints**: *Maximum Items*: `20` |
| `ObservedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `PaypalDebugId` | [`DisputeListResponsePaypalDebugId`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-list-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `ProviderSubmission` | [`ProviderSubmissionEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `Readback` | `string` | Required, Constant | Readback.<br><br>**Value**: `"GET_LIST"` |
| `Source` | [`SourceEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/source.md) | Required | Source. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

DisputeListResponse disputeListResponse = new DisputeListResponse
{
    DataSourceLabel = DataSourceLabelEnum.Sandbox,
    Environment = "sandbox",
    EvidenceClass = EvidenceClassEnum.SYNTHETICTESTRESPONSE,
    Items = new List<DisputeRecord>
    {
        new DisputeRecord
        {
            CreateTime = "create_time4",
            DisputeAmount = new ProviderMoney
            {
                CurrencyCode = "currency_code6",
                MValue = "value0",
            },
            DisputeId = "dispute_id0",
            DisputeLifeCycleStage = DisputeLifeCycleStageEnum.PREARBITRATION,
            Reason = Reason2Enum.CREDITNOTPROCESSED,
            Status = Status3Enum.UNDERREVIEW,
            DisputeState = DisputeRecordDisputeState.FromString("String1"),
            SellerResponseDueDate = DisputeRecordSellerResponseDueDate.FromString("String7"),
            UpdateTime = DisputeRecordUpdateTime.FromString("String1"),
        },
    },
    ObservedAt = "observed_at4",
    ProviderSubmission = ProviderSubmissionEnum.NOTPERFORMED,
    Readback = "GET_LIST",
    Source = SourceEnum.PaypalSandbox,
    PaypalDebugId = DisputeListResponsePaypalDebugId.FromString("String1"),
};
```



