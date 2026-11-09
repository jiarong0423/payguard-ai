# Velocity Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlZlbG9jaXR5UmVzcG9uc2U

VelocityResponse.


# Class Name

`VelocityResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `str` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `alert` | `bool` | Required | Alert. |
| `baseline_amount_per_hour` | `str` | Required | Baseline amount per hour. |
| `baseline_provenance` | [`BaselineProvenanceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/baseline-provenance.md) | Required | Baseline provenance. |
| `baseline_window_end` | `str` | Required | Baseline window end. |
| `baseline_window_start` | `str` | Required | Baseline window start. |
| `currency` | str | Required | This is a container for any-of cases. |
| `current_amount_per_hour` | `str` | Required | Current amount per hour. |
| `excluded_future_count` | `int` | Required | Excluded future count. |
| `excluded_past_count` | `int` | Required | Excluded past count. |
| `limitations` | `List[str]` | Required | Limitations. |
| `policy_version` | `str` | Required | Policy version. |
| `ratio` | str | Required | This is a container for any-of cases. |
| `status` | [`Status14Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/status-14.md) | Required | Status. |
| `threshold` | `str` | Required | Threshold. |
| `total_amount` | `str` | Required | Total amount. |
| `transaction_count` | `int` | Required | Transaction count. |
| `window_boundary` | `str` | Required, Constant | Window boundary.<br><br>**Value**: `"left_open_right_closed"` |
| `window_end` | `str` | Required | Window end. |
| `window_hours` | `int` | Required | Window hours. |
| `window_start` | `str` | Required | Window start. |


# Example

```python
from tradeglotlocalconsole.models.baseline_provenance_enum import BaselineProvenanceEnum
from tradeglotlocalconsole.models.status_14_enum import Status14Enum
from tradeglotlocalconsole.models.velocity_response import VelocityResponse

velocity_response = VelocityResponse(
    alert=False,
    baseline_amount_per_hour='baseline_amount_per_hour6',
    baseline_provenance=BaselineProvenanceEnum.SYNTHETIC_BASELINE,
    baseline_window_end='baseline_window_end6',
    baseline_window_start='baseline_window_start0',
    currency='String1',
    current_amount_per_hour='current_amount_per_hour4',
    excluded_future_count=110,
    excluded_past_count=2,
    limitations=[
        'limitations7',
        'limitations6',
        'limitations5'
    ],
    policy_version='policy_version8',
    ratio='String1',
    status=Status14Enum.INSUFFICIENT_BASELINE,
    threshold='threshold8',
    total_amount='total_amount6',
    transaction_count=238,
    window_end='window_end0',
    window_hours=124,
    window_start='window_start6'
)
```



