# Reply

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlJlcGx5

Reply.


# Interface Name

`Reply`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chooser` | [`ChooserEnum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/chooser.md) | Optional | Chooser. |
| `dropped` | [`GuideDropped[] \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/guide-dropped.md) | Optional | Dropped. |
| `fallbackReason` | [`ReplyFallbackReason \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/reply-fallback-reason.md) | Optional | This is a container for any-of cases. |
| `stateChanged` | `boolean \| undefined` | Optional | State changed. |
| `template` | [`TemplateEnum \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/template.md) | Optional | Template. |
| `text` | `string \| undefined` | Optional | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` |


# Example

```ts
import {
  ChooserEnum,
  FallbackReasonEnum,
  Reason6Enum,
  Reply,
  TemplateEnum,
} from 'tradeglot-local-consolelib';

const reply: Reply = {
  chooser: ChooserEnum.Keyword,
  dropped: [
    {
      item: 'item2',
      reason: Reason6Enum.OtherParty,
    },
    {
      item: 'item2',
      reason: Reason6Enum.OtherParty,
    }
  ],
  fallbackReason: FallbackReasonEnum.ProviderError,
  stateChanged: false,
  template: TemplateEnum.SUBTRACTION,
};
```



