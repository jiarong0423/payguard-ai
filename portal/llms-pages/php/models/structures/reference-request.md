# Reference Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlcXVlc3Q

ReferenceRequest.


# Class Name

`ReferenceRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `asOf` | string\|null | Optional | This is a container for any-of cases. | getAsOf(): ?string | setAsOf(?string asOf): void |
| `caseStage` | [`?string(CaseStage2Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/case-stage-2.md) | Optional | Case stage.<br><br>**Default**: `CaseStage2Enum::ANY` | getCaseStage(): ?string | setCaseStage(?string caseStage): void |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` | getJurisdiction(): string | setJurisdiction(string jurisdiction): void |
| `limit` | `?int` | Optional | Limit.<br><br>**Default**: `3`<br><br>**Constraints**: `>= 1`, `<= 10` | getLimit(): ?int | setLimit(?int limit): void |
| `materialTypes` | string([MaterialType4Enum](http://localhost:3000/llms-pages/php/models/enumerations/material-type-4.md))[]\|null | Optional | This is a container for any-of cases. | getMaterialTypes(): ?array | setMaterialTypes(?array materialTypes): void |
| `maxSourceAgeDays` | int\|null | Optional | This is a container for any-of cases. | getMaxSourceAgeDays(): ?int | setMaxSourceAgeDays(?int maxSourceAgeDays): void |
| `query` | `string` | Required | Query.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `512` | getQuery(): string | setQuery(string query): void |
| `requireKnownSourceDate` | `?bool` | Optional | Require known source date.<br><br>**Default**: `false` | getRequireKnownSourceDate(): ?bool | setRequireKnownSourceDate(?bool requireKnownSourceDate): void |
| `theme` | [`string(ThemeEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/theme.md) | Required | Theme. | getTheme(): string | setTheme(string theme): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ReferenceRequestBuilder;
use TradeGlotLocalConsoleLib\Models\ThemeEnum;
use TradeGlotLocalConsoleLib\Models\CaseStage2Enum;
use TradeGlotLocalConsoleLib\Models\MaterialType4Enum;

$referenceRequest = ReferenceRequestBuilder::init(
    'query4',
    ThemeEnum::DISPUTE_MEDIATION
)
    ->asOf(
        'String7'
    )
    ->caseStage(CaseStage2Enum::ANY)
    ->limit(3)
    ->materialTypes(
        [
            MaterialType4Enum::PUBLIC_COURT_ORDER_COPY
        ]
    )
    ->maxSourceAgeDays(
        110
    )
    ->requireKnownSourceDate(false)
    ->build();
```



