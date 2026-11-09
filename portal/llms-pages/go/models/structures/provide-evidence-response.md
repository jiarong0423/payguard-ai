# Provide Evidence Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlc3BvbnNl

ProvideEvidenceResponse.


# Class Name

`ProvideEvidenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CaseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `ConfirmToken` | [`*models.ProvideEvidenceResponseConfirmToken`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/provide-evidence-response-confirm-token.md) | Optional | This is a container for any-of cases. |
| `ContentType` | `string` | Required, Constant | Content type.<br><br>**Value**: `"multipart/form-data"` |
| `DataSourceLabel` | [`models.DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/data-source-label.md) | Required | Data source label. |
| `DisputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceClass` | [`models.EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `ExternalSend` | [`models.ExternalSendEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/external-send.md) | Required | External send. |
| `Files` | [`[]models.MultipartFilePart`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/multipart-file-part.md) | Required | Files.<br><br>**Constraints**: *Maximum Items*: `20` |
| `HumanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `"True"` |
| `Input` | [`models.EvidenceInput`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/evidence-input.md) | Required | EvidenceInput. |
| `Method` | `string` | Required, Constant | Method.<br><br>**Value**: `"POST"` |
| `ObservedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `Path` | `string` | Required | Path.<br><br>**Constraints**: *Pattern*: `^/v1/customer/disputes/PP-[A-Z0-9][A-Z0-9-]{2,62}/provide-evidence$` |
| `PayloadSha256` | [`*models.ProvideEvidenceResponsePayloadSha256`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/provide-evidence-response-payload-sha-256.md) | Optional | This is a container for any-of cases. |
| `PaypalDebugId` | [`*models.ProvideEvidenceResponsePaypalDebugId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/provide-evidence-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `ProviderSubmission` | [`models.ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `Readback` | [`models.Readback1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/readback-1.md) | Required | Readback. |
| `SendGuard` | [`models.SendGuard`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). |
| `SentFiles` | [`*models.ProvideEvidenceResponseSentFiles`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/provide-evidence-response-sent-files.md) | Optional | This is a container for any-of cases. |
| `Source` | [`models.SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/source.md) | Required | Source. |
| `SubmitFlagEnabled` | `bool` | Required | Submit flag enabled. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    provideEvidenceResponse := models.ProvideEvidenceResponse{
        CaseRef:             "case_ref2",
        ConfirmToken:        models.ToPointer(models.ProvideEvidenceResponseConfirmTokenContainer.FromString("String9")),
        ContentType:         "multipart/form-data",
        DataSourceLabel:     models.DataSourceLabelEnum_SANDBOX,
        DisputeId:           "dispute_id0",
        Environment:         "sandbox",
        EvidenceClass:       models.EvidenceClassEnum_AUTHENTICSANDBOXRESPONSE,
        ExternalSend:        models.ExternalSendEnum_FROZEN,
        Files:               []models.MultipartFilePart{
            models.MultipartFilePart{
                ByteLength:  68,
                ContentType: models.ContentTypeEnum_ENUMIMAGEPNG,
                Filename:    "filename6",
                Name:        "name4",
            },
        },
        HumanReviewRequired: "True",
        Input:               models.EvidenceInput{
            Evidences: []models.EvidenceInputItem{
                models.EvidenceInputItem{
                    EvidenceInfo: models.EvidenceInfo{
                        TrackingInfo: []models.TrackingInfo{
                            models.TrackingInfo{
                                CarrierName:      models.CarrierNameEnum_DHL,
                                CarrierNameOther: models.ToPointer(models.TrackingInfoCarrierNameOtherContainer.FromString("String1")),
                                TrackingNumber:   "tracking_number6",
                            },
                        },
                    },
                    EvidenceType: "evidence_type2",
                    Notes:        "notes2",
                },
            },
        },
        Method:              "POST",
        ObservedAt:          "observed_at2",
        Path:                "path2",
        PayloadSha256:       models.ToPointer(models.ProvideEvidenceResponsePayloadSha256Container.FromString("String9")),
        PaypalDebugId:       models.ToPointer(models.ProvideEvidenceResponsePaypalDebugIdContainer.FromString("String9")),
        ProviderSubmission:  models.ProviderSubmissionEnum_NOTPERFORMED,
        Readback:            models.Readback1Enum_PROVIDEEVIDENCEPREVIEW,
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
        SentFiles:           models.ToPointer(models.ProvideEvidenceResponseSentFilesContainer.FromArrayOfSentFileFingerprint([]models.SentFileFingerprint{
            models.SentFileFingerprint{
                ByteLength:  196,
                ContentType: models.ContentTypeEnum_ENUMIMAGEPNG,
                Filename:    "filename6",
                Sha256:      "sha2566",
            },
            models.SentFileFingerprint{
                ByteLength:  196,
                ContentType: models.ContentTypeEnum_ENUMIMAGEPNG,
                Filename:    "filename6",
                Sha256:      "sha2566",
            },
            models.SentFileFingerprint{
                ByteLength:  196,
                ContentType: models.ContentTypeEnum_ENUMIMAGEPNG,
                Filename:    "filename6",
                Sha256:      "sha2566",
            },
        })),
        Source:              models.SourceEnum_PAYPALSANDBOX,
        SubmitFlagEnabled:   false,
    }

}
```



