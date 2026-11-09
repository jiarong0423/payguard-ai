# Reply

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlJlcGx5

Reply.


# Class Name

`Reply`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Chooser` | [`ChooserEnum?`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/chooser.md) | Optional | Chooser. |
| `Dropped` | [`List<GuideDropped>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/guide-dropped.md) | Optional | Dropped. |
| `FallbackReason` | [`ReplyFallbackReason`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/reply-fallback-reason.md) | Optional | This is a container for any-of cases. |
| `StateChanged` | `bool?` | Optional | State changed. |
| `Template` | [`TemplateEnum?`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/template.md) | Optional | Template. |
| `Text` | `string` | Optional | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

Reply reply = new Reply
{
    Chooser = ChooserEnum.Keyword,
    Dropped = new List<GuideDropped>
    {
        new GuideDropped
        {
            Item = "item2",
            Reason = Reason6Enum.OtherParty,
        },
        new GuideDropped
        {
            Item = "item2",
            Reason = Reason6Enum.OtherParty,
        },
    },
    FallbackReason = ReplyFallbackReason.FromFallbackReason(FallbackReasonEnum.ProviderError),
    StateChanged = false,
    Template = TemplateEnum.SUBTRACTION,
};
```



