# Provide Evidence Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlc3BvbnNl

ProvideEvidenceResponse.


# Class Name

`ProvideEvidenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CaseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `ConfirmToken` | [`ProvideEvidenceResponseConfirmToken`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/provide-evidence-response-confirm-token.md) | Optional | This is a container for any-of cases. |
| `ContentType` | `string` | Required, Constant | Content type.<br><br>**Value**: `"multipart/form-data"` |
| `DataSourceLabel` | [`DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/data-source-label.md) | Required | Data source label. |
| `DisputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceClass` | [`EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `ExternalSend` | [`ExternalSendEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/external-send.md) | Required | External send. |
| `Files` | [`List<MultipartFilePart>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/multipart-file-part.md) | Required | Files.<br><br>**Constraints**: *Maximum Items*: `20` |
| `HumanReviewRequired` | `string` | Required, Constant | Human review required.<br><br>**Value**: `"True"` |
| `Input` | [`EvidenceInput`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/evidence-input.md) | Required | EvidenceInput. |
| `Method` | `string` | Required, Constant | Method.<br><br>**Value**: `"POST"` |
| `ObservedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `Path` | `string` | Required | Path.<br><br>**Constraints**: *Pattern*: `^/v1/customer/disputes/PP-[A-Z0-9][A-Z0-9-]{2,62}/provide-evidence$` |
| `PayloadSha256` | [`ProvideEvidenceResponsePayloadSha256`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/provide-evidence-response-payload-sha-256.md) | Optional | This is a container for any-of cases. |
| `PaypalDebugId` | [`ProvideEvidenceResponsePaypalDebugId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/provide-evidence-response-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `ProviderSubmission` | [`ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `Readback` | [`Readback1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/readback-1.md) | Required | Readback. |
| `SendGuard` | [`SendGuard`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). |
| `Source` | [`SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/source.md) | Required | Source. |
| `SubmitFlagEnabled` | `bool` | Required | Submit flag enabled. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

ProvideEvidenceResponse provideEvidenceResponse = new ProvideEvidenceResponse
{
    CaseRef = "case_ref2",
    ContentType = "multipart/form-data",
    DataSourceLabel = DataSourceLabelEnum.Sandbox,
    DisputeId = "dispute_id0",
    Environment = "sandbox",
    EvidenceClass = EvidenceClassEnum.AUTHENTICSANDBOXRESPONSE,
    ExternalSend = ExternalSendEnum.FROZEN,
    Files = new List<MultipartFilePart>
    {
        new MultipartFilePart
        {
            ByteLength = 68,
            ContentType = ContentTypeEnum.EnumImagepng,
            Filename = "filename6",
            Name = "name4",
        },
    },
    HumanReviewRequired = "True",
    Input = new EvidenceInput
    {
        Evidences = new List<EvidenceInputItem>
        {
            new EvidenceInputItem
            {
                EvidenceInfo = new EvidenceInfo
                {
                    TrackingInfo = new List<TrackingInfo>
                    {
                        new TrackingInfo
                        {
                            CarrierName = CarrierNameEnum.DHL,
                            TrackingNumber = "tracking_number6",
                            CarrierNameOther = TrackingInfoCarrierNameOther.FromString("String1"),
                        },
                    },
                },
                EvidenceType = "evidence_type2",
                Notes = "notes2",
            },
        },
    },
    Method = "POST",
    ObservedAt = "observed_at2",
    Path = "path2",
    ProviderSubmission = ProviderSubmissionEnum.NOTPERFORMED,
    Readback = Readback1Enum.PROVIDEEVIDENCEPREVIEW,
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
    ConfirmToken = ProvideEvidenceResponseConfirmToken.FromString("String9"),
    PayloadSha256 = ProvideEvidenceResponsePayloadSha256.FromString("String9"),
    PaypalDebugId = ProvideEvidenceResponsePaypalDebugId.FromString("String9"),
};
```



