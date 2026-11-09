# Guide State Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZQ

GuideStateResponse.


# Interface Name

`GuideStateResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `analysis` | [`GuideStateResponseAnalysis`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-state-response-analysis.md) | Required | This is a container for any-of cases. |
| `asked` | `string[]` | Required | Asked.<br><br>**Constraints**: *Maximum Items*: `3` |
| `autoConfirmed` | `string[]` | Required | Auto confirmed. |
| `chooserMode` | [`ChooserModeEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/chooser-mode.md) | Required | Chooser mode. |
| `deferred` | `string[]` | Required | Deferred. |
| `flowName` | [`GuideStateResponseFlowName`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-state-response-flow-name.md) | Required | This is a container for any-of cases. |
| `formResult` | [`GuideStateResponseFormResult`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-state-response-form-result.md) | Required | This is a container for any-of cases. |
| `formResults` | [`GuideFieldResult[]`](http://localhost:3000/llms-pages/typescript/models/structures/guide-field-result.md) | Required | Form results. |
| `gap` | [`GuideGap`](http://localhost:3000/llms-pages/typescript/models/structures/guide-gap.md) | Required | GuideGap. |
| `goodsType` | [`GuideStateResponseGoodsType`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-state-response-goods-type.md) | Required | This is a container for any-of cases. |
| `items` | [`GuideItem[]`](http://localhost:3000/llms-pages/typescript/models/structures/guide-item.md) | Required | Items. |
| `modelRequested` | `boolean` | Required | Model requested. |
| `modelTextShown` | `string` | Required, Constant | Model text shown.<br><br>**Value**: `'False'` |
| `prefill` | `Record<string, string>` | Required | Prefill. |
| `reply` | [`GuideStateResponseReply`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-state-response-reply.md) | Required | This is a container for any-of cases. |
| `review` | [`GuideReviewRow[]`](http://localhost:3000/llms-pages/typescript/models/structures/guide-review-row.md) | Required | Review. |
| `roundsUsed` | `number` | Required | Rounds used. |
| `scenario` | [`GuideStateResponseScenario`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-state-response-scenario.md) | Required | This is a container for any-of cases. |
| `schemaVersion` | `number` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `stage` | [`GuideStateResponseStage`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-state-response-stage.md) | Required | This is a container for any-of cases. |
| `started` | `boolean` | Required | Started. |
| `subtraction` | [`GuideStateResponseSubtraction`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/guide-state-response-subtraction.md) | Required | This is a container for any-of cases. |
| `turnsLimit` | `number` | Required | Turns limit. |
| `turnsUsed` | `number` | Required | Turns used. |
| `valuesStored` | `string` | Required, Constant | Values stored.<br><br>**Value**: `'False'` |


# Example

```ts
import {
  ChooserEnum,
  ChooserModeEnum,
  FallbackReasonEnum,
  GoodsTypeEnum,
  GuideStateResponse,
  Kind2Enum,
  Reason5Enum,
  Reason6Enum,
  Scenario1Enum,
  Source8Enum,
  Source9Enum,
  Stage3Enum,
  Status8Enum,
  Status9Enum,
  TemplateEnum,
} from 'tradeglot-local-consolelib';

const guideStateResponse: GuideStateResponse = {
  advisoryOnly: 'True',
  analysis: {
    reason: Reason5Enum.InvalidReply,
    status: Status8Enum.Replaced,
    turn: 186,
  },
  asked: [
    'asked6',
    'asked7'
  ],
  autoConfirmed: [
    'auto_confirmed2',
    'auto_confirmed3'
  ],
  chooserMode: ChooserModeEnum.Keyword,
  deferred: [
    'deferred9'
  ],
  flowName: 'String1',
  formResult: {
    item: 'item2',
    valid: false,
  },
  formResults: [
    {
      deferred: false,
      item: 'item6',
      valid: false,
    }
  ],
  gap: {
    conflicting: [
      'conflicting9',
      'conflicting8'
    ],
    missing: [
      'missing2',
      'missing3',
      'missing4'
    ],
    partial: [
      'partial4',
      'partial3',
      'partial2'
    ],
    present: [
      'present7',
      'present8'
    ],
  },
  goodsType: GoodsTypeEnum.Physical,
  items: [
    {
      chunk: 'String9',
      form: {
        kind: Kind2Enum.Choice,
        options: [
          {
            label: 'label2',
            value: 'value4',
          }
        ],
        placeholder: 'String9',
      },
      id: 'id8',
      label: 'label8',
      source: Source8Enum.OFFICIAL,
      status: Status9Enum.MISSING,
    }
  ],
  modelRequested: false,
  modelTextShown: 'False',
  prefill: {
    'key0': 'prefill7',
    'key1': 'prefill8',
    'key2': 'prefill9'
  },
  reply: {
    chooser: ChooserEnum.Form,
    dropped: [
      {
        item: 'item2',
        reason: Reason6Enum.OtherParty,
      }
    ],
    fallbackReason: FallbackReasonEnum.Late,
    stateChanged: false,
    template: TemplateEnum.REVIEW,
    text: 'text0',
  },
  review: [
    {
      item: 'item4',
      source: Source9Enum.Words,
      value: 'value4',
    }
  ],
  roundsUsed: 242,
  scenario: Scenario1Enum.Dispute,
  schemaVersion: 1,
  stage: Stage3Enum.Review,
  started: false,
  subtraction: {
    left: 64,
    needed: 190,
    taken: 178,
    text: 'text0',
  },
  turnsLimit: 230,
  turnsUsed: 128,
  valuesStored: 'False',
};
```



