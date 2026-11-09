# Policy Context

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlBvbGljeUNvbnRleHQ

PolicyContext.


# Class Name

`PolicyContext`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `asOf` | `string` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` | getAsOf(): string | setAsOf(string asOf): void |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` | getJurisdiction(): string | setJurisdiction(string jurisdiction): void |
| `observationMaxAgeDays` | `int` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` | getObservationMaxAgeDays(): int | setObservationMaxAgeDays(int observationMaxAgeDays): void |
| `theme` | [`string(ThemeEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/theme.md) | Required | Theme. | getTheme(): string | setTheme(string theme): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\PolicyContextBuilder;
use TradeGlotLocalConsoleLib\Models\ThemeEnum;

$policyContext = PolicyContextBuilder::init(
    'as_of4',
    12,
    ThemeEnum::VELOCITY_GUARD
)->build();
```



