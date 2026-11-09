# Velocity Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlZlbG9jaXR5UmVzcG9uc2U

VelocityResponse.


# Class Name

`VelocityResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AdvisoryOnly` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` | String getAdvisoryOnly() | setAdvisoryOnly(String advisoryOnly) |
| `Alert` | `boolean` | Required | Alert. | boolean getAlert() | setAlert(boolean alert) |
| `BaselineAmountPerHour` | `String` | Required | Baseline amount per hour. | String getBaselineAmountPerHour() | setBaselineAmountPerHour(String baselineAmountPerHour) |
| `BaselineProvenance` | [`BaselineProvenanceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/baseline-provenance.md) | Required | Baseline provenance. | BaselineProvenanceEnum getBaselineProvenance() | setBaselineProvenance(BaselineProvenanceEnum baselineProvenance) |
| `BaselineWindowEnd` | `String` | Required | Baseline window end. | String getBaselineWindowEnd() | setBaselineWindowEnd(String baselineWindowEnd) |
| `BaselineWindowStart` | `String` | Required | Baseline window start. | String getBaselineWindowStart() | setBaselineWindowStart(String baselineWindowStart) |
| `Currency` | [`VelocityResponseCurrency`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/velocity-response-currency.md) | Required | This is a container for any-of cases. | VelocityResponseCurrency getCurrency() | setCurrency(VelocityResponseCurrency currency) |
| `CurrentAmountPerHour` | `String` | Required | Current amount per hour. | String getCurrentAmountPerHour() | setCurrentAmountPerHour(String currentAmountPerHour) |
| `ExcludedFutureCount` | `int` | Required | Excluded future count. | int getExcludedFutureCount() | setExcludedFutureCount(int excludedFutureCount) |
| `ExcludedPastCount` | `int` | Required | Excluded past count. | int getExcludedPastCount() | setExcludedPastCount(int excludedPastCount) |
| `Limitations` | `List<String>` | Required | Limitations. | List<String> getLimitations() | setLimitations(List<String> limitations) |
| `PolicyVersion` | `String` | Required | Policy version. | String getPolicyVersion() | setPolicyVersion(String policyVersion) |
| `Ratio` | [`VelocityResponseRatio`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/velocity-response-ratio.md) | Required | This is a container for any-of cases. | VelocityResponseRatio getRatio() | setRatio(VelocityResponseRatio ratio) |
| `Status` | [`Status14Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/status-14.md) | Required | Status. | Status14Enum getStatus() | setStatus(Status14Enum status) |
| `Threshold` | `String` | Required | Threshold. | String getThreshold() | setThreshold(String threshold) |
| `TotalAmount` | `String` | Required | Total amount. | String getTotalAmount() | setTotalAmount(String totalAmount) |
| `TransactionCount` | `int` | Required | Transaction count. | int getTransactionCount() | setTransactionCount(int transactionCount) |
| `WindowBoundary` | `String` | Required, Constant | Window boundary.<br><br>**Value**: `"left_open_right_closed"` | String getWindowBoundary() | setWindowBoundary(String windowBoundary) |
| `WindowEnd` | `String` | Required | Window end. | String getWindowEnd() | setWindowEnd(String windowEnd) |
| `WindowHours` | `int` | Required | Window hours. | int getWindowHours() | setWindowHours(int windowHours) |
| `WindowStart` | `String` | Required | Window start. | String getWindowStart() | setWindowStart(String windowStart) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.BaselineProvenanceEnum;
import m18000.m0.m0.m127.models.Status14Enum;
import m18000.m0.m0.m127.models.VelocityResponse;
import m18000.m0.m0.m127.models.containers.VelocityResponseCurrency;
import m18000.m0.m0.m127.models.containers.VelocityResponseRatio;

VelocityResponse velocityResponse = new VelocityResponse.Builder(
    "True",
    false,
    "baseline_amount_per_hour4",
    BaselineProvenanceEnum.SYNTHETIC_BASELINE,
    "baseline_window_end6",
    "baseline_window_start0",
    VelocityResponseCurrency.fromString(
        "String1"
    ),
    "current_amount_per_hour4",
    6,
    154,
    Arrays.asList(
        "limitations9",
        "limitations8",
        "limitations7"
    ),
    "policy_version8",
    VelocityResponseRatio.fromString(
        "String1"
    ),
    Status14Enum.NORMAL,
    "threshold8",
    "total_amount6",
    134,
    "left_open_right_closed",
    "window_end0",
    20,
    "window_start6"
)
.build();
```



