# Country Rules Search Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkNvdW50cnlSdWxlc1NlYXJjaFJlcXVlc3Q

CountryRulesSearchRequest.


# Class Name

`CountryRulesSearchRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `limit` | `int` | Optional | Limit.<br><br>**Default**: `5`<br><br>**Constraints**: `>= 1`, `<= 10` |
| `query` | `str` | Required | Query.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` |


# Example

```python
from tradeglotlocalconsole.models.country_rules_search_request import CountryRulesSearchRequest

country_rules_search_request = CountryRulesSearchRequest(
    query='query2',
    limit=5
)
```



