# Ai Usage Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkFpVXNhZ2VSZXNwb25zZQ

AiUsageResponse.


# Class Name

`AiUsageResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ContentLogged` | `*bool` | Optional | Content logged.<br><br>**Default**: `false` |
| `CostNote` | `string` | Required | Cost note. |
| `Entries` | [`[]models.AiUsageEntry`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/ai-usage-entry.md) | Required | Entries.<br><br>**Constraints**: *Maximum Items*: `50` |
| `PriceTableSource` | `string` | Required | Price table source. |
| `Source` | [`models.Source1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/source-1.md) | Required | Source. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    aiUsageResponse := models.AiUsageResponse{
        ContentLogged:    models.ToPointer(false),
        CostNote:         "cost_note4",
        Entries:          []models.AiUsageEntry{
            models.AiUsageEntry{
                At:               "at6",
                EstimatedCostUsd: models.ToPointer(models.AiUsageEntryEstimatedCostUsdContainer.FromString("String7")),
                LatencyMs:        254,
                Model:            models.ToPointer(models.AiUsageEntryModelContainer.FromString("String9")),
                Outcome:          models.OutcomeEnum_OK,
                Stage:            models.Stage2Enum_STUDIOAGENT,
                TokensIn:         models.ToPointer(models.AiUsageEntryTokensInContainer.FromNumber(196)),
                TokensOut:        models.ToPointer(models.AiUsageEntryTokensOutContainer.FromNumber(54)),
                TokensTotal:      models.ToPointer(models.AiUsageEntryTokensTotalContainer.FromNumber(118)),
            },
        },
        PriceTableSource: "price_table_source0",
        Source:           models.Source1Enum_SESSIONMEMORY,
    }

}
```



