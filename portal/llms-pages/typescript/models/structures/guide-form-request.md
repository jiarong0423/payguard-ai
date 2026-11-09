# Guide Form Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlcXVlc3Q

One field ({item, value}) or one round of up to three fields ({fields: [...]}), never both.


# Interface Name

`GuideFormRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `confirmReview` | `boolean \| undefined` | Optional | Confirm review.<br><br>**Default**: `false` |
| `fields` | [`GuideFormRequestFields \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-form-request-fields.md) | Optional | This is a container for any-of cases. |
| `item` | [`GuideFormRequestItem \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-form-request-item.md) | Optional | This is a container for any-of cases. |
| `scenario` | [`GuideFormRequestScenario \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-form-request-scenario.md) | Optional | This is a container for any-of cases. |
| `value` | [`GuideFormRequestValue \| undefined`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-form-request-value.md) | Optional | This is a container for any-of cases. |


# Example

```ts
import { GuideFormRequest, Scenario1Enum } from 'tradeglot-local-consolelib';

const guideFormRequest: GuideFormRequest = {
  confirmReview: false,
  fields: [
    {
    item: 'item8',
    value: 'value8',
  }
  ],
  item: 'String1',
  scenario: Scenario1Enum.Preflight,
  value: 'String1',
};
```



