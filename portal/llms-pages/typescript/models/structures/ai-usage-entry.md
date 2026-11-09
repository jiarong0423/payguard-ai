# Ai Usage Entry

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkFpVXNhZ2VFbnRyeQ

AiUsageEntry.


# Interface Name

`AiUsageEntry`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `string` | Required | At. |
| `estimatedCostUsd` | [`AiUsageEntryEstimatedCostUsd \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/ai-usage-entry-estimated-cost-usd.md) | Optional | This is a container for any-of cases. |
| `latencyMs` | `number` | Required | Latency ms.<br><br>**Constraints**: `>= 0`, `<= 3600000` |
| `model` | [`AiUsageEntryModel \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/ai-usage-entry-model.md) | Optional | This is a container for any-of cases. |
| `outcome` | [`OutcomeEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/outcome.md) | Required | Outcome. |
| `stage` | [`Stage2Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/stage-2.md) | Required | Stage. |
| `tokensIn` | [`AiUsageEntryTokensIn \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/ai-usage-entry-tokens-in.md) | Optional | This is a container for any-of cases. |
| `tokensOut` | [`AiUsageEntryTokensOut \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/ai-usage-entry-tokens-out.md) | Optional | This is a container for any-of cases. |
| `tokensTotal` | [`AiUsageEntryTokensTotal \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/ai-usage-entry-tokens-total.md) | Optional | This is a container for any-of cases. |


# Example

```ts
import {
  AiUsageEntry,
  OutcomeEnum,
  Stage2Enum,
} from 'tradeglot-local-consolelib';

const aiUsageEntry: AiUsageEntry = {
  at: 'at4',
  latencyMs: 38,
  outcome: OutcomeEnum.Ok,
  stage: Stage2Enum.VelocityGuard,
  estimatedCostUsd: 'String5',
  model: 'String7',
  tokensIn: 236,
  tokensOut: 94,
  tokensTotal: 158,
};
```



