# Policy Context

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlBvbGljeUNvbnRleHQ

PolicyContext.


# Class Name

`PolicyContext`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AsOf` | `String` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` | String getAsOf() | setAsOf(String asOf) |
| `Jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` | String getJurisdiction() | setJurisdiction(String jurisdiction) |
| `ObservationMaxAgeDays` | `int` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` | int getObservationMaxAgeDays() | setObservationMaxAgeDays(int observationMaxAgeDays) |
| `Theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/theme.md) | Required | Theme. | ThemeEnum getTheme() | setTheme(ThemeEnum theme) |


# Example

```java
import m18000.m0.m0.m127.models.PolicyContext;
import m18000.m0.m0.m127.models.ThemeEnum;

PolicyContext policyContext = new PolicyContext.Builder(
    "as_of4",
    "US",
    12,
    ThemeEnum.VELOCITY_GUARD
)
.build();
```



