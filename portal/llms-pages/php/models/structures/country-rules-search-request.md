# Country Rules Search Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkNvdW50cnlSdWxlc1NlYXJjaFJlcXVlc3Q

CountryRulesSearchRequest.


# Class Name

`CountryRulesSearchRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `limit` | `?int` | Optional | Limit.<br><br>**Default**: `5`<br><br>**Constraints**: `>= 1`, `<= 10` | getLimit(): ?int | setLimit(?int limit): void |
| `query` | `string` | Required | Query.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` | getQuery(): string | setQuery(string query): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\CountryRulesSearchRequestBuilder;

$countryRulesSearchRequest = CountryRulesSearchRequestBuilder::init(
    'query4'
)
    ->limit(5)
    ->build();
```



