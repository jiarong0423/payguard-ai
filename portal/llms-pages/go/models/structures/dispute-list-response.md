# Dispute List Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkRpc3B1dGVMaXN0UmVzcG9uc2U

DisputeListResponse.


# Class Name

`DisputeListResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `DataSourceLabel` | [`models.DataSourceLabelEnum`](http://localhost:3000/llms-pages/go/models/enumerations/data-source-label.md) | Required | Data source label. |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceClass` | [`models.EvidenceClassEnum`](http://localhost:3000/llms-pages/go/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `Items` | [`[]models.DisputeRecord`](http://localhost:3000/llms-pages/go/models/structures/dispute-record.md) | Required | Items.<br><br>**Constraints**: *Maximum Items*: `20` |
| `ObservedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `PaypalDebugId` | [`*models.DisputeListResponsePaypalDebugId`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/dispute-list-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `ProviderSubmission` | [`models.ProviderSubmissionEnum`](http://localhost:3000/llms-pages/go/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `Readback` | `string` | Required, Constant | Readback.<br><br>**Value**: `"GET_LIST"` |
| `Source` | [`models.SourceEnum`](http://localhost:3000/llms-pages/go/models/enumerations/source.md) | Required | Source. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    disputeListResponse := models.DisputeListResponse{
        DataSourceLabel:    models.DataSourceLabelEnum_SANDBOX,
        Environment:        "sandbox",
        EvidenceClass:      models.EvidenceClassEnum_SYNTHETICTESTRESPONSE,
        Items:              []models.DisputeRecord{
            models.DisputeRecord{
                CreateTime:            "create_time4",
                DisputeAmount:         models.ProviderMoney{
                    CurrencyCode:         "currency_code6",
                    Value:                "value0",
                },
                DisputeId:             "dispute_id0",
                DisputeLifeCycleStage: models.DisputeLifeCycleStageEnum_PREARBITRATION,
                DisputeState:          models.ToPointer(models.DisputeRecordDisputeStateContainer.FromString("String1")),
                Reason:                models.Reason2Enum_CREDITNOTPROCESSED,
                SellerResponseDueDate: models.ToPointer(models.DisputeRecordSellerResponseDueDateContainer.FromString("String7")),
                Status:                models.Status3Enum_UNDERREVIEW,
                UpdateTime:            models.ToPointer(models.DisputeRecordUpdateTimeContainer.FromString("String1")),
            },
        },
        ObservedAt:         "observed_at4",
        PaypalDebugId:      models.ToPointer(models.DisputeListResponsePaypalDebugIdContainer.FromString("String1")),
        ProviderSubmission: models.ProviderSubmissionEnum_NOTPERFORMED,
        Readback:           "GET_LIST",
        Source:             models.SourceEnum_PAYPALSANDBOX,
    }

}
```



