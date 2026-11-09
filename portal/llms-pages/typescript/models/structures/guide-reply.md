# Guide Reply

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkd1aWRlUmVwbHk

GuideReply.


# Interface Name

`GuideReply`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chooser` | [`ChooserEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/chooser.md) | Required | Chooser. |
| `dropped` | [`GuideDropped[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/guide-dropped.md) | Required | Dropped. |
| `fallbackReason` | [`GuideReplyFallbackReason`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/guide-reply-fallback-reason.md) | Required | This is a container for any-of cases. |
| `stateChanged` | `boolean` | Required | State changed. |
| `template` | [`TemplateEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/template.md) | Required | Template. |
| `text` | `string` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` |


# Example

```ts
import {
  ChooserEnum,
  FallbackReasonEnum,
  GuideReply,
  Reason6Enum,
  TemplateEnum,
} from 'tradeglot-local-consolelib';

const guideReply: GuideReply = {
  chooser: ChooserEnum.None,
  dropped: [
    {
      item: 'item2',
      reason: Reason6Enum.OtherParty,
    }
  ],
  fallbackReason: FallbackReasonEnum.Late,
  stateChanged: false,
  template: TemplateEnum.NOGUARANTEE,
  text: 'text6',
};
```



