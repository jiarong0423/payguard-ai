# Guide Turn Request

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlVHVyblJlcXVlc3Q

GuideTurnRequest.


# Class Name

`GuideTurnRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Fields` | [`GuideTurnRequestFields`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-turn-request-fields.md) | Optional | This is a container for any-of cases. |
| `Scenario` | [`GuideTurnRequestScenario`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-turn-request-scenario.md) | Optional | This is a container for any-of cases. |
| `Text` | `string` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1600` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

GuideTurnRequest guideTurnRequest = new GuideTurnRequest
{
    Text = "text2",
    Fields = GuideTurnRequestFields.FromListOfGuideField(
        new List<GuideField>
        {
            new GuideField
            {
                Item = "item8",
                MValue = "value8",
            },
        }
    ),
    Scenario = GuideTurnRequestScenario.FromScenario1(Scenario1Enum.Preflight),
};
```



