# Policy Theme Counts

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlBvbGljeVRoZW1lQ291bnRz

PolicyThemeCounts.


# Class Name

`PolicyThemeCounts`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `DisputeMediation` | `int` | Required | Dispute mediation.<br><br>**Constraints**: `>= 0`, `<= 29` |
| `SourceCompliance` | `int` | Required | Source compliance.<br><br>**Constraints**: `>= 0`, `<= 29` |
| `VelocityGuard` | `int` | Required | Velocity guard.<br><br>**Constraints**: `>= 0`, `<= 29` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

PolicyThemeCounts policyThemeCounts = new PolicyThemeCounts
{
    DisputeMediation = 29,
    SourceCompliance = 29,
    VelocityGuard = 29,
};
```



