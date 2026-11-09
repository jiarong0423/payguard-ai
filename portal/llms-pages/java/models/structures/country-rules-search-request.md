# Country Rules Search Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkNvdW50cnlSdWxlc1NlYXJjaFJlcXVlc3Q

CountryRulesSearchRequest.


# Class Name

`CountryRulesSearchRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Limit` | `Integer` | Optional | Limit.<br><br>**Default**: `5`<br><br>**Constraints**: `>= 1`, `<= 10` | Integer getLimit() | setLimit(Integer limit) |
| `Query` | `String` | Required | Query.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` | String getQuery() | setQuery(String query) |


# Example

```java
import m18000.m0.m0.m127.models.CountryRulesSearchRequest;

CountryRulesSearchRequest countryRulesSearchRequest = new CountryRulesSearchRequest.Builder(
    "query4"
)
.limit(5)
.build();
```



