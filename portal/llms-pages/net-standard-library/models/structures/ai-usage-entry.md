# Ai Usage Entry

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkFpVXNhZ2VFbnRyeQ

AiUsageEntry.


# Class Name

`AiUsageEntry`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `At` | `string` | Required | At. |
| `EstimatedCostUsd` | [`AiUsageEntryEstimatedCostUsd`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/ai-usage-entry-estimated-cost-usd.md) | Optional | This is a container for any-of cases. |
| `LatencyMs` | `int` | Required | Latency ms.<br><br>**Constraints**: `>= 0`, `<= 3600000` |
| `Model` | [`AiUsageEntryModel`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/ai-usage-entry-model.md) | Optional | This is a container for any-of cases. |
| `Outcome` | [`OutcomeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/outcome.md) | Required | Outcome. |
| `Stage` | [`Stage2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/stage-2.md) | Required | Stage. |
| `TokensIn` | [`AiUsageEntryTokensIn`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/ai-usage-entry-tokens-in.md) | Optional | This is a container for any-of cases. |
| `TokensOut` | [`AiUsageEntryTokensOut`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/ai-usage-entry-tokens-out.md) | Optional | This is a container for any-of cases. |
| `TokensTotal` | [`AiUsageEntryTokensTotal`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/ai-usage-entry-tokens-total.md) | Optional | This is a container for any-of cases. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

AiUsageEntry aiUsageEntry = new AiUsageEntry
{
    At = "at4",
    LatencyMs = 38,
    Outcome = OutcomeEnum.Ok,
    Stage = Stage2Enum.VelocityGuard,
    EstimatedCostUsd = AiUsageEntryEstimatedCostUsd.FromString("String5"),
    Model = AiUsageEntryModel.FromString("String7"),
    TokensIn = AiUsageEntryTokensIn.FromNumber(236),
    TokensOut = AiUsageEntryTokensOut.FromNumber(94),
    TokensTotal = AiUsageEntryTokensTotal.FromNumber(158),
};
```



