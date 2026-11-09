# Velocity Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlZlbG9jaXR5UmVzcG9uc2U

VelocityResponse.


# Class Name

`VelocityResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` | getAdvisoryOnly(): string | setAdvisoryOnly(string advisoryOnly): void |
| `alert` | `bool` | Required | Alert. | getAlert(): bool | setAlert(bool alert): void |
| `baselineAmountPerHour` | `string` | Required | Baseline amount per hour. | getBaselineAmountPerHour(): string | setBaselineAmountPerHour(string baselineAmountPerHour): void |
| `baselineProvenance` | [`string(BaselineProvenanceEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/baseline-provenance.md) | Required | Baseline provenance. | getBaselineProvenance(): string | setBaselineProvenance(string baselineProvenance): void |
| `baselineWindowEnd` | `string` | Required | Baseline window end. | getBaselineWindowEnd(): string | setBaselineWindowEnd(string baselineWindowEnd): void |
| `baselineWindowStart` | `string` | Required | Baseline window start. | getBaselineWindowStart(): string | setBaselineWindowStart(string baselineWindowStart): void |
| `currency` | string | Required | This is a container for any-of cases. | getCurrency(): string | setCurrency(string currency): void |
| `currentAmountPerHour` | `string` | Required | Current amount per hour. | getCurrentAmountPerHour(): string | setCurrentAmountPerHour(string currentAmountPerHour): void |
| `excludedFutureCount` | `int` | Required | Excluded future count. | getExcludedFutureCount(): int | setExcludedFutureCount(int excludedFutureCount): void |
| `excludedPastCount` | `int` | Required | Excluded past count. | getExcludedPastCount(): int | setExcludedPastCount(int excludedPastCount): void |
| `limitations` | `string[]` | Required | Limitations. | getLimitations(): array | setLimitations(array limitations): void |
| `policyVersion` | `string` | Required | Policy version. | getPolicyVersion(): string | setPolicyVersion(string policyVersion): void |
| `ratio` | string | Required | This is a container for any-of cases. | getRatio(): string | setRatio(string ratio): void |
| `status` | [`string(Status14Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/status-14.md) | Required | Status. | getStatus(): string | setStatus(string status): void |
| `threshold` | `string` | Required | Threshold. | getThreshold(): string | setThreshold(string threshold): void |
| `totalAmount` | `string` | Required | Total amount. | getTotalAmount(): string | setTotalAmount(string totalAmount): void |
| `transactionCount` | `int` | Required | Transaction count. | getTransactionCount(): int | setTransactionCount(int transactionCount): void |
| `windowBoundary` | `string` | Required, Constant | Window boundary.<br><br>**Value**: `'left_open_right_closed'` | getWindowBoundary(): string | setWindowBoundary(string windowBoundary): void |
| `windowEnd` | `string` | Required | Window end. | getWindowEnd(): string | setWindowEnd(string windowEnd): void |
| `windowHours` | `int` | Required | Window hours. | getWindowHours(): int | setWindowHours(int windowHours): void |
| `windowStart` | `string` | Required | Window start. | getWindowStart(): string | setWindowStart(string windowStart): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\VelocityResponseBuilder;
use TradeGlotLocalConsoleLib\Models\BaselineProvenanceEnum;
use TradeGlotLocalConsoleLib\Models\Status14Enum;

$velocityResponse = VelocityResponseBuilder::init(
    false,
    'baseline_amount_per_hour4',
    BaselineProvenanceEnum::SYNTHETIC_BASELINE,
    'baseline_window_end6',
    'baseline_window_start0',
    'String1',
    'current_amount_per_hour4',
    6,
    154,
    [
        'limitations9',
        'limitations8',
        'limitations7'
    ],
    'policy_version8',
    'String1',
    Status14Enum::NORMAL,
    'threshold8',
    'total_amount6',
    134,
    'window_end0',
    20,
    'window_start6'
)->build();
```



