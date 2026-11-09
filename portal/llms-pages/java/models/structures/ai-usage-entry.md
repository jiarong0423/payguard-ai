# Ai Usage Entry

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkFpVXNhZ2VFbnRyeQ

AiUsageEntry.


# Class Name

`AiUsageEntry`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `At` | `String` | Required | At. | String getAt() | setAt(String at) |
| `EstimatedCostUsd` | [`AiUsageEntryEstimatedCostUsd`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/ai-usage-entry-estimated-cost-usd.md) | Optional | This is a container for any-of cases. | AiUsageEntryEstimatedCostUsd getEstimatedCostUsd() | setEstimatedCostUsd(AiUsageEntryEstimatedCostUsd estimatedCostUsd) |
| `LatencyMs` | `int` | Required | Latency ms.<br><br>**Constraints**: `>= 0`, `<= 3600000` | int getLatencyMs() | setLatencyMs(int latencyMs) |
| `Model` | [`AiUsageEntryModel`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/ai-usage-entry-model.md) | Optional | This is a container for any-of cases. | AiUsageEntryModel getModel() | setModel(AiUsageEntryModel model) |
| `Outcome` | [`OutcomeEnum`](http://localhost:3000/llms-pages/java/models/enumerations/outcome.md) | Required | Outcome. | OutcomeEnum getOutcome() | setOutcome(OutcomeEnum outcome) |
| `Stage` | [`Stage2Enum`](http://localhost:3000/llms-pages/java/models/enumerations/stage-2.md) | Required | Stage. | Stage2Enum getStage() | setStage(Stage2Enum stage) |
| `TokensIn` | [`AiUsageEntryTokensIn`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/ai-usage-entry-tokens-in.md) | Optional | This is a container for any-of cases. | AiUsageEntryTokensIn getTokensIn() | setTokensIn(AiUsageEntryTokensIn tokensIn) |
| `TokensOut` | [`AiUsageEntryTokensOut`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/ai-usage-entry-tokens-out.md) | Optional | This is a container for any-of cases. | AiUsageEntryTokensOut getTokensOut() | setTokensOut(AiUsageEntryTokensOut tokensOut) |
| `TokensTotal` | [`AiUsageEntryTokensTotal`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/ai-usage-entry-tokens-total.md) | Optional | This is a container for any-of cases. | AiUsageEntryTokensTotal getTokensTotal() | setTokensTotal(AiUsageEntryTokensTotal tokensTotal) |


# Example

```java
import m18000.m0.m0.m127.models.AiUsageEntry;
import m18000.m0.m0.m127.models.OutcomeEnum;
import m18000.m0.m0.m127.models.Stage2Enum;
import m18000.m0.m0.m127.models.containers.AiUsageEntryEstimatedCostUsd;
import m18000.m0.m0.m127.models.containers.AiUsageEntryModel;
import m18000.m0.m0.m127.models.containers.AiUsageEntryTokensIn;
import m18000.m0.m0.m127.models.containers.AiUsageEntryTokensOut;
import m18000.m0.m0.m127.models.containers.AiUsageEntryTokensTotal;

AiUsageEntry aiUsageEntry = new AiUsageEntry.Builder(
    "at4",
    38,
    OutcomeEnum.OK,
    Stage2Enum.VELOCITY_GUARD
)
.estimatedCostUsd(AiUsageEntryEstimatedCostUsd.fromString(
        "String5"
    ))
.model(AiUsageEntryModel.fromString(
        "String7"
    ))
.tokensIn(AiUsageEntryTokensIn.fromNumber(
        236
    ))
.tokensOut(AiUsageEntryTokensOut.fromNumber(
        94
    ))
.tokensTotal(AiUsageEntryTokensTotal.fromNumber(
        158
    ))
.build();
```



