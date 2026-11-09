# Advisory Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkFkdmlzb3J5UmVxdWVzdA

AdvisoryRequest.


# Class Name

`AdvisoryRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AsOf` | `String` | Required | As of.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` | String getAsOf() | setAsOf(String asOf) |
| `CandidateJson` | `String` | Required | Candidate json.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8192` | String getCandidateJson() | setCandidateJson(String candidateJson) |
| `Jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` | String getJurisdiction() | setJurisdiction(String jurisdiction) |
| `ObservationMaxAgeDays` | `int` | Required | Observation max age days.<br><br>**Constraints**: `>= 0`, `<= 365000` | int getObservationMaxAgeDays() | setObservationMaxAgeDays(int observationMaxAgeDays) |
| `Theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/theme.md) | Required | Theme. | ThemeEnum getTheme() | setTheme(ThemeEnum theme) |


# Example

```java
import m18000.m0.m0.m127.models.AdvisoryRequest;
import m18000.m0.m0.m127.models.ThemeEnum;

AdvisoryRequest advisoryRequest = new AdvisoryRequest.Builder(
    "as_of2",
    "candidate_json2",
    "US",
    220,
    ThemeEnum.VELOCITY_GUARD
)
.build();
```



