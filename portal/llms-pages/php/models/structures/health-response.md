# Health Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkhlYWx0aFJlc3BvbnNl

HealthResponse.


# Class Name

`HealthResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `mode` | `string` | Required, Constant | Mode.<br><br>**Value**: `'demo'` | getMode(): string | setMode(string mode): void |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` | getSource(): string | setSource(string source): void |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'ok'` | getStatus(): string | setStatus(string status): void |
| `version` | `string` | Required | Version. | getVersion(): string | setVersion(string version): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\HealthResponseBuilder;

$healthResponse = HealthResponseBuilder::init(
    'version0'
)->build();
```



