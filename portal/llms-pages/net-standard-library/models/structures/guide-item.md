# Guide Item

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlSXRlbQ

GuideItem.


# Class Name

`GuideItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Chunk` | [`GuideItemChunk`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-item-chunk.md) | Required | This is a container for any-of cases. |
| `Form` | [`GuideItemForm`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-item-form.md) | Required | This is a container for any-of cases. |
| `Id` | `string` | Required | Id. |
| `Label` | `string` | Required | Label. |
| `Source` | [`Source8Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/source-8.md) | Required | Source. |
| `Status` | [`Status9Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/status-9.md) | Required | Status. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

GuideItem guideItem = new GuideItem
{
    Chunk = GuideItemChunk.FromString("String7"),
    Form = GuideItemForm.FromGuideForm(
        new GuideForm
        {
            Kind = Kind2Enum.Choice,
            Options = new List<GuideOption>
            {
                new GuideOption
                {
                    Label = "label2",
                    MValue = "value4",
                },
            },
            Placeholder = GuideFormPlaceholder.FromString("String9"),
        }
    ),
    Id = "id0",
    Label = "label0",
    Source = Source8Enum.OFFICIAL,
    Status = Status9Enum.UNCLEAR,
};
```



