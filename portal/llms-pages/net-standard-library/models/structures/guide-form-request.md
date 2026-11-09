# Guide Form Request

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlcXVlc3Q

One field ({item, value}) or one round of up to three fields ({fields: [...]}), never both.


# Class Name

`GuideFormRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ConfirmReview` | `bool?` | Optional | Confirm review.<br><br>**Default**: `false` |
| `Fields` | [`GuideFormRequestFields`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-form-request-fields.md) | Optional | This is a container for any-of cases. |
| `Item` | [`GuideFormRequestItem`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-form-request-item.md) | Optional | This is a container for any-of cases. |
| `Scenario` | [`GuideFormRequestScenario`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-form-request-scenario.md) | Optional | This is a container for any-of cases. |
| `MValue` | [`GuideFormRequestValue`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-form-request-value.md) | Optional | This is a container for any-of cases. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

GuideFormRequest guideFormRequest = new GuideFormRequest
{
    ConfirmReview = false,
    Fields = GuideFormRequestFields.FromListOfGuideField(
        new List<GuideField>
        {
            new GuideField
            {
                Item = "item8",
                MValue = "value8",
            },
        }
    ),
    Item = GuideFormRequestItem.FromString("String1"),
    Scenario = GuideFormRequestScenario.FromScenario1(Scenario1Enum.Preflight),
    MValue = GuideFormRequestValue.FromString("String1"),
};
```



