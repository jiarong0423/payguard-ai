# Guide Gap

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlR2Fw

GuideGap.


# Class Name

`GuideGap`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Conflicting` | `List<string>` | Required | Conflicting. |
| `Missing` | `List<string>` | Required | Missing. |
| `Partial` | `List<string>` | Required | Partial. |
| `Present` | `List<string>` | Required | Present. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;

GuideGap guideGap = new GuideGap
{
    Conflicting = new List<string>
    {
        "conflicting9",
    },
    Missing = new List<string>
    {
        "missing4",
    },
    MPartial = new List<string>
    {
        "partial4",
        "partial5",
    },
    Present = new List<string>
    {
        "present9",
        "present0",
        "present1",
    },
};
```



