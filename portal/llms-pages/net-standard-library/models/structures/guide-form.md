# Guide Form

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlRm9ybQ

GuideForm.


# Class Name

`GuideForm`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Kind` | [`Kind2Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/kind-2.md) | Required | Kind. |
| `Options` | [`List<GuideOption>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-option.md) | Required | Options. |
| `Placeholder` | [`GuideFormPlaceholder`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-form-placeholder.md) | Required | This is a container for any-of cases. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

GuideForm guideForm = new GuideForm
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
    Placeholder = GuideFormPlaceholder.FromString("String3"),
};
```



