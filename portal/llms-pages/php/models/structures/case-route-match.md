# Case Route Match

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkNhc2VSb3V0ZU1hdGNo

CaseRouteMatch.


# Class Name

`CaseRouteMatch`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `category` | string | Required | This is a container for any-of cases. | getCategory(): string | setCategory(string category): void |
| `exactWords` | `string[]` | Required | Exact words.<br><br>**Constraints**: *Maximum Items*: `8`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z0-9]+$` | getExactWords(): array | setExactWords(array exactWords): void |
| `matchType` | [`string(MatchTypeEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/match-type.md) | Required | Match type. | getMatchType(): string | setMatchType(string matchType): void |
| `productId` | `string` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` | getProductId(): string | setProductId(string productId): void |
| `score` | `float` | Required | Score.<br><br>**Constraints**: `>= 0`, `<= 1` | getScore(): float | setScore(float score): void |
| `title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | getTitle(): string | setTitle(string title): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\CaseRouteMatchBuilder;
use TradeGlotLocalConsoleLib\Models\MatchTypeEnum;

$caseRouteMatch = CaseRouteMatchBuilder::init(
    'String7',
    [
        'exact_words4',
        'exact_words3'
    ],
    MatchTypeEnum::EXACT,
    'product_id4',
    1,
    'title4'
)->build();
```



