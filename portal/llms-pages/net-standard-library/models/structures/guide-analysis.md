# Guide Analysis

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlQW5hbHlzaXM

GuideAnalysis.


# Class Name

`GuideAnalysis`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Reason` | [`GuideAnalysisReason`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-analysis-reason.md) | Required | This is a container for any-of cases. |
| `Status` | [`Status8Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/status-8.md) | Required | Status. |
| `Turn` | `int` | Required | Turn. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

GuideAnalysis guideAnalysis = new GuideAnalysis
{
    Reason = GuideAnalysisReason.FromReason5(Reason5Enum.InvalidReply),
    Status = Status8Enum.Analysing,
    Turn = 236,
};
```



