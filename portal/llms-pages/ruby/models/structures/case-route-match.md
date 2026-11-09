# Case Route Match

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkNhc2VSb3V0ZU1hdGNo

CaseRouteMatch.


# Class Name

`CaseRouteMatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | String | Required | This is a container for any-of cases. |
| `exact_words` | `Array[String]` | Required | Exact words.<br><br>**Constraints**: *Maximum Items*: `8`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z0-9]+$` |
| `match_type` | [`MatchTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/match-type.md) | Required | Match type. |
| `product_id` | `String` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `score` | `Float` | Required | Score.<br><br>**Constraints**: `>= 0`, `<= 1` |
| `title` | `String` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```ruby
case_route_match = CaseRouteMatch.new(
  'String7',
  [
    'exact_words8',
    'exact_words9'
  ],
  MatchTypeEnum::EXACT,
  'product_id8',
  1,
  'title8'
)
```



