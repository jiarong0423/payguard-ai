# Dispute List Response

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkRpc3B1dGVMaXN0UmVzcG9uc2U

DisputeListResponse.


# Class Name

`DisputeListResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `data_source_label` | [`DataSourceLabelEnum`](http://localhost:3000/llms-pages/python/models/enumerations/data-source-label.md) | Required | Data source label. |
| `environment` | `str` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `evidence_class` | [`EvidenceClassEnum`](http://localhost:3000/llms-pages/python/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `items` | [`List[DisputeRecord]`](http://localhost:3000/llms-pages/python/models/structures/dispute-record.md) | Required | Items.<br><br>**Constraints**: *Maximum Items*: `20` |
| `observed_at` | `str` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypal_debug_id` | str \| None | Optional | This is a container for any-of cases. |
| `provider_submission` | [`ProviderSubmissionEnum`](http://localhost:3000/llms-pages/python/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `readback` | `str` | Required, Constant | Readback.<br><br>**Value**: `"GET_LIST"` |
| `source` | [`SourceEnum`](http://localhost:3000/llms-pages/python/models/enumerations/source.md) | Required | Source. |


# Example

```python
from tradeglotlocalconsole.models.data_source_label_enum import DataSourceLabelEnum
from tradeglotlocalconsole.models.dispute_life_cycle_stage_enum import DisputeLifeCycleStageEnum
from tradeglotlocalconsole.models.dispute_list_response import DisputeListResponse
from tradeglotlocalconsole.models.dispute_record import DisputeRecord
from tradeglotlocalconsole.models.evidence_class_enum import EvidenceClassEnum
from tradeglotlocalconsole.models.provider_money import ProviderMoney
from tradeglotlocalconsole.models.provider_submission_enum import ProviderSubmissionEnum
from tradeglotlocalconsole.models.reason_2_enum import Reason2Enum
from tradeglotlocalconsole.models.source_enum import SourceEnum
from tradeglotlocalconsole.models.status_3_enum import Status3Enum

dispute_list_response = DisputeListResponse(
    data_source_label=DataSourceLabelEnum.SANDBOX,
    evidence_class=EvidenceClassEnum.SYNTHETIC_FIXTURE,
    items=[
        DisputeRecord(
            create_time='create_time4',
            dispute_amount=ProviderMoney(
                currency_code='currency_code6',
                value='value0'
            ),
            dispute_id='dispute_id0',
            dispute_life_cycle_stage=DisputeLifeCycleStageEnum.PRE_ARBITRATION,
            reason=Reason2Enum.CREDIT_NOT_PROCESSED,
            status=Status3Enum.UNDER_REVIEW,
            dispute_state='String1',
            seller_response_due_date='String7',
            update_time='String1'
        )
    ],
    observed_at='observed_at4',
    provider_submission=ProviderSubmissionEnum.NOT_PERFORMED,
    source=SourceEnum.PAYPAL_SANDBOX,
    paypal_debug_id='String1'
)
```



