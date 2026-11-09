# Guide Turn Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkd1aWRlVHVyblJlcXVlc3Q

GuideTurnRequest.


# Interface Name

`GuideTurnRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `fields` | [`GuideTurnRequestFields \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/guide-turn-request-fields.md) | Optional | This is a container for any-of cases. |
| `scenario` | [`GuideTurnRequestScenario \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/guide-turn-request-scenario.md) | Optional | This is a container for any-of cases. |
| `text` | `string` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1600` |


# Example

```ts
import { GuideTurnRequest, Scenario1Enum } from 'tradeglot-local-consolelib';

const guideTurnRequest: GuideTurnRequest = {
  text: 'text2',
  fields: [
    {
    item: 'item8',
    value: 'value8',
  }
  ],
  scenario: Scenario1Enum.Preflight,
};
```



