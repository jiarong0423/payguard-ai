# Policy Coverage

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlBvbGljeUNvdmVyYWdl

PolicyCoverage.


# Class Name

`PolicyCoverage`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Basis` | `string` | Required, Constant | Basis.<br><br>**Value**: `"pinned_authored_summaries_only"` |
| `Complete` | `bool` | Required | Complete. |
| `MissingOfficialPolicyThemes` | [`List<MissingOfficialPolicyThemeEnum>`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/missing-official-policy-theme.md) | Required | Missing official policy themes.<br><br>**Constraints**: *Maximum Items*: `3` |
| `OfficialPolicyChunkCountByTheme` | [`PolicyThemeCounts`](http://localhost:3000/llms-pages/net-standard-library/models/structures/policy-theme-counts.md) | Required | PolicyThemeCounts. |
| `OfficialPolicySourceIds` | `List<string>` | Required | Official policy source ids.<br><br>**Constraints**: *Maximum Items*: `16`, *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `RegionalSourceCount` | `int` | Required | Regional source count.<br><br>**Constraints**: `>= 0`, `<= 16` |
| `SelectedChunkCount` | `int` | Required | Selected chunk count.<br><br>**Constraints**: `>= 0`, `<= 29` |
| `SelectedSourceCount` | `int` | Required | Selected source count.<br><br>**Constraints**: `>= 0`, `<= 16` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;

PolicyCoverage policyCoverage = new PolicyCoverage
{
    Basis = "pinned_authored_summaries_only",
    Complete = false,
    MissingOfficialPolicyThemes = new List<MissingOfficialPolicyThemeEnum>
    {
        MissingOfficialPolicyThemeEnum.SourceCompliance,
    },
    OfficialPolicyChunkCountByTheme = new PolicyThemeCounts
    {
        DisputeMediation = 12,
        SourceCompliance = 29,
        VelocityGuard = 29,
    },
    OfficialPolicySourceIds = new List<string>
    {
        "official_policy_source_ids0",
    },
    RegionalSourceCount = 16,
    SelectedChunkCount = 29,
    SelectedSourceCount = 16,
};
```



