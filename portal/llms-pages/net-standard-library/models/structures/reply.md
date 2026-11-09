# Reply

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlJlcGx5

Reply.


# Class Name

`Reply`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Chooser` | [`ChooserEnum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/chooser.md) | Optional | Chooser. |
| `Dropped` | [`List<GuideDropped>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-dropped.md) | Optional | Dropped. |
| `FallbackReason` | [`ReplyFallbackReason`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/reply-fallback-reason.md) | Optional | This is a container for any-of cases. |
| `StateChanged` | `bool?` | Optional | State changed. |
| `Template` | [`TemplateEnum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/template.md) | Optional | Template. |
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



