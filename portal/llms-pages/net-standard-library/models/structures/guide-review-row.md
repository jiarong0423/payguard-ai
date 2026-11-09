# Guide Review Row

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3Um93

GuideReviewRow.


# Class Name

`GuideReviewRow`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Item` | `string` | Required | Item. |
| `Source` | [`Source9Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/source-9.md) | Required | Source. |
| `MValue` | `string` | Required | Value.<br><br>**Constraints**: *Maximum Length*: `120` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

GuideReviewRow guideReviewRow = new GuideReviewRow
{
    Item = "item6",
    Source = Source9Enum.Words,
    MValue = "value6",
};
```



