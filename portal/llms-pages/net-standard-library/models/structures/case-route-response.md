# Case Route Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkNhc2VSb3V0ZVJlc3BvbnNl

Fuzzy case routing: which goods group (and so which dispute items) applies. Code decides; advisory only.


# Class Name

`CaseRouteResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AffectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` |
| `DecidedBy` | `string` | Required, Constant | Decided by.<br><br>**Value**: `"code"` |
| `FilteredOut` | `int` | Required | Filtered out.<br><br>**Constraints**: `>= 0`, `<= 1000` |
| `Items` | `List<string>` | Required | Items.<br><br>**Constraints**: *Maximum Items*: `12` |
| `MatchedWord` | [`CaseRouteResponseMatchedWord`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/case-route-response-matched-word.md) | Required | This is a container for any-of cases. |
| `Matches` | [`List<CaseRouteMatch>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/case-route-match.md) | Required | Matches.<br><br>**Constraints**: *Maximum Items*: `3` |
| `Query` | [`CaseRouteResponseQuery`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/case-route-response-query.md) | Required | This is a container for any-of cases. |
| `Reason` | [`Reason1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/reason-1.md) | Required | Reason. |
| `Route` | [`RouteEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/route.md) | Required | Route. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

CaseRouteResponse caseRouteResponse = new CaseRouteResponse
{
    AffectsDecision = "False",
    DecidedBy = "code",
    FilteredOut = 76,
    Items = new List<string>
    {
        "items3",
        "items4",
        "items5",
    },
    MatchedWord = CaseRouteResponseMatchedWord.FromString("String5"),
    Matches = new List<CaseRouteMatch>
    {
        new CaseRouteMatch
        {
            Category = CaseRouteMatchCategory.FromString("String1"),
            ExactWords = new List<string>
            {
                "exact_words2",
                "exact_words3",
                "exact_words4",
            },
            MatchType = MatchTypeEnum.Exact,
            ProductId = "product_id8",
            Score = 1,
            Title = "title2",
        },
    },
    Query = CaseRouteResponseQuery.FromString("String7"),
    Reason = Reason1Enum.NoCloseMatch,
    Route = RouteEnum.Physical,
};
```



