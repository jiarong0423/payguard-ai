# Advisory Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkFkdmlzb3J5UmVxdWVzdA

AdvisoryRequest.


# Class Name

`AdvisoryRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `asOf` | `string` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` | getAsOf(): string | setAsOf(string asOf): void |
| `candidateJson` | `string` | Required | Candidate json.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8192` | getCandidateJson(): string | setCandidateJson(string candidateJson): void |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` | getJurisdiction(): string | setJurisdiction(string jurisdiction): void |
| `observationMaxAgeDays` | `int` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` | getObservationMaxAgeDays(): int | setObservationMaxAgeDays(int observationMaxAgeDays): void |
| `theme` | [`string(ThemeEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/theme.md) | Required | Theme. | getTheme(): string | setTheme(string theme): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\AdvisoryRequestBuilder;
use TradeGlotLocalConsoleLib\Models\ThemeEnum;

$advisoryRequest = AdvisoryRequestBuilder::init(
    'as_of2',
    'candidate_json2',
    220,
    ThemeEnum::VELOCITY_GUARD
)->build();
```



