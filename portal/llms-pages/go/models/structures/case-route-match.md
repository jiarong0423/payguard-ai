# Case Route Match

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkNhc2VSb3V0ZU1hdGNo

CaseRouteMatch.


# Class Name

`CaseRouteMatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Category` | [`models.CaseRouteMatchCategory`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/case-route-match-category.md) | Required | This is a container for any-of cases. |
| `ExactWords` | `[]string` | Required | Exact words.<br><br>**Constraints**: *Maximum Items*: `8`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z0-9]+$` |
| `MatchType` | [`models.MatchTypeEnum`](http://localhost:3000/llms-pages/go/models/enumerations/match-type.md) | Required | Match type. |
| `ProductId` | `string` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `Score` | `float64` | Required | Score.<br><br>**Constraints**: `>= 0`, `<= 1` |
| `Title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    caseRouteMatch := models.CaseRouteMatch{
        Category:   models.CaseRouteMatchCategoryContainer.FromString("String7"),
        ExactWords: []string{
            "exact_words4",
            "exact_words3",
        },
        MatchType:  models.MatchTypeEnum_EXACT,
        ProductId:  "product_id4",
        Score:      float64(1),
        Title:      "title4",
    }

}
```



