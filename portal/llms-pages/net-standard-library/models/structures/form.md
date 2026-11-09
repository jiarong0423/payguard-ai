# Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkZvcm0

Form.


# Class Name

`Form`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Kind` | [`Kind2Enum?`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/kind-2.md) | Optional | Kind. |
| `Options` | [`List<GuideOption>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/guide-option.md) | Optional | Options. |
| `Placeholder` | [`FormPlaceholder`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/form-placeholder.md) | Optional | This is a container for any-of cases. |


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



