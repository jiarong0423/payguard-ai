# Case Route Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkNhc2VSb3V0ZVJlc3BvbnNl

Fuzzy case routing: which goods group (and so which dispute items) applies. Code decides; advisory only.


# Class Name

`CaseRouteResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AffectsDecision` | `String` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` | String getAffectsDecision() | setAffectsDecision(String affectsDecision) |
| `DecidedBy` | `String` | Required, Constant | Decided by.<br><br>**Value**: `"code"` | String getDecidedBy() | setDecidedBy(String decidedBy) |
| `FilteredOut` | `int` | Required | Filtered out.<br><br>**Constraints**: `>= 0`, `<= 1000` | int getFilteredOut() | setFilteredOut(int filteredOut) |
| `Items` | `List<String>` | Required | Items.<br><br>**Constraints**: *Maximum Items*: `12` | List<String> getItems() | setItems(List<String> items) |
| `MatchedWord` | [`CaseRouteResponseMatchedWord`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/case-route-response-matched-word.md) | Required | This is a container for any-of cases. | CaseRouteResponseMatchedWord getMatchedWord() | setMatchedWord(CaseRouteResponseMatchedWord matchedWord) |
| `Matches` | [`List<CaseRouteMatch>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/case-route-match.md) | Required | Matches.<br><br>**Constraints**: *Maximum Items*: `3` | List<CaseRouteMatch> getMatches() | setMatches(List<CaseRouteMatch> matches) |
| `Query` | [`CaseRouteResponseQuery`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/case-route-response-query.md) | Required | This is a container for any-of cases. | CaseRouteResponseQuery getQuery() | setQuery(CaseRouteResponseQuery query) |
| `Reason` | [`Reason1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/reason-1.md) | Required | Reason. | Reason1Enum getReason() | setReason(Reason1Enum reason) |
| `Route` | [`RouteEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/route.md) | Required | Route. | RouteEnum getRoute() | setRoute(RouteEnum route) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.CaseRouteMatch;
import m18000.m0.m0.m127.models.CaseRouteResponse;
import m18000.m0.m0.m127.models.MatchTypeEnum;
import m18000.m0.m0.m127.models.Reason1Enum;
import m18000.m0.m0.m127.models.RouteEnum;
import m18000.m0.m0.m127.models.containers.CaseRouteMatchCategory;
import m18000.m0.m0.m127.models.containers.CaseRouteResponseMatchedWord;
import m18000.m0.m0.m127.models.containers.CaseRouteResponseQuery;

CaseRouteResponse caseRouteResponse = new CaseRouteResponse.Builder(
    "False",
    "code",
    76,
    Arrays.asList(
        "items3",
        "items4",
        "items5"
    ),
    CaseRouteResponseMatchedWord.fromString(
        "String5"
    ),
    Arrays.asList(
        new CaseRouteMatch.Builder(
            CaseRouteMatchCategory.fromString(
                "String1"
            ),
            Arrays.asList(
                "exact_words2",
                "exact_words3",
                "exact_words4"
            ),
            MatchTypeEnum.EXACT,
            "product_id8",
            1D,
            "title2"
        )
        .build()
    ),
    CaseRouteResponseQuery.fromString(
        "String7"
    ),
    Reason1Enum.NO_CLOSE_MATCH,
    RouteEnum.PHYSICAL
)
.build();
```



