# Guide Review Request

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3UmVxdWVzdA

GuideReviewRequest.


# Class Name

`GuideReviewRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Change` | `List<string>` | Optional | Change.<br><br>**Constraints**: *Maximum Items*: `9`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z_]+$` |
| `Confirm` | `bool?` | Optional | Confirm.<br><br>**Default**: `false` |
| `Scenario` | [`GuideReviewRequestScenario`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-review-request-scenario.md) | Optional | This is a container for any-of cases. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

GuideReviewRequest guideReviewRequest = new GuideReviewRequest
{
    Change = new List<string>
    {
        "change9",
        "change0",
        "change1",
    },
    Confirm = false,
    Scenario = GuideReviewRequestScenario.FromScenario1(Scenario1Enum.Dispute),
};
```



