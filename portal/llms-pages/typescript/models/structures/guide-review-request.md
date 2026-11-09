# Guide Review Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3UmVxdWVzdA

GuideReviewRequest.


# Interface Name

`GuideReviewRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `change` | `string[] \| undefined` | Optional | Change.<br><br>**Constraints**: *Maximum Items*: `9`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z_]+$` |
| `confirm` | `boolean \| undefined` | Optional | Confirm.<br><br>**Default**: `false` |
| `scenario` | [`GuideReviewRequestScenario \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-review-request-scenario.md) | Optional | This is a container for any-of cases. |


# Example

```ts
import {
  GuideReviewRequest,
  Scenario1Enum,
} from 'tradeglot-local-consolelib';

const guideReviewRequest: GuideReviewRequest = {
  change: [
    'change9',
    'change0',
    'change1'
  ],
  confirm: false,
  scenario: Scenario1Enum.Dispute,
};
```



