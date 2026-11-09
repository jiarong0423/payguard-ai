# Aup Category Signal Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVzcG9uc2U

Optional Channel3 signal shown next to the AUP result; it never changes the rule decision.


# Interface Name

`AupCategorySignalResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `affectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `'False'` |
| `reason` | [`AupCategorySignalResponseReason`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/aup-category-signal-response-reason.md) | Required | This is a container for any-of cases. |
| `signal` | [`AupCategorySignalResponseSignal`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/aup-category-signal-response-signal.md) | Required | This is a container for any-of cases. |
| `status` | [`Status2Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/status-2.md) | Required | Status. |


# Example

```ts
import {
  AupCategorySignalResponse,
  ConfidenceEnum,
  ReasonEnum,
  Status2Enum,
} from 'tradeglot-local-consolelib';

const aupCategorySignalResponse: AupCategorySignalResponse = {
  affectsDecision: 'False',
  reason: ReasonEnum.BudgetExhausted,
  signal: {
    category: 'String9',
    confidence: ConfidenceEnum.HIGH,
    source: 'channel3',
  },
  status: Status2Enum.NOTSENT,
};
```



