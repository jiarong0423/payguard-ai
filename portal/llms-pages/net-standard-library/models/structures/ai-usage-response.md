# Ai Usage Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkFpVXNhZ2VSZXNwb25zZQ

AiUsageResponse.


# Class Name

`AiUsageResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ContentLogged` | `bool?` | Optional | Content logged.<br><br>**Default**: `false` |
| `CostNote` | `string` | Required | Cost note. |
| `Entries` | [`List<AiUsageEntry>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/ai-usage-entry.md) | Required | Entries.<br><br>**Constraints**: *Maximum Items*: `50` |
| `PriceTableSource` | `string` | Required | Price table source. |
| `Source` | [`Source1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/source-1.md) | Required | Source. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

AiUsageResponse aiUsageResponse = new AiUsageResponse
{
    CostNote = "cost_note4",
    Entries = new List<AiUsageEntry>
    {
        new AiUsageEntry
        {
            At = "at6",
            LatencyMs = 254,
            Outcome = OutcomeEnum.Ok,
            Stage = Stage2Enum.StudioAgent,
            EstimatedCostUsd = AiUsageEntryEstimatedCostUsd.FromString("String7"),
            Model = AiUsageEntryModel.FromString("String9"),
            TokensIn = AiUsageEntryTokensIn.FromNumber(196),
            TokensOut = AiUsageEntryTokensOut.FromNumber(54),
            TokensTotal = AiUsageEntryTokensTotal.FromNumber(118),
        },
    },
    PriceTableSource = "price_table_source0",
    Source = Source1Enum.SessionMemory,
    ContentLogged = false,
};
```



