# Reference Filters

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlJlZmVyZW5jZUZpbHRlcnM

ReferenceFilters.


# Interface Name

`ReferenceFilters`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `ageBasis` | `string` | Required, Constant | Age basis.<br><br>**Value**: `'source_updated_date_utc_calendar'` |
| `asOf` | [`ReferenceFiltersAsOf`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/reference-filters-as-of.md) | Required | This is a container for any-of cases. |
| `caseStage` | [`CaseStage2Enum`](http://localhost:3000/llms-pages/typescript/models/enumerations/case-stage-2.md) | Required | Case stage. |
| `jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `limit` | `number` | Required | Limit.<br><br>**Constraints**: `>= 1`, `<= 10` |
| `materialTypes` | [`MaterialType4Enum[]`](http://localhost:3000/llms-pages/typescript/models/enumerations/material-type-4.md) | Required | Material types.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3` |
| `maxSourceAgeDays` | [`ReferenceFiltersMaxSourceAgeDays`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/reference-filters-max-source-age-days.md) | Required | This is a container for any-of cases. |
| `requireKnownSourceDate` | `boolean` | Required | Require known source date. |
| `theme` | [`ThemeEnum`](http://localhost:3000/llms-pages/typescript/models/enumerations/theme.md) | Required | Theme. |


# Example

```ts
import {
  CaseStage2Enum,
  MaterialType4Enum,
  ReferenceFilters,
  ThemeEnum,
} from 'tradeglot-local-consolelib';

const referenceFilters: ReferenceFilters = {
  ageBasis: 'source_updated_date_utc_calendar',
  asOf: 'String9',
  caseStage: CaseStage2Enum.ProceduralOrder,
  jurisdiction: 'US',
  limit: 10,
  materialTypes: [
    MaterialType4Enum.OfficialPolicy,
    MaterialType4Enum.PublicCourtOrderCopy
  ],
  maxSourceAgeDays: 238,
  requireKnownSourceDate: false,
  theme: ThemeEnum.DisputeMediation,
};
```



