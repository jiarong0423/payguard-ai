# Ai Usage Entry

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkFpVXNhZ2VFbnRyeQ

AiUsageEntry.


# Class Name

`AiUsageEntry`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `At` | `string` | Required | At. |
| `EstimatedCostUsd` | [`*models.AiUsageEntryEstimatedCostUsd`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/ai-usage-entry-estimated-cost-usd.md) | Optional | This is a container for any-of cases. |
| `LatencyMs` | `int` | Required | Latency ms.<br><br>**Constraints**: `>= 0`, `<= 3600000` |
| `Model` | [`*models.AiUsageEntryModel`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/ai-usage-entry-model.md) | Optional | This is a container for any-of cases. |
| `Outcome` | [`models.OutcomeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/outcome.md) | Required | Outcome. |
| `Stage` | [`models.Stage2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/stage-2.md) | Required | Stage. |
| `TokensIn` | [`*models.AiUsageEntryTokensIn`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/ai-usage-entry-tokens-in.md) | Optional | This is a container for any-of cases. |
| `TokensOut` | [`*models.AiUsageEntryTokensOut`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/ai-usage-entry-tokens-out.md) | Optional | This is a container for any-of cases. |
| `TokensTotal` | [`*models.AiUsageEntryTokensTotal`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/ai-usage-entry-tokens-total.md) | Optional | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    aiUsageEntry := models.AiUsageEntry{
        At:               "at4",
        EstimatedCostUsd: models.ToPointer(models.AiUsageEntryEstimatedCostUsdContainer.FromString("String5")),
        LatencyMs:        38,
        Model:            models.ToPointer(models.AiUsageEntryModelContainer.FromString("String7")),
        Outcome:          models.OutcomeEnum_OK,
        Stage:            models.Stage2Enum_VELOCITYGUARD,
        TokensIn:         models.ToPointer(models.AiUsageEntryTokensInContainer.FromNumber(236)),
        TokensOut:        models.ToPointer(models.AiUsageEntryTokensOutContainer.FromNumber(94)),
        TokensTotal:      models.ToPointer(models.AiUsageEntryTokensTotalContainer.FromNumber(158)),
    }

}
```



