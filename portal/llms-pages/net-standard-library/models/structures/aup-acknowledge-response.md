# Aup Acknowledge Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVzcG9uc2U

AupAcknowledgeResponse.


# Class Name

`AupAcknowledgeResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AcknowledgementToken` | [`AupAcknowledgeResponseAcknowledgementToken`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/aup-acknowledge-response-acknowledgement-token.md) | Required | This is a container for any-of cases. |
| `Choice` | [`ChoiceEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/choice.md) | Required | Choice. |
| `ComplianceDecision` | `string` | Required, Constant | Compliance decision.<br><br>**Value**: `"NOT_MADE"` |
| `DescriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `EvaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `ExpiresAt` | [`AupAcknowledgeResponseExpiresAt`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/aup-acknowledge-response-expires-at.md) | Required | This is a container for any-of cases. |
| `ExternalActionAuthorized` | `string` | Required, Constant | External action authorized.<br><br>**Value**: `"False"` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `WarningCopyVersion` | `string` | Required, Constant | Warning copy version.<br><br>**Value**: `"aup-warning-v1"` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

AupAcknowledgeResponse aupAcknowledgeResponse = new AupAcknowledgeResponse
{
    AcknowledgementToken = AupAcknowledgeResponseAcknowledgementToken.FromString("String9"),
    Choice = ChoiceEnum.ACKNOWLEDGEANDCONTINUE,
    ComplianceDecision = "NOT_MADE",
    DescriptionDigest = "description_digest6",
    EvaluationId = "evaluation_id2",
    ExpiresAt = AupAcknowledgeResponseExpiresAt.FromString("String9"),
    ExternalActionAuthorized = "False",
    Source = "synthetic",
    WarningCopyVersion = "aup-warning-v1",
};
```



