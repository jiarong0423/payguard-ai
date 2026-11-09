# Case Route Match

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkNhc2VSb3V0ZU1hdGNo

CaseRouteMatch.


# Class Name

`CaseRouteMatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | str | Required | This is a container for any-of cases. |
| `exact_words` | `List[str]` | Required | Exact words.<br><br>**Constraints**: *Maximum Items*: `8`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z0-9]+$` |
| `match_type` | [`MatchTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/match-type.md) | Required | Match type. |
| `product_id` | `str` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `score` | `float` | Required | Score.<br><br>**Constraints**: `>= 0`, `<= 1` |
| `title` | `str` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```python
from tradeglotlocalconsole.models.case_route_match import CaseRouteMatch
from tradeglotlocalconsole.models.match_type_enum import MatchTypeEnum

case_route_match = CaseRouteMatch(
    category='String7',
    exact_words=[
        'exact_words8',
        'exact_words9'
    ],
    match_type=MatchTypeEnum.EXACT,
    product_id='product_id8',
    score=1,
    title='title8'
)
```



