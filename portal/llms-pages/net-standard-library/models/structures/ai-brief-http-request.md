# Ai Brief Http Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkFpQnJpZWZIdHRwUmVxdWVzdA

What the console may send: the stage and, for disputes, which case. Session facts are never caller input.


# Class Name

`AiBriefHttpRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CaseRef` | [`AiBriefHttpRequestCaseRef`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/ai-brief-http-request-case-ref.md) | Optional | This is a container for any-of cases. |
| `Stage` | [`StageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/stage.md) | Required | Stage. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

AiBriefHttpRequest aiBriefHttpRequest = new AiBriefHttpRequest
{
    Stage = StageEnum.VelocityGuard,
    CaseRef = AiBriefHttpRequestCaseRef.FromString("String9"),
};
```



