# Time Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlRpbWVFdmVudA

TimeEvent.


# Class Name

`TimeEvent`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `At` | `string` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `Kind` | [`KindEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/kind.md) | Required | Kind. |
| `Source` | [`Source5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/source-5.md) | Required | Source. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

TimeEvent timeEvent = new TimeEvent
{
    At = "at6",
    Kind = KindEnum.DELIVERY,
    Source = Source5Enum.PROVIDER,
};
```



