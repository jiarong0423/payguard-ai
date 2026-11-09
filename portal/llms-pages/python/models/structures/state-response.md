# State Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlN0YXRlUmVzcG9uc2U

StateResponse.


# Class Name

`StateResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `activity` | [`List[Activity]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/activity.md) | Required | Activity. |
| `disputes` | [`List[DisputeSummary]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/dispute-summary.md) | Required | Disputes. |
| `expires_at` | `str` | Required | Expires at. |
| `policy_version` | `str` | Required | Policy version. |
| `scenario` | [`Scenario`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/scenario.md) | Required | Scenario. |
| `session_id` | `str` | Required | Session id. |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `transactions` | [`List[Transaction]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/transaction.md) | Required | Transactions. |
| `velocity` | [`VelocityResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/velocity-response.md) | Required | VelocityResponse. |


# Example

```python
from tradeglotlocalconsole.models.activity import Activity
from tradeglotlocalconsole.models.baseline_provenance_enum import BaselineProvenanceEnum
from tradeglotlocalconsole.models.dispute_summary import DisputeSummary
from tradeglotlocalconsole.models.scenario import Scenario
from tradeglotlocalconsole.models.state_response import StateResponse
from tradeglotlocalconsole.models.status_14_enum import Status14Enum
from tradeglotlocalconsole.models.status_7_enum import Status7Enum
from tradeglotlocalconsole.models.synthetic_money import SyntheticMoney
from tradeglotlocalconsole.models.transaction import Transaction
from tradeglotlocalconsole.models.velocity_response import VelocityResponse

state_response = StateResponse(
    activity=[
        Activity(
            at='at4',
            id='id8',
            kind='kind6',
            label='label8'
        )
    ],
    disputes=[
        DisputeSummary(
            case_ref='case_ref6',
            dispute_amount=SyntheticMoney(
                currency_code='currency_code6',
                value='value0'
            ),
            opened_at='opened_at0',
            order_ref='order_ref8',
            reason='reason2',
            seller_response_due_date='seller_response_due_date0',
            status=Status7Enum.NEEDS_REVIEW
        )
    ],
    expires_at='expires_at2',
    policy_version='policy_version2',
    scenario=Scenario(
        burst=False,
        dispute=False
    ),
    session_id='session_id4',
    transactions=[
        Transaction(
            amount='amount0',
            currency='currency8',
            occurred_at='occurred_at2',
            order_id='order_id2'
        )
    ],
    velocity=VelocityResponse(
        alert=False,
        baseline_amount_per_hour='baseline_amount_per_hour0',
        baseline_provenance=BaselineProvenanceEnum.SYNTHETIC_BASELINE,
        baseline_window_end='baseline_window_end2',
        baseline_window_start='baseline_window_start4',
        currency='String7',
        current_amount_per_hour='current_amount_per_hour0',
        excluded_future_count=240,
        excluded_past_count=132,
        limitations=[
            'limitations7'
        ],
        policy_version='policy_version4',
        ratio='String5',
        status=Status14Enum.INSUFFICIENT_BASELINE,
        threshold='threshold4',
        total_amount='total_amount2',
        transaction_count=112,
        window_end='window_end6',
        window_hours=2,
        window_start='window_start8'
    )
)
```



