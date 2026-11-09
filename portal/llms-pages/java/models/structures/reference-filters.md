# Reference Filters

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlJlZmVyZW5jZUZpbHRlcnM

ReferenceFilters.


# Class Name

`ReferenceFilters`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AgeBasis` | `String` | Required, Constant | Age basis.<br><br>**Value**: `"source_updated_date_utc_calendar"` | String getAgeBasis() | setAgeBasis(String ageBasis) |
| `AsOf` | [`ReferenceFiltersAsOf`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/reference-filters-as-of.md) | Required | This is a container for any-of cases. | ReferenceFiltersAsOf getAsOf() | setAsOf(ReferenceFiltersAsOf asOf) |
| `CaseStage` | [`CaseStage2Enum`](http://localhost:3000/llms-pages/java/models/enumerations/case-stage-2.md) | Required | Case stage. | CaseStage2Enum getCaseStage() | setCaseStage(CaseStage2Enum caseStage) |
| `Jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` | String getJurisdiction() | setJurisdiction(String jurisdiction) |
| `Limit` | `int` | Required | Limit.<br><br>**Constraints**: `>= 1`, `<= 10` | int getLimit() | setLimit(int limit) |
| `MaterialTypes` | [`List<MaterialType4Enum>`](http://localhost:3000/llms-pages/java/models/enumerations/material-type-4.md) | Required | Material types.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3` | List<MaterialType4Enum> getMaterialTypes() | setMaterialTypes(List<MaterialType4Enum> materialTypes) |
| `MaxSourceAgeDays` | [`ReferenceFiltersMaxSourceAgeDays`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/reference-filters-max-source-age-days.md) | Required | This is a container for any-of cases. | ReferenceFiltersMaxSourceAgeDays getMaxSourceAgeDays() | setMaxSourceAgeDays(ReferenceFiltersMaxSourceAgeDays maxSourceAgeDays) |
| `RequireKnownSourceDate` | `boolean` | Required | Require known source date. | boolean getRequireKnownSourceDate() | setRequireKnownSourceDate(boolean requireKnownSourceDate) |
| `Theme` | [`ThemeEnum`](http://localhost:3000/llms-pages/java/models/enumerations/theme.md) | Required | Theme. | ThemeEnum getTheme() | setTheme(ThemeEnum theme) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.CaseStage2Enum;
import m18000.m0.m0.m127.models.MaterialType4Enum;
import m18000.m0.m0.m127.models.ReferenceFilters;
import m18000.m0.m0.m127.models.ThemeEnum;
import m18000.m0.m0.m127.models.containers.ReferenceFiltersAsOf;
import m18000.m0.m0.m127.models.containers.ReferenceFiltersMaxSourceAgeDays;

ReferenceFilters referenceFilters = new ReferenceFilters.Builder(
    "source_updated_date_utc_calendar",
    ReferenceFiltersAsOf.fromString(
        "String9"
    ),
    CaseStage2Enum.PROCEDURAL_ORDER,
    "US",
    10,
    Arrays.asList(
        MaterialType4Enum.OFFICIAL_POLICY,
        MaterialType4Enum.PUBLIC_COURT_ORDER_COPY
    ),
    ReferenceFiltersMaxSourceAgeDays.fromNumber(
        238
    ),
    false,
    ThemeEnum.DISPUTE_MEDIATION
)
.build();
```



