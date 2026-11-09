# Guide Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlRm9ybQ

GuideForm.


# Class Name

`GuideForm`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Kind` | [`Kind2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/kind-2.md) | Required | Kind. |
| `Options` | [`List<GuideOption>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/guide-option.md) | Required | Options. |
| `Placeholder` | [`GuideFormPlaceholder`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-form-placeholder.md) | Required | This is a container for any-of cases. |


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



