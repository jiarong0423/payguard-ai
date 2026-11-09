# Reference Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlcXVlc3Q

ReferenceRequest.


# Class Name

`ReferenceRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AsOf` | [`ReferenceRequestAsOf`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/reference-request-as-of.md) | Optional | This is a container for any-of cases. | ReferenceRequestAsOf getAsOf() | setAsOf(ReferenceRequestAsOf asOf) |
| `CaseStage` | [`CaseStage2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/case-stage-2.md) | Optional | Case stage.<br><br>**Default**: `CaseStage2Enum.ANY` | CaseStage2Enum getCaseStage() | setCaseStage(CaseStage2Enum caseStage) |
| `Jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` | String getJurisdiction() | setJurisdiction(String jurisdiction) |
| `Limit` | `Integer` | Optional | Limit.<br><br>**Default**: `3`<br><br>**Constraints**: `>= 1`, `<= 10` | Integer getLimit() | setLimit(Integer limit) |
| `MaterialTypes` | [`ReferenceRequestMaterialTypes`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/reference-request-material-types.md) | Optional | This is a container for any-of cases. | ReferenceRequestMaterialTypes getMaterialTypes() | setMaterialTypes(ReferenceRequestMaterialTypes materialTypes) |
| `MaxSourceAgeDays` | [`ReferenceRequestMaxSourceAgeDays`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/reference-request-max-source-age-days.md) | Optional | This is a container for any-of cases. | ReferenceRequestMaxSourceAgeDays getMaxSourceAgeDays() | setMaxSourceAgeDays(ReferenceRequestMaxSourceAgeDays maxSourceAgeDays) |
| `Query` | `String` | Required | Query.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `512` | String getQuery() | setQuery(String query) |
| `RequireKnownSourceDate` | `Boolean` | Optional | Require known source date.<br><br>**Default**: `false` | Boolean getRequireKnownSourceDate() | setRequireKnownSourceDate(Boolean requireKnownSourceDate) |
| `Theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/theme.md) | Required | Theme. | ThemeEnum getTheme() | setTheme(ThemeEnum theme) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.CaseStage2Enum;
import m18000.m0.m0.m127.models.MaterialType4Enum;
import m18000.m0.m0.m127.models.ReferenceRequest;
import m18000.m0.m0.m127.models.ThemeEnum;
import m18000.m0.m0.m127.models.containers.ReferenceRequestAsOf;
import m18000.m0.m0.m127.models.containers.ReferenceRequestMaterialTypes;
import m18000.m0.m0.m127.models.containers.ReferenceRequestMaxSourceAgeDays;

ReferenceRequest referenceRequest = new ReferenceRequest.Builder(
    "US",
    "query4",
    ThemeEnum.DISPUTE_MEDIATION
)
.asOf(ReferenceRequestAsOf.fromString(
        "String7"
    ))
.caseStage(CaseStage2Enum.ANY)
.limit(3)
.materialTypes(ReferenceRequestMaterialTypes.fromListOfMaterialType4(
        Arrays.asList(
            MaterialType4Enum.PUBLIC_COURT_ORDER_COPY
        )
    ))
.maxSourceAgeDays(ReferenceRequestMaxSourceAgeDays.fromNumber(
        110
    ))
.requireKnownSourceDate(false)
.build();
```



