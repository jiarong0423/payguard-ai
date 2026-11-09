# Finding

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkZpbmRpbmc

Finding.


# Class Name

`Finding`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Category` | [`CategoryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/category.md) | Required | Category. |
| `Code` | `string` | Required, Constant | Code.<br><br>**Value**: `"keyword_requires_policy_review"` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

Finding finding = new Finding
{
    Category = CategoryEnum.UnsupportedFinancialPromise,
    Code = "keyword_requires_policy_review",
};
```



