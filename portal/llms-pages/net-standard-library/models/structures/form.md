# Form

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkZvcm0

Form.


# Class Name

`Form`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Kind` | [`Kind2Enum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/kind-2.md) | Optional | Kind. |
| `Options` | [`List<GuideOption>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-option.md) | Optional | Options. |
| `Placeholder` | [`FormPlaceholder`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/form-placeholder.md) | Optional | This is a container for any-of cases. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

Form form = new Form
{
    Kind = Kind2Enum.Text,
    Options = new List<GuideOption>
    {
        new GuideOption
        {
            Label = "label2",
            MValue = "value4",
        },
        new GuideOption
        {
            Label = "label2",
            MValue = "value4",
        },
        new GuideOption
        {
            Label = "label2",
            MValue = "value4",
        },
    },
    Placeholder = FormPlaceholder.FromString("String9"),
};
```



