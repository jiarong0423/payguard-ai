# Policy Coverage

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlBvbGljeUNvdmVyYWdl

PolicyCoverage.


# Class Name

`PolicyCoverage`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Basis` | `String` | Required, Constant | Basis.<br><br>**Value**: `"pinned_authored_summaries_only"` | String getBasis() | setBasis(String basis) |
| `Complete` | `boolean` | Required | Complete. | boolean getComplete() | setComplete(boolean complete) |
| `MissingOfficialPolicyThemes` | [`List<MissingOfficialPolicyThemeEnum>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/missing-official-policy-theme.md) | Required | Missing official policy themes.<br><br>**Constraints**: *Maximum Items*: `3` | List<MissingOfficialPolicyThemeEnum> getMissingOfficialPolicyThemes() | setMissingOfficialPolicyThemes(List<MissingOfficialPolicyThemeEnum> missingOfficialPolicyThemes) |
| `OfficialPolicyChunkCountByTheme` | [`PolicyThemeCounts`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/policy-theme-counts.md) | Required | PolicyThemeCounts. | PolicyThemeCounts getOfficialPolicyChunkCountByTheme() | setOfficialPolicyChunkCountByTheme(PolicyThemeCounts officialPolicyChunkCountByTheme) |
| `OfficialPolicySourceIds` | `List<String>` | Required | Official policy source ids.<br><br>**Constraints**: *Maximum Items*: `16`, *Pattern*: `^[A-Z0-9-]{1,128}$` | List<String> getOfficialPolicySourceIds() | setOfficialPolicySourceIds(List<String> officialPolicySourceIds) |
| `RegionalSourceCount` | `int` | Required | Regional source count.<br><br>**Constraints**: `>= 0`, `<= 16` | int getRegionalSourceCount() | setRegionalSourceCount(int regionalSourceCount) |
| `SelectedChunkCount` | `int` | Required | Selected chunk count.<br><br>**Constraints**: `>= 0`, `<= 29` | int getSelectedChunkCount() | setSelectedChunkCount(int selectedChunkCount) |
| `SelectedSourceCount` | `int` | Required | Selected source count.<br><br>**Constraints**: `>= 0`, `<= 16` | int getSelectedSourceCount() | setSelectedSourceCount(int selectedSourceCount) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.MissingOfficialPolicyThemeEnum;
import m18000.m0.m0.m127.models.PolicyCoverage;
import m18000.m0.m0.m127.models.PolicyThemeCounts;

PolicyCoverage policyCoverage = new PolicyCoverage.Builder(
    "pinned_authored_summaries_only",
    false,
    Arrays.asList(
        MissingOfficialPolicyThemeEnum.SOURCE_COMPLIANCE
    ),
    new PolicyThemeCounts.Builder(
        12,
        29,
        29
    )
    .build(),
    Arrays.asList(
        "official_policy_source_ids0"
    ),
    16,
    29,
    16
)
.build();
```



