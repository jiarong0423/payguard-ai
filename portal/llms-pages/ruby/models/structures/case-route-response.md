# Case Route Response

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkNhc2VSb3V0ZVJlc3BvbnNl

Fuzzy case routing: which goods group (and so which dispute items) applies. Code decides; advisory only.


# Class Name

`CaseRouteResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `affects_decision` | `String` | Required, Constant | Affects decision.<br><br>**Value**: `'False'` |
| `decided_by` | `String` | Required, Constant | Decided by.<br><br>**Value**: `'code'` |
| `filtered_out` | `Integer` | Required | Filtered out.<br><br>**Constraints**: `>= 0`, `<= 1000` |
| `items` | `Array[String]` | Required | Items.<br><br>**Constraints**: *Maximum Items*: `12` |
| `matched_word` | String | Required | This is a container for any-of cases. |
| `matches` | [`Array[CaseRouteMatch]`](http://localhost:3000/llms-pages/ruby/models/structures/case-route-match.md) | Required | Matches.<br><br>**Constraints**: *Maximum Items*: `3` |
| `query` | String | Required | This is a container for any-of cases. |
| `reason` | [`Reason1Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/reason-1.md) | Required | Reason. |
| `route` | [`RouteEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/route.md) | Required | Route. |


# Example

```ruby
case_route_response = CaseRouteResponse.new(
  'False',
  'code',
  90,
  [
    'items1',
    'items2'
  ],
  'String3',
  [
    CaseRouteMatch.new(
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
    )
  ],
  'String5',
  Reason1Enum::NOTHING_TO_MATCH,
  RouteEnum::SERVICE
)
```



