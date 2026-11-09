# Connections Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkNvbm5lY3Rpb25zUmVzcG9uc2U

Deployment mode only. Never a key, a key's presence, a value or a variable name.


# Class Name

`ConnectionsResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `mode` | [`string(ModeEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/mode.md) | Required | Mode. | getMode(): string | setMode(string mode): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ConnectionsResponseBuilder;
use TradeGlotLocalConsoleLib\Models\ModeEnum;

$connectionsResponse = ConnectionsResponseBuilder::init(
    ModeEnum::LOCAL
)->build();
```



