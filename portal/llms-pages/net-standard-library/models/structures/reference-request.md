# Reference Request

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlcXVlc3Q

ReferenceRequest.


# Class Name

`ReferenceRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AsOf` | [`ReferenceRequestAsOf`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/reference-request-as-of.md) | Optional | This is a container for any-of cases. |
| `CaseStage` | [`CaseStage2Enum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/case-stage-2.md) | Optional | Case stage.<br><br>**Default**: `CaseStage2Enum.any` |
| `Jurisdiction` | `string` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `Limit` | `int?` | Optional | Limit.<br><br>**Default**: `3`<br><br>**Constraints**: `>= 1`, `<= 10` |
| `MaterialTypes` | [`ReferenceRequestMaterialTypes`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/reference-request-material-types.md) | Optional | This is a container for any-of cases. |
| `MaxSourceAgeDays` | [`ReferenceRequestMaxSourceAgeDays`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/reference-request-max-source-age-days.md) | Optional | This is a container for any-of cases. |
| `Query` | `string` | Required | Query.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `512` |
| `RequireKnownSourceDate` | `bool?` | Optional | Require known source date.<br><br>**Default**: `false` |
| `Theme` | [`ThemeEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/theme.md) | Required | Theme. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

ReferenceRequest referenceRequest = new ReferenceRequest
{
    Jurisdiction = "US",
    Query = "query4",
    Theme = ThemeEnum.DisputeMediation,
    AsOf = ReferenceRequestAsOf.FromString("String7"),
    CaseStage = CaseStage2Enum.Any,
    Limit = 3,
    MaterialTypes = ReferenceRequestMaterialTypes.FromListOfMaterialType4(
        new List<MaterialType4Enum>
        {
            MaterialType4Enum.PublicCourtOrderCopy,
        }
    ),
    MaxSourceAgeDays = ReferenceRequestMaxSourceAgeDays.FromNumber(110),
    RequireKnownSourceDate = false,
};
```



