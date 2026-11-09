# Signal

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlNpZ25hbA

Signal.


# Class Name

`Signal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Category` | [`SignalCategory`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/signal-category.md) | Optional | This is a container for any-of cases. |
| `Confidence` | [`SignalConfidence`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/signal-confidence.md) | Optional | This is a container for any-of cases. |
| `Source` | [`Source2Enum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/source-2.md) | Optional | Source. |


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



