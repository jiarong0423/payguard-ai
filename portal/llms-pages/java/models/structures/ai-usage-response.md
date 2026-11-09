# Ai Usage Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkFpVXNhZ2VSZXNwb25zZQ

AiUsageResponse.


# Class Name

`AiUsageResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `ContentLogged` | `Boolean` | Optional | Content logged.<br><br>**Default**: `false` | Boolean getContentLogged() | setContentLogged(Boolean contentLogged) |
| `CostNote` | `String` | Required | Cost note. | String getCostNote() | setCostNote(String costNote) |
| `Entries` | [`List<AiUsageEntry>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/ai-usage-entry.md) | Required | Entries.<br><br>**Constraints**: *Maximum Items*: `50` | List<AiUsageEntry> getEntries() | setEntries(List<AiUsageEntry> entries) |
| `PriceTableSource` | `String` | Required | Price table source. | String getPriceTableSource() | setPriceTableSource(String priceTableSource) |
| `Source` | [`Source1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/source-1.md) | Required | Source. | Source1Enum getSource() | setSource(Source1Enum source) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.AiUsageEntry;
import m18000.m0.m0.m127.models.AiUsageResponse;
import m18000.m0.m0.m127.models.OutcomeEnum;
import m18000.m0.m0.m127.models.Source1Enum;
import m18000.m0.m0.m127.models.Stage2Enum;
import m18000.m0.m0.m127.models.containers.AiUsageEntryEstimatedCostUsd;
import m18000.m0.m0.m127.models.containers.AiUsageEntryModel;
import m18000.m0.m0.m127.models.containers.AiUsageEntryTokensIn;
import m18000.m0.m0.m127.models.containers.AiUsageEntryTokensOut;
import m18000.m0.m0.m127.models.containers.AiUsageEntryTokensTotal;

AiUsageResponse aiUsageResponse = new AiUsageResponse.Builder(
    "cost_note4",
    Arrays.asList(
        new AiUsageEntry.Builder(
            "at6",
            254,
            OutcomeEnum.OK,
            Stage2Enum.STUDIO_AGENT
        )
        .estimatedCostUsd(AiUsageEntryEstimatedCostUsd.fromString(
                "String7"
            ))
        .model(AiUsageEntryModel.fromString(
                "String9"
            ))
        .tokensIn(AiUsageEntryTokensIn.fromNumber(
                196
            ))
        .tokensOut(AiUsageEntryTokensOut.fromNumber(
                54
            ))
        .tokensTotal(AiUsageEntryTokensTotal.fromNumber(
                118
            ))
        .build()
    ),
    "price_table_source0",
    Source1Enum.SESSION_MEMORY
)
.contentLogged(false)
.build();
```



