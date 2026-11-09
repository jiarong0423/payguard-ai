# Case Route Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkNhc2VSb3V0ZVJlc3BvbnNl

Fuzzy case routing: which goods group (and so which dispute items) applies. Code decides; advisory only.


# Class Name

`CaseRouteResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AffectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` |
| `DecidedBy` | `string` | Required, Constant | Decided by.<br><br>**Value**: `"code"` |
| `FilteredOut` | `int` | Required | Filtered out.<br><br>**Constraints**: `>= 0`, `<= 1000` |
| `Items` | `[]string` | Required | Items.<br><br>**Constraints**: *Maximum Items*: `12` |
| `MatchedWord` | [`models.CaseRouteResponseMatchedWord`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/case-route-response-matched-word.md) | Required | This is a container for any-of cases. |
| `Matches` | [`[]models.CaseRouteMatch`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/case-route-match.md) | Required | Matches.<br><br>**Constraints**: *Maximum Items*: `3` |
| `Query` | [`models.CaseRouteResponseQuery`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/case-route-response-query.md) | Required | This is a container for any-of cases. |
| `Reason` | [`models.Reason1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/reason-1.md) | Required | Reason. |
| `Route` | [`models.RouteEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/route.md) | Required | Route. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    caseRouteResponse := models.CaseRouteResponse{
        AffectsDecision: "False",
        DecidedBy:       "code",
        FilteredOut:     76,
        Items:           []string{
            "items3",
            "items4",
            "items5",
        },
        MatchedWord:     models.CaseRouteResponseMatchedWordContainer.FromString("String5"),
        Matches:         []models.CaseRouteMatch{
            models.CaseRouteMatch{
                Category:   models.CaseRouteMatchCategoryContainer.FromString("String1"),
                ExactWords: []string{
                    "exact_words2",
                    "exact_words3",
                    "exact_words4",
                },
                MatchType:  models.MatchTypeEnum_EXACT,
                ProductId:  "product_id8",
                Score:      float64(1),
                Title:      "title2",
            },
        },
        Query:           models.CaseRouteResponseQueryContainer.FromString("String7"),
        Reason:          models.Reason1Enum_NOCLOSEMATCH,
        Route:           models.RouteEnum_PHYSICAL,
    }

}
```



