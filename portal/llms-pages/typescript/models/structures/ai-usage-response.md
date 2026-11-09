# Ai Usage Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkFpVXNhZ2VSZXNwb25zZQ

AiUsageResponse.


# Interface Name

`AiUsageResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `contentLogged` | `boolean \| undefined` | Optional | Content logged.<br><br>**Default**: `false` |
| `costNote` | `string` | Required | Cost note. |
| `entries` | [`AiUsageEntry[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/ai-usage-entry.md) | Required | Entries.<br><br>**Constraints**: *Maximum Items*: `50` |
| `priceTableSource` | `string` | Required | Price table source. |
| `source` | [`Source1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/source-1.md) | Required | Source. |


# Example

```ts
import {
  AiUsageResponse,
  OutcomeEnum,
  Source1Enum,
  Stage2Enum,
} from 'tradeglot-local-consolelib';

const aiUsageResponse: AiUsageResponse = {
  costNote: 'cost_note4',
  entries: [
    {
      at: 'at6',
      latencyMs: 254,
      outcome: OutcomeEnum.Ok,
      stage: Stage2Enum.StudioAgent,
      estimatedCostUsd: 'String7',
      model: 'String9',
      tokensIn: 196,
      tokensOut: 54,
      tokensTotal: 118,
    }
  ],
  priceTableSource: 'price_table_source0',
  source: Source1Enum.SessionMemory,
  contentLogged: false,
};
```



