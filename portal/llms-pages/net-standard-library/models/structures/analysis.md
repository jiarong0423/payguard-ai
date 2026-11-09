# Analysis

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkFuYWx5c2lz

Analysis.


# Class Name

`Analysis`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Reason` | [`AnalysisReason`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/analysis-reason.md) | Optional | This is a container for any-of cases. |
| `Status` | [`Status8Enum?`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/status-8.md) | Optional | Status. |
| `Turn` | `int?` | Optional | Turn. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

Analysis analysis = new Analysis
{
    Reason = AnalysisReason.FromReason5(Reason5Enum.InvalidReply),
    Status = Status8Enum.Replaced,
    Turn = 198,
};
```



