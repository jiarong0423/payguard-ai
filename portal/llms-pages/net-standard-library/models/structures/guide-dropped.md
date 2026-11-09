# Guide Dropped

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlRHJvcHBlZA

GuideDropped.


# Class Name

`GuideDropped`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Item` | `string` | Required | Item. |
| `Reason` | [`Reason6Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/reason-6.md) | Required | Reason. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

GuideDropped guideDropped = new GuideDropped
{
    Item = "item6",
    Reason = Reason6Enum.OtherParty,
};
```



