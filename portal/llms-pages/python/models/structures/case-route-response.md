# Case Route Response

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkNhc2VSb3V0ZVJlc3BvbnNl

Fuzzy case routing: which goods group (and so which dispute items) applies. Code decides; advisory only.


# Class Name

`CaseRouteResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `affects_decision` | `str` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` |
| `decided_by` | `str` | Required, Constant | Decided by.<br><br>**Value**: `"code"` |
| `filtered_out` | `int` | Required | Filtered out.<br><br>**Constraints**: `>= 0`, `<= 1000` |
| `items` | `List[str]` | Required | Items.<br><br>**Constraints**: *Maximum Items*: `12` |
| `matched_word` | str | Required | This is a container for any-of cases. |
| `matches` | [`List[CaseRouteMatch]`](http://localhost:3000/llms-pages/python/models/structures/case-route-match.md) | Required | Matches.<br><br>**Constraints**: *Maximum Items*: `3` |
| `query` | str | Required | This is a container for any-of cases. |
| `reason` | [`Reason1Enum`](http://localhost:3000/llms-pages/python/models/enumerations/reason-1.md) | Required | Reason. |
| `route` | [`RouteEnum`](http://localhost:3000/llms-pages/python/models/enumerations/route.md) | Required | Route. |


# Example

```python
from tradeglotlocalconsole.models.case_route_match import CaseRouteMatch
from tradeglotlocalconsole.models.case_route_response import CaseRouteResponse
from tradeglotlocalconsole.models.match_type_enum import MatchTypeEnum
from tradeglotlocalconsole.models.reason_1_enum import Reason1Enum
from tradeglotlocalconsole.models.route_enum import RouteEnum

case_route_response = CaseRouteResponse(
    filtered_out=90,
    items=[
        'items1',
        'items2'
    ],
    matched_word='String3',
    matches=[
        CaseRouteMatch(
            category='String1',
            exact_words=[
                'exact_words2',
                'exact_words3',
                'exact_words4'
            ],
            match_type=MatchTypeEnum.EXACT,
            product_id='product_id8',
            score=1,
            title='title2'
        )
    ],
    query='String5',
    reason=Reason1Enum.NOTHING_TO_MATCH,
    route=RouteEnum.SERVICE
)
```



