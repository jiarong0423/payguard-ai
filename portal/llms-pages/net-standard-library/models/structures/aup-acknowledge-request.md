# Aup Acknowledge Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVxdWVzdA

AupAcknowledgeRequest.


# Class Name

`AupAcknowledgeRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Choice` | [`ChoiceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/choice.md) | Required | Choice. |
| `DescriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `EvaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

AupAcknowledgeRequest aupAcknowledgeRequest = new AupAcknowledgeRequest
{
    Choice = ChoiceEnum.ACKNOWLEDGEANDCONTINUE,
    DescriptionDigest = "description_digest0",
    EvaluationId = "evaluation_id6",
};
```



