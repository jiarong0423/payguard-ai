# Provide Evidence Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlcXVlc3Q

ProvideEvidenceRequest.


# Class Name

`ProvideEvidenceRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CaseRef` | `string` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `ConfirmToken` | [`ProvideEvidenceRequestConfirmToken`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/provide-evidence-request-confirm-token.md) | Optional | This is a container for any-of cases. |
| `DisputeId` | `string` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `Submit` | `bool?` | Optional | Submit.<br><br>**Default**: `false` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

ProvideEvidenceRequest provideEvidenceRequest = new ProvideEvidenceRequest
{
    CaseRef = "case_ref0",
    DisputeId = "dispute_id8",
    ConfirmToken = ProvideEvidenceRequestConfirmToken.FromString("String7"),
    Submit = false,
};
```



