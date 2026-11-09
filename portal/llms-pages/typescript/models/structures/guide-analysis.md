# Guide Analysis

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkd1aWRlQW5hbHlzaXM

GuideAnalysis.


# Interface Name

`GuideAnalysis`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `reason` | [`GuideAnalysisReason`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-analysis-reason.md) | Required | This is a container for any-of cases. |
| `status` | [`Status8Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/status-8.md) | Required | Status. |
| `turn` | `number` | Required | Turn. |


# Example

```ts
import {
  GuideAnalysis,
  Reason5Enum,
  Status8Enum,
} from 'tradeglot-local-consolelib';

const guideAnalysis: GuideAnalysis = {
  reason: Reason5Enum.InvalidReply,
  status: Status8Enum.Analysing,
  turn: 236,
};
```



