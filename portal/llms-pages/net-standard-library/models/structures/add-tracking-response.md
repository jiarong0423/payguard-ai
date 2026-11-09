# Add Tracking Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkFkZFRyYWNraW5nUmVzcG9uc2U

AddTrackingResponse.


# Class Name

`AddTrackingResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Body` | [`TrackerBatch`](http://localhost:3000/llms-pages/net-standard-library/models/structures/tracker-batch.md) | Required | TrackerBatch. |
| `CaseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `ConfirmToken` | [`AddTrackingResponseConfirmToken`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/add-tracking-response-confirm-token.md) | Optional | This is a container for any-of cases. |
| `ContentType` | `string` | Required, Constant | Content type.<br><br>**Value**: `"application/json"` |
| `DataSourceLabel` | [`DataSourceLabelEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/data-source-label.md) | Required | Data source label. |
| `DisputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceClass` | [`EvidenceClassEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `ExternalSend` | [`ExternalSendEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/external-send.md) | Required | External send. |
| `HumanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `"True"` |
| `Method` | `string` | Required, Constant | Method.<br><br>**Value**: `"POST"` |
| `ObservedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `Path` | `string` | Required, Constant | Path.<br><br>**Value**: `"/v1/shipping/trackers-batch"` |
| `PayloadSha256` | [`AddTrackingResponsePayloadSha256`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/add-tracking-response-payload-sha-256.md) | Optional | This is a container for any-of cases. |
| `PaypalDebugId` | [`AddTrackingResponsePaypalDebugId`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/add-tracking-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `ProviderSubmission` | [`ProviderSubmissionEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `Readback` | [`ReadbackEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/readback.md) | Required | Readback. |
| `SendGuard` | [`SendGuard`](http://localhost:3000/llms-pages/net-standard-library/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). |
| `Source` | [`SourceEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/source.md) | Required | Source. |
| `SubmitFlagEnabled` | `bool` | Required | Submit flag enabled. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

AddTrackingResponse addTrackingResponse = new AddTrackingResponse
{
    Body = new TrackerBatch
    {
        Trackers = new List<TrackerItem>
        {
            new TrackerItem
            {
                Carrier = CarrierEnum.JPJAPANPOST,
                Status = "SHIPPED",
                TrackingNumber = "tracking_number0",
                TransactionId = "transaction_id0",
                CarrierNameOther = TrackerItemCarrierNameOther.FromString("String5"),
            },
        },
    },
    CaseRef = "case_ref6",
    ContentType = "application/json",
    DataSourceLabel = DataSourceLabelEnum.Sandbox,
    DisputeId = "dispute_id4",
    Environment = "sandbox",
    EvidenceClass = EvidenceClassEnum.AUTHENTICSANDBOXRESPONSE,
    ExternalSend = ExternalSendEnum.FROZEN,
    HumanReviewRequired = "True",
    Method = "POST",
    ObservedAt = "observed_at6",
    Path = "/v1/shipping/trackers-batch",
    ProviderSubmission = ProviderSubmissionEnum.NOTPERFORMED,
    Readback = ReadbackEnum.ADDTRACKINGPREVIEW,
    SendGuard = new SendGuard
    {
        AccountStatus = AccountStatusEnum.MATCH,
        CaseRef = "case_ref6",
        DisputeMasked = "dispute_masked0",
        BoundDisputeMasked = SendGuardBoundDisputeMasked.FromString("String3"),
        CaseReason = SendGuardCaseReason.FromString("String7"),
        DisputeAmount = SendGuardDisputeAmount.FromProviderMoney(
            new ProviderMoney
            {
                CurrencyCode = "currency_code0",
                MValue = "value6",
            }
        ),
        DisputeReason = SendGuardDisputeReason.FromString("String9"),
        DisputeSellerMasked = SendGuardDisputeSellerMasked.FromString("String1"),
    },
    Source = SourceEnum.PaypalSandbox,
    SubmitFlagEnabled = false,
    ConfirmToken = AddTrackingResponseConfirmToken.FromString("String9"),
    PayloadSha256 = AddTrackingResponsePayloadSha256.FromString("String9"),
    PaypalDebugId = AddTrackingResponsePaypalDebugId.FromString("String9"),
};
```



