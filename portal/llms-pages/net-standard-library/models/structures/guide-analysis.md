# Guide Analysis

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlQW5hbHlzaXM

GuideAnalysis.


# Class Name

`GuideAnalysis`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Reason` | [`GuideAnalysisReason`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/guide-analysis-reason.md) | Required | This is a container for any-of cases. |
| `Status` | [`Status8Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/status-8.md) | Required | Status. |
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



