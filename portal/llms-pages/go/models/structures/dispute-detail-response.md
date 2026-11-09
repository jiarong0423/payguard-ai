# Dispute Detail Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkRpc3B1dGVEZXRhaWxSZXNwb25zZQ

DisputeDetailResponse.


# Class Name

`DisputeDetailResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CreateTime` | `string` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` |
| `DataSourceLabel` | [`models.DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/data-source-label.md) | Required | Data source label. |
| `DisputeAmount` | [`models.ProviderMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/provider-money.md) | Required | ProviderMoney. |
| `DisputeChannel` | [`*models.DisputeDetailResponseDisputeChannel`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/dispute-detail-response-dispute-channel.md) | Optional | This is a container for any-of cases. |
| `DisputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `DisputeLifeCycleStage` | [`models.DisputeLifeCycleStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `DisputeState` | [`*models.DisputeDetailResponseDisputeState`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/dispute-detail-response-dispute-state.md) | Optional | This is a container for any-of cases. |
| `DisputedTransactions` | [`[]models.DisputedTransaction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/disputed-transaction.md) | Required | Disputed transactions.<br><br>**Constraints**: *Maximum Items*: `10` |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceClass` | [`models.EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `Evidences` | [`[]models.DisputeEvidenceRow`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/dispute-evidence-row.md) | Required | Evidences.<br><br>**Constraints**: *Maximum Items*: `20` |
| `ObservedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `PaypalDebugId` | [`*models.DisputeDetailResponsePaypalDebugId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/dispute-detail-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `ProviderSubmission` | [`models.ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `Readback` | `string` | Required, Constant | Readback.<br><br>**Value**: `"GET_DETAIL"` |
| `Reason` | [`models.Reason2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/reason-2.md) | Required | Reason. |
| `SellerResponseDueDate` | [`*models.DisputeDetailResponseSellerResponseDueDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/dispute-detail-response-seller-response-due-date.md) | Optional | This is a container for any-of cases. |
| `Source` | [`models.SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/source.md) | Required | Source. |
| `Status` | [`models.Status3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/status-3.md) | Required | Status. |
| `UpdateTime` | [`*models.DisputeDetailResponseUpdateTime`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/dispute-detail-response-update-time.md) | Optional | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    disputeDetailResponse := models.DisputeDetailResponse{
        CreateTime:            "create_time6",
        DataSourceLabel:       models.DataSourceLabelEnum_SANDBOX,
        DisputeAmount:         models.ProviderMoney{
            CurrencyCode:         "currency_code6",
            Value:                "value0",
        },
        DisputeChannel:        models.ToPointer(models.DisputeDetailResponseDisputeChannelContainer.FromString("String5")),
        DisputeId:             "dispute_id2",
        DisputeLifeCycleStage: models.DisputeLifeCycleStageEnum_UNKNOWN,
        DisputeState:          models.ToPointer(models.DisputeDetailResponseDisputeStateContainer.FromString("String9")),
        DisputedTransactions:  []models.DisputedTransaction{
            models.DisputedTransaction{
                GrossAmount:              models.ToPointer(models.DisputedTransactionGrossAmountContainer.FromProviderMoney(models.ProviderMoney{
                    CurrencyCode:         "currency_code0",
                    Value:                "value6",
                })),
                SellerProtectionEligible: models.ToPointer(models.DisputedTransactionSellerProtectionEligibleContainer.FromBoolean(true)),
                SellerTransactionId:      "seller_transaction_id2",
                TransactionStatus:        models.ToPointer(models.DisputedTransactionTransactionStatusContainer.FromString("String7")),
            },
        },
        Environment:           "sandbox",
        EvidenceClass:         models.EvidenceClassEnum_SYNTHETICTESTRESPONSE,
        Evidences:             []models.DisputeEvidenceRow{
            models.DisputeEvidenceRow{
                Action:       models.ToPointer(models.DisputeEvidenceRowActionContainer.FromString("String1")),
                Date:         models.ToPointer(models.DisputeEvidenceRowDateContainer.FromString("String9")),
                EvidenceType: "evidence_type2",
                Source:       models.Source3Enum_SUBMITTEDBYPARTNER,
            },
        },
        ObservedAt:            "observed_at4",
        PaypalDebugId:         models.ToPointer(models.DisputeDetailResponsePaypalDebugIdContainer.FromString("String1")),
        ProviderSubmission:    models.ProviderSubmissionEnum_NOTPERFORMED,
        Readback:              "GET_DETAIL",
        Reason:                models.Reason2Enum_MERCHANDISEORSERVICENOTRECEIVED,
        SellerResponseDueDate: models.ToPointer(models.DisputeDetailResponseSellerResponseDueDateContainer.FromString("String9")),
        Source:                models.SourceEnum_PAYPALSANDBOX,
        Status:                models.Status3Enum_CLOSED,
        UpdateTime:            models.ToPointer(models.DisputeDetailResponseUpdateTimeContainer.FromString("String9")),
    }

}
```



