# Case Route Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkNhc2VSb3V0ZVJlcXVlc3Q

CaseRouteRequest.


# Class Name

`CaseRouteRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `text` | `string` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` | getText(): string | setText(string text): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\CaseRouteRequestBuilder;

$caseRouteRequest = CaseRouteRequestBuilder::init(
    'text6'
)->build();
```



