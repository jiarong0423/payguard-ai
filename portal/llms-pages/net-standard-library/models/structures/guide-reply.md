# Guide Reply

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlUmVwbHk

GuideReply.


# Class Name

`GuideReply`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Chooser` | [`ChooserEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/chooser.md) | Required | Chooser. |
| `Dropped` | [`List<GuideDropped>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-dropped.md) | Required | Dropped. |
| `FallbackReason` | [`GuideReplyFallbackReason`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-reply-fallback-reason.md) | Required | This is a container for any-of cases. |
| `StateChanged` | `bool` | Required | State changed. |
| `Template` | [`TemplateEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/template.md) | Required | Template. |
| `Text` | `string` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

GuideReply guideReply = new GuideReply
{
    Chooser = ChooserEnum.None,
    Dropped = new List<GuideDropped>
    {
        new GuideDropped
        {
            Item = "item2",
            Reason = Reason6Enum.OtherParty,
        },
    },
    FallbackReason = GuideReplyFallbackReason.FromFallbackReason(FallbackReasonEnum.Late),
    StateChanged = false,
    Template = TemplateEnum.NOGUARANTEE,
    Text = "text6",
};
```



