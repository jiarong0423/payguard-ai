# Policy Coverage

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlBvbGljeUNvdmVyYWdl

PolicyCoverage.


# Class Name

`PolicyCoverage`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Basis` | `string` | Required, Constant | Basis.<br><br>**Value**: `"pinned_authored_summaries_only"` |
| `Complete` | `bool` | Required | Complete. |
| `MissingOfficialPolicyThemes` | [`[]models.MissingOfficialPolicyThemeEnum`](http://localhost:3000/llms-pages/go/models/enumerations/missing-official-policy-theme.md) | Required | Missing official policy themes.<br><br>**Constraints**: *Maximum Items*: `3` |
| `OfficialPolicyChunkCountByTheme` | [`models.PolicyThemeCounts`](http://localhost:3000/llms-pages/go/models/structures/policy-theme-counts.md) | Required | PolicyThemeCounts. |
| `OfficialPolicySourceIds` | `[]string` | Required | Official policy source ids.<br><br>**Constraints**: *Maximum Items*: `16`, *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `RegionalSourceCount` | `int` | Required | Regional source count.<br><br>**Constraints**: `>= 0`, `<= 16` |
| `SelectedChunkCount` | `int` | Required | Selected chunk count.<br><br>**Constraints**: `>= 0`, `<= 29` |
| `SelectedSourceCount` | `int` | Required | Selected source count.<br><br>**Constraints**: `>= 0`, `<= 16` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    policyCoverage := models.PolicyCoverage{
        Basis:                           "pinned_authored_summaries_only",
        Complete:                        false,
        MissingOfficialPolicyThemes:     []models.MissingOfficialPolicyThemeEnum{
            models.MissingOfficialPolicyThemeEnum_SOURCECOMPLIANCE,
        },
        OfficialPolicyChunkCountByTheme: models.PolicyThemeCounts{
            DisputeMediation: 12,
            SourceCompliance: 29,
            VelocityGuard:    29,
        },
        OfficialPolicySourceIds:         []string{
            "official_policy_source_ids0",
        },
        RegionalSourceCount:             16,
        SelectedChunkCount:              29,
        SelectedSourceCount:             16,
    }

}
```



