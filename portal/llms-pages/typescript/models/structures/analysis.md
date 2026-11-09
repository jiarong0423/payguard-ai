# Analysis

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkFuYWx5c2lz

Analysis.


# Interface Name

`Analysis`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `reason` | [`AnalysisReason \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/analysis-reason.md) | Optional | This is a container for any-of cases. |
| `status` | [`Status8Enum \| undefined`](http://localhost:3000/llms-pages/typescript/models/enumerations/status-8.md) | Optional | Status. |
| `turn` | `number \| undefined` | Optional | Turn. |


# Example

```ts
import {
  Analysis,
  Reason5Enum,
  Status8Enum,
} from 'tradeglot-local-consolelib';

const analysis: Analysis = {
  reason: Reason5Enum.InvalidReply,
  status: Status8Enum.Replaced,
  turn: 198,
};
```



