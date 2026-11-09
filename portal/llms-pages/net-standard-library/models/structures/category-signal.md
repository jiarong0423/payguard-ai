# Category Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkNhdGVnb3J5U2lnbmFs

CategorySignal.


# Class Name

`CategorySignal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Category` | [`CategorySignalCategory`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/category-signal-category.md) | Required | This is a container for any-of cases. |
| `Confidence` | [`CategorySignalConfidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/category-signal-confidence.md) | Required | This is a container for any-of cases. |
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



