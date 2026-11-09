# Velocity Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlZlbG9jaXR5UmVzcG9uc2U

VelocityResponse.


# Interface Name

`VelocityResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `alert` | `boolean` | Required | Alert. |
| `baselineAmountPerHour` | `string` | Required | Baseline amount per hour. |
| `baselineProvenance` | [`BaselineProvenanceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/baseline-provenance.md) | Required | Baseline provenance. |
| `baselineWindowEnd` | `string` | Required | Baseline window end. |
| `baselineWindowStart` | `string` | Required | Baseline window start. |
| `currency` | [`VelocityResponseCurrency`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/velocity-response-currency.md) | Required | This is a container for any-of cases. |
| `currentAmountPerHour` | `string` | Required | Current amount per hour. |
| `excludedFutureCount` | `number` | Required | Excluded future count. |
| `excludedPastCount` | `number` | Required | Excluded past count. |
| `limitations` | `string[]` | Required | Limitations. |
| `policyVersion` | `string` | Required | Policy version. |
| `ratio` | [`VelocityResponseRatio`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/velocity-response-ratio.md) | Required | This is a container for any-of cases. |
| `status` | [`Status14Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/status-14.md) | Required | Status. |
| `threshold` | `string` | Required | Threshold. |
| `totalAmount` | `string` | Required | Total amount. |
| `transactionCount` | `number` | Required | Transaction count. |
| `windowBoundary` | `string` | Required, Constant | Window boundary.<br><br>**Value**: `'left_open_right_closed'` |
| `windowEnd` | `string` | Required | Window end. |
| `windowHours` | `number` | Required | Window hours. |
| `windowStart` | `string` | Required | Window start. |


# Example

```ts
import {
  BaselineProvenanceEnum,
  Status14Enum,
  VelocityResponse,
} from 'tradeglot-local-consolelib';

const velocityResponse: VelocityResponse = {
  advisoryOnly: 'True',
  alert: false,
  baselineAmountPerHour: 'baseline_amount_per_hour4',
  baselineProvenance: BaselineProvenanceEnum.SYNTHETICBASELINE,
  baselineWindowEnd: 'baseline_window_end6',
  baselineWindowStart: 'baseline_window_start0',
  currency: 'String1',
  currentAmountPerHour: 'current_amount_per_hour4',
  excludedFutureCount: 6,
  excludedPastCount: 154,
  limitations: [
    'limitations9',
    'limitations8',
    'limitations7'
  ],
  policyVersion: 'policy_version8',
  ratio: 'String1',
  status: Status14Enum.Normal,
  threshold: 'threshold8',
  totalAmount: 'total_amount6',
  transactionCount: 134,
  windowBoundary: 'left_open_right_closed',
  windowEnd: 'window_end0',
  windowHours: 20,
  windowStart: 'window_start6',
};
```



