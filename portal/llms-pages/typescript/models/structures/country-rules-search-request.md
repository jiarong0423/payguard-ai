# Country Rules Search Request

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkNvdW50cnlSdWxlc1NlYXJjaFJlcXVlc3Q

CountryRulesSearchRequest.


# Interface Name

`CountryRulesSearchRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `limit` | `number \| undefined` | Optional | Limit.<br><br>**Default**: `5`<br><br>**Constraints**: `>= 1`, `<= 10` |
| `query` | `string` | Required | Query.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` |


# Example

```ts
import { CountryRulesSearchRequest } from 'tradeglot-local-consolelib';

const countryRulesSearchRequest: CountryRulesSearchRequest = {
  query: 'query4',
  limit: 5,
};
```



