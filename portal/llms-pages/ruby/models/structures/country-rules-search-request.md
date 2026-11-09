# Country Rules Search Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkNvdW50cnlSdWxlc1NlYXJjaFJlcXVlc3Q

CountryRulesSearchRequest.


# Class Name

`CountryRulesSearchRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `limit` | `Integer` | Optional | Limit.<br><br>**Default**: `5`<br><br>**Constraints**: `>= 1`, `<= 10` |
| `query` | `String` | Required | Query.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` |


# Example

```ruby
country_rules_search_request = CountryRulesSearchRequest.new(
  'query2',
  5
)
```



