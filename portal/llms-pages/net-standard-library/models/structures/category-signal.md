# Category Signal

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkNhdGVnb3J5U2lnbmFs

CategorySignal.


# Class Name

`CategorySignal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Category` | [`CategorySignalCategory`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/category-signal-category.md) | Required | This is a container for any-of cases. |
| `Confidence` | [`CategorySignalConfidence`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/category-signal-confidence.md) | Required | This is a container for any-of cases. |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"channel3"` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

CategorySignal categorySignal = new CategorySignal
{
    Category = CategorySignalCategory.FromString("String1"),
    Confidence = CategorySignalConfidence.FromConfidence(ConfidenceEnum.HIGH),
    Source = "channel3",
};
```



