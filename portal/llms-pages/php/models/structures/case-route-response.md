# Case Route Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkNhc2VSb3V0ZVJlc3BvbnNl

Fuzzy case routing: which goods group (and so which dispute items) applies. Code decides; advisory only.


# Class Name

`CaseRouteResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `affectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `'False'` | getAffectsDecision(): string | setAffectsDecision(string affectsDecision): void |
| `decidedBy` | `string` | Required, Constant | Decided by.<br><br>**Value**: `'code'` | getDecidedBy(): string | setDecidedBy(string decidedBy): void |
| `filteredOut` | `int` | Required | Filtered out.<br><br>**Constraints**: `>= 0`, `<= 1000` | getFilteredOut(): int | setFilteredOut(int filteredOut): void |
| `items` | `string[]` | Required | Items.<br><br>**Constraints**: *Maximum Items*: `12` | getItems(): array | setItems(array items): void |
| `matchedWord` | string | Required | This is a container for any-of cases. | getMatchedWord(): string | setMatchedWord(string matchedWord): void |
| `matches` | [`CaseRouteMatch[]`](http://localhost:3000/llms-pages/php/models/structures/case-route-match.md) | Required | Matches.<br><br>**Constraints**: *Maximum Items*: `3` | getMatches(): array | setMatches(array matches): void |
| `query` | string | Required | This is a container for any-of cases. | getQuery(): string | setQuery(string query): void |
| `reason` | [`string(Reason1Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/reason-1.md) | Required | Reason. | getReason(): string | setReason(string reason): void |
| `route` | [`string(RouteEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/route.md) | Required | Route. | getRoute(): string | setRoute(string route): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\CaseRouteResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\CaseRouteMatchBuilder;
use TradeGlotLocalConsoleLib\Models\MatchTypeEnum;
use TradeGlotLocalConsoleLib\Models\Reason1Enum;
use TradeGlotLocalConsoleLib\Models\RouteEnum;

$caseRouteResponse = CaseRouteResponseBuilder::init(
    76,
    [
        'items3',
        'items4',
        'items5'
    ],
    'String5',
    [
        CaseRouteMatchBuilder::init(
            'String1',
            [
                'exact_words2',
                'exact_words3',
                'exact_words4'
            ],
            MatchTypeEnum::EXACT,
            'product_id8',
            1,
            'title2'
        )->build()
    ],
    'String7',
    Reason1Enum::NO_CLOSE_MATCH,
    RouteEnum::PHYSICAL
)->build();
```



