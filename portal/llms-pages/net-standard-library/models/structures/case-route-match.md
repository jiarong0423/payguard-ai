# Case Route Match

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkNhc2VSb3V0ZU1hdGNo

CaseRouteMatch.


# Class Name

`CaseRouteMatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Category` | [`CaseRouteMatchCategory`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/case-route-match-category.md) | Required | This is a container for any-of cases. |
| `ExactWords` | `List<string>` | Required | Exact words.<br><br>**Constraints**: *Maximum Items*: `8`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z0-9]+$` |
| `MatchType` | [`MatchTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/match-type.md) | Required | Match type. |
| `ProductId` | `string` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `Score` | `double` | Required | Score.<br><br>**Constraints**: `>= 0`, `<= 1` |
| `Title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

CaseRouteMatch caseRouteMatch = new CaseRouteMatch
{
    Category = CaseRouteMatchCategory.FromString("String7"),
    ExactWords = new List<string>
    {
        "exact_words4",
        "exact_words3",
    },
    MatchType = MatchTypeEnum.Exact,
    ProductId = "product_id4",
    Score = 1,
    Title = "title4",
};
```



