# Reference Filters

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlJlZmVyZW5jZUZpbHRlcnM

ReferenceFilters.


# Class Name

`ReferenceFilters`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AgeBasis` | `string` | Required, Constant | Age basis.<br><br>**Value**: `"source_updated_date_utc_calendar"` |
| `AsOf` | [`ReferenceFiltersAsOf`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/reference-filters-as-of.md) | Required | This is a container for any-of cases. |
| `CaseStage` | [`CaseStage2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/case-stage-2.md) | Required | Case stage. |
| `Jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `Limit` | `int` | Required | Limit.<br><br>**Constraints**: `>= 1`, `<= 10` |
| `MaterialTypes` | [`List<MaterialType4Enum>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/material-type-4.md) | Required | Material types.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3` |
| `MaxSourceAgeDays` | [`ReferenceFiltersMaxSourceAgeDays`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/reference-filters-max-source-age-days.md) | Required | This is a container for any-of cases. |
| `RequireKnownSourceDate` | `bool` | Required | Require known source date. |
| `Theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/theme.md) | Required | Theme. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

ReferenceFilters referenceFilters = new ReferenceFilters
{
    AgeBasis = "source_updated_date_utc_calendar",
    AsOf = ReferenceFiltersAsOf.FromString("String9"),
    CaseStage = CaseStage2Enum.ProceduralOrder,
    Jurisdiction = "US",
    Limit = 10,
    MaterialTypes = new List<MaterialType4Enum>
    {
        MaterialType4Enum.OfficialPolicy,
        MaterialType4Enum.PublicCourtOrderCopy,
    },
    MaxSourceAgeDays = ReferenceFiltersMaxSourceAgeDays.FromNumber(238),
    RequireKnownSourceDate = false,
    Theme = ThemeEnum.DisputeMediation,
};
```



