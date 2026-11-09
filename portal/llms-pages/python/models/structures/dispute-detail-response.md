# Dispute Detail Response

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkRpc3B1dGVEZXRhaWxSZXNwb25zZQ

DisputeDetailResponse.


# Class Name

`DisputeDetailResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `create_time` | `str` | Required | Create time.<br><br>**Constraints**: *Pattern*: `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z$` |
| `data_source_label` | [`DataSourceLabelEnum`](http://localhost:3000/llms-pages/python/models/enumerations/data-source-label.md) | Required | Data source label. |
| `dispute_amount` | [`ProviderMoney`](http://localhost:3000/llms-pages/python/models/structures/provider-money.md) | Required | ProviderMoney. |
| `dispute_channel` | str \| None | Optional | This is a container for any-of cases. |
| `dispute_id` | `str` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `dispute_life_cycle_stage` | [`DisputeLifeCycleStageEnum`](http://localhost:3000/llms-pages/python/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `dispute_state` | str \| None | Optional | This is a container for any-of cases. |
| `disputed_transactions` | [`List[DisputedTransaction]`](http://localhost:3000/llms-pages/python/models/structures/disputed-transaction.md) | Required | Disputed transactions.<br><br>**Constraints**: *Maximum Items*: `10` |
| `environment` | `str` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `evidence_class` | [`EvidenceClassEnum`](http://localhost:3000/llms-pages/python/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `evidences` | [`List[DisputeEvidenceRow]`](http://localhost:3000/llms-pages/python/models/structures/dispute-evidence-row.md) | Required | Evidences.<br><br>**Constraints**: *Maximum Items*: `20` |
| `observed_at` | `str` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypal_debug_id` | str \| None | Optional | This is a container for any-of cases. |
| `provider_submission` | [`ProviderSubmissionEnum`](http://localhost:3000/llms-pages/python/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `readback` | `str` | Required, Constant | Readback.<br><br>**Value**: `"GET_DETAIL"` |
| `reason` | [`Reason2Enum`](http://localhost:3000/llms-pages/python/models/enumerations/reason-2.md) | Required | Reason. |
| `seller_response_due_date` | str \| None | Optional | This is a container for any-of cases. |
| `source` | [`SourceEnum`](http://localhost:3000/llms-pages/python/models/enumerations/source.md) | Required | Source. |
| `status` | [`Status3Enum`](http://localhost:3000/llms-pages/python/models/enumerations/status-3.md) | Required | Status. |
| `update_time` | str \| None | Optional | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.data_source_label_enum import DataSourceLabelEnum
from tradeglotlocalconsole.models.dispute_detail_response import DisputeDetailResponse
from tradeglotlocalconsole.models.dispute_evidence_row import DisputeEvidenceRow
from tradeglotlocalconsole.models.dispute_life_cycle_stage_enum import DisputeLifeCycleStageEnum
from tradeglotlocalconsole.models.disputed_transaction import DisputedTransaction
from tradeglotlocalconsole.models.evidence_class_enum import EvidenceClassEnum
from tradeglotlocalconsole.models.provider_money import ProviderMoney
from tradeglotlocalconsole.models.provider_submission_enum import ProviderSubmissionEnum
from tradeglotlocalconsole.models.reason_2_enum import Reason2Enum
from tradeglotlocalconsole.models.source_3_enum import Source3Enum
from tradeglotlocalconsole.models.source_enum import SourceEnum
from tradeglotlocalconsole.models.status_3_enum import Status3Enum

dispute_detail_response = DisputeDetailResponse(
    create_time='create_time6',
    data_source_label=DataSourceLabelEnum.SANDBOX,
    dispute_amount=ProviderMoney(
        currency_code='currency_code6',
        value='value0'
    ),
    dispute_id='dispute_id2',
    dispute_life_cycle_stage=DisputeLifeCycleStageEnum.UNKNOWN,
    disputed_transactions=[
        DisputedTransaction(
            seller_transaction_id='seller_transaction_id2',
            gross_amount=ProviderMoney(
                currency_code='currency_code0',
                value='value6'
            ),
            seller_protection_eligible=True,
            transaction_status='String7'
        )
    ],
    evidence_class=EvidenceClassEnum.AUTHENTIC_SANDBOX_RESPONSE,
    evidences=[
        DisputeEvidenceRow(
            evidence_type='evidence_type2',
            source=Source3Enum.SUBMITTED_BY_PARTNER,
            action='String1',
            date='String9'
        )
    ],
    observed_at='observed_at4',
    provider_submission=ProviderSubmissionEnum.NOT_PERFORMED,
    reason=Reason2Enum.CANCELED_RECURRING_BILLING,
    source=SourceEnum.PAYPAL_SANDBOX,
    status=Status3Enum.RESOLVED,
    dispute_channel='String5',
    dispute_state='String9',
    paypal_debug_id='String1',
    seller_response_due_date='String9',
    update_time='String3'
)
```



