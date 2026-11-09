# Reference Filters

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlJlZmVyZW5jZUZpbHRlcnM

ReferenceFilters.


# Class Name

`ReferenceFilters`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `ageBasis` | `string` | Required, Constant | Age basis.<br><br>**Value**: `'source_updated_date_utc_calendar'` | getAgeBasis(): string | setAgeBasis(string ageBasis): void |
| `asOf` | string | Required | This is a container for any-of cases. | getAsOf(): string | setAsOf(string asOf): void |
| `caseStage` | [`string(CaseStage2Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/case-stage-2.md) | Required | Case stage. | getCaseStage(): string | setCaseStage(string caseStage): void |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` | getJurisdiction(): string | setJurisdiction(string jurisdiction): void |
| `limit` | `int` | Required | Limit.<br><br>**Constraints**: `>= 1`, `<= 10` | getLimit(): int | setLimit(int limit): void |
| `materialTypes` | [`string(MaterialType4Enum)[]`](http://localhost:3000/llms-pages/php/models/enumerations/material-type-4.md) | Required | Material types.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3` | getMaterialTypes(): array | setMaterialTypes(array materialTypes): void |
| `maxSourceAgeDays` | int | Required | This is a container for any-of cases. | getMaxSourceAgeDays(): int | setMaxSourceAgeDays(int maxSourceAgeDays): void |
| `requireKnownSourceDate` | `bool` | Required | Require known source date. | getRequireKnownSourceDate(): bool | setRequireKnownSourceDate(bool requireKnownSourceDate): void |
| `theme` | [`string(ThemeEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/theme.md) | Required | Theme. | getTheme(): string | setTheme(string theme): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ReferenceFiltersBuilder;
use TradeGlotLocalConsoleLib\Models\CaseStage2Enum;
use TradeGlotLocalConsoleLib\Models\MaterialType4Enum;
use TradeGlotLocalConsoleLib\Models\ThemeEnum;

$referenceFilters = ReferenceFiltersBuilder::init(
    'String9',
    CaseStage2Enum::PROCEDURAL_ORDER,
    10,
    [
        MaterialType4Enum::OFFICIAL_POLICY,
        MaterialType4Enum::PUBLIC_COURT_ORDER_COPY
    ],
    238,
    false,
    ThemeEnum::DISPUTE_MEDIATION
)->build();
```



