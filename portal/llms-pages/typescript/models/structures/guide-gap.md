# Guide Gap

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkd1aWRlR2Fw

GuideGap.


# Interface Name

`GuideGap`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `conflicting` | `string[]` | Required | Conflicting. |
| `missing` | `string[]` | Required | Missing. |
| `partial` | `string[]` | Required | Partial. |
| `present` | `string[]` | Required | Present. |


# Example

```ts
import { GuideGap } from 'tradeglot-local-consolelib';

const guideGap: GuideGap = {
  conflicting: [
    'conflicting9'
  ],
  missing: [
    'missing4'
  ],
  partial: [
    'partial4',
    'partial5'
  ],
  present: [
    'present9',
    'present0',
    'present1'
  ],
};
```



