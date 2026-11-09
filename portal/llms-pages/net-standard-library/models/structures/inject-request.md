# Inject Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkluamVjdFJlcXVlc3Q

InjectRequest.


# Class Name

`InjectRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Scenario` | [`Scenario5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/scenario-5.md) | Required | Scenario. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

InjectRequest injectRequest = new InjectRequest
{
    Scenario = Scenario5Enum.Burst,
};
```



