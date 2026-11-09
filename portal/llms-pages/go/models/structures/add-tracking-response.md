# Add Tracking Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkFkZFRyYWNraW5nUmVzcG9uc2U

AddTrackingResponse.


# Class Name

`AddTrackingResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Body` | [`models.TrackerBatch`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/tracker-batch.md) | Required | TrackerBatch. |
| `CaseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `ConfirmToken` | [`*models.AddTrackingResponseConfirmToken`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/add-tracking-response-confirm-token.md) | Optional | This is a container for any-of cases. |
| `ContentType` | `string` | Required, Constant | Content type.<br><br>**Value**: `"application/json"` |
| `DataSourceLabel` | [`models.DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/data-source-label.md) | Required | Data source label. |
| `DisputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceClass` | [`models.EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `ExternalSend` | [`models.ExternalSendEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/external-send.md) | Required | External send. |
| `HumanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `"True"` |
| `Method` | `string` | Required, Constant | Method.<br><br>**Value**: `"POST"` |
| `ObservedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `Path` | `string` | Required, Constant | Path.<br><br>**Value**: `"/v1/shipping/trackers-batch"` |
| `PayloadSha256` | [`*models.AddTrackingResponsePayloadSha256`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/add-tracking-response-payload-sha-256.md) | Optional | This is a container for any-of cases. |
| `PaypalDebugId` | [`*models.AddTrackingResponsePaypalDebugId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/add-tracking-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `ProviderSubmission` | [`models.ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `Readback` | [`models.ReadbackEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/readback.md) | Required | Readback. |
| `SendGuard` | [`models.SendGuard`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). |
| `Source` | [`models.SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/source.md) | Required | Source. |
| `SubmitFlagEnabled` | `bool` | Required | Submit flag enabled. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    addTrackingResponse := models.AddTrackingResponse{
        Body:                models.TrackerBatch{
            Trackers: []models.TrackerItem{
                models.TrackerItem{
                    Carrier:          models.CarrierEnum_JPJAPANPOST,
                    CarrierNameOther: models.ToPointer(models.TrackerItemCarrierNameOtherContainer.FromString("String5")),
                    Status:           "SHIPPED",
                    TrackingNumber:   "tracking_number0",
                    TransactionId:    "transaction_id0",
                },
            },
        },
        CaseRef:             "case_ref6",
        ConfirmToken:        models.ToPointer(models.AddTrackingResponseConfirmTokenContainer.FromString("String9")),
        ContentType:         "application/json",
        DataSourceLabel:     models.DataSourceLabelEnum_SANDBOX,
        DisputeId:           "dispute_id4",
        Environment:         "sandbox",
        EvidenceClass:       models.EvidenceClassEnum_AUTHENTICSANDBOXRESPONSE,
        ExternalSend:        models.ExternalSendEnum_FROZEN,
        HumanReviewRequired: "True",
        Method:              "POST",
        ObservedAt:          "observed_at6",
        Path:                "/v1/shipping/trackers-batch",
        PayloadSha256:       models.ToPointer(models.AddTrackingResponsePayloadSha256Container.FromString("String9")),
        PaypalDebugId:       models.ToPointer(models.AddTrackingResponsePaypalDebugIdContainer.FromString("String9")),
        ProviderSubmission:  models.ProviderSubmissionEnum_NOTPERFORMED,
        Readback:            models.ReadbackEnum_ADDTRACKINGPREVIEW,
        SendGuard:           models.SendGuard{
            AccountStatus:        models.AccountStatusEnum_MATCH,
            BoundDisputeMasked:   models.ToPointer(models.SendGuardBoundDisputeMaskedContainer.FromString("String3")),
            CaseReason:           models.ToPointer(models.SendGuardCaseReasonContainer.FromString("String7")),
            CaseRef:              "case_ref6",
            DisputeAmount:        models.ToPointer(models.SendGuardDisputeAmountContainer.FromProviderMoney(models.ProviderMoney{
                CurrencyCode:         "currency_code0",
                Value:                "value6",
            })),
            DisputeMasked:        "dispute_masked0",
            DisputeReason:        models.ToPointer(models.SendGuardDisputeReasonContainer.FromString("String9")),
            DisputeSellerMasked:  models.ToPointer(models.SendGuardDisputeSellerMaskedContainer.FromString("String1")),
        },
        Source:              models.SourceEnum_PAYPALSANDBOX,
        SubmitFlagEnabled:   false,
    }

}
```



