# Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlNpZ25hbA

Signal.


# Class Name

`Signal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Category` | [`SignalCategory`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/signal-category.md) | Optional | This is a container for any-of cases. |
| `Confidence` | [`SignalConfidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/signal-confidence.md) | Optional | This is a container for any-of cases. |
| `Source` | [`Source2Enum?`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/source-2.md) | Optional | Source. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

Signal signal = new Signal
{
    Category = SignalCategory.FromString("String1"),
    Confidence = SignalConfidence.FromConfidence(ConfidenceEnum.HIGH),
    Source = Source2Enum.Channel3,
};
```



