# Policy Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlBvbGljeVJlcXVlc3Q

PolicyRequest.


# Class Name

`PolicyRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `asOf` | `string` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` | getAsOf(): string | setAsOf(string asOf): void |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` | getJurisdiction(): string | setJurisdiction(string jurisdiction): void |
| `observationMaxAgeDays` | `int` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` | getObservationMaxAgeDays(): int | setObservationMaxAgeDays(int observationMaxAgeDays): void |
| `theme` | [`string(ThemeEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/theme.md) | Required | Theme. | getTheme(): string | setTheme(string theme): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\PolicyRequestBuilder;
use TradeGlotLocalConsoleLib\Models\ThemeEnum;

$policyRequest = PolicyRequestBuilder::init(
    'as_of8',
    186,
    ThemeEnum::DISPUTE_MEDIATION
)->build();
```



