# Guide Turn Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlVHVyblJlcXVlc3Q

GuideTurnRequest.


# Class Name

`GuideTurnRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Fields` | [`GuideTurnRequestFields`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-turn-request-fields.md) | Optional | This is a container for any-of cases. |
| `Scenario` | [`GuideTurnRequestScenario`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-turn-request-scenario.md) | Optional | This is a container for any-of cases. |
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



