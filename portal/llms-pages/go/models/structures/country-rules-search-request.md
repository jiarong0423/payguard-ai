# Country Rules Search Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkNvdW50cnlSdWxlc1NlYXJjaFJlcXVlc3Q

CountryRulesSearchRequest.


# Class Name

`CountryRulesSearchRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Limit` | `*int` | Optional | Limit.<br><br>**Default**: `5`<br><br>**Constraints**: `>= 1`, `<= 10` |
| `Query` | `string` | Required | Query.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    countryRulesSearchRequest := models.CountryRulesSearchRequest{
        Limit: models.ToPointer(5),
        Query: "query4",
    }

}
```



