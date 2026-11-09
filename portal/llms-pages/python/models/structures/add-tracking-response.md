# Add Tracking Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkFkZFRyYWNraW5nUmVzcG9uc2U

AddTrackingResponse.


# Class Name

`AddTrackingResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`TrackerBatch`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/tracker-batch.md) | Required | TrackerBatch. |
| `case_ref` | `str` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `confirm_token` | str \| None | Optional | This is a container for any-of cases. |
| `content_type` | `str` | Required, Constant | Content type.<br><br>**Value**: `"application/json"` |
| `data_source_label` | [`DataSourceLabelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/data-source-label.md) | Required | Data source label. |
| `dispute_id` | `str` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `environment` | `str` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `evidence_class` | [`EvidenceClassEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `external_send` | [`ExternalSendEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/external-send.md) | Required | External send. |
| `human_review_required` | `str` | Required, Constant | Human review required.<br><br>**Value**: `"True"` |
| `method` | `str` | Required, Constant | Method.<br><br>**Value**: `"POST"` |
| `observed_at` | `str` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `path` | `str` | Required, Constant | Path.<br><br>**Value**: `"/v1/shipping/trackers-batch"` |
| `payload_sha_256` | str \| None | Optional | This is a container for any-of cases. |
| `paypal_debug_id` | str \| None | Optional | This is a container for any-of cases. |
| `provider_submission` | [`ProviderSubmissionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `readback` | [`ReadbackEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/readback.md) | Required | Readback. |
| `send_guard` | [`SendGuard`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). |
| `source` | [`SourceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/source.md) | Required | Source. |
| `submit_flag_enabled` | `bool` | Required | Submit flag enabled. |


# Example

```python
from tradeglotlocalconsole.models.account_status_enum import AccountStatusEnum
from tradeglotlocalconsole.models.add_tracking_response import AddTrackingResponse
from tradeglotlocalconsole.models.carrier_enum import CarrierEnum
from tradeglotlocalconsole.models.data_source_label_enum import DataSourceLabelEnum
from tradeglotlocalconsole.models.evidence_class_enum import EvidenceClassEnum
from tradeglotlocalconsole.models.external_send_enum import ExternalSendEnum
from tradeglotlocalconsole.models.provider_money import ProviderMoney
from tradeglotlocalconsole.models.provider_submission_enum import ProviderSubmissionEnum
from tradeglotlocalconsole.models.readback_enum import ReadbackEnum
from tradeglotlocalconsole.models.send_guard import SendGuard
from tradeglotlocalconsole.models.source_enum import SourceEnum
from tradeglotlocalconsole.models.tracker_batch import TrackerBatch
from tradeglotlocalconsole.models.tracker_item import TrackerItem

add_tracking_response = AddTrackingResponse(
    body=TrackerBatch(
        trackers=[
            TrackerItem(
                carrier=CarrierEnum.JP_JAPANPOST,
                tracking_number='tracking_number0',
                transaction_id='transaction_id0',
                carrier_name_other='String5'
            )
        ]
    ),
    case_ref='case_ref0',
    data_source_label=DataSourceLabelEnum.SANDBOX,
    dispute_id='dispute_id8',
    evidence_class=EvidenceClassEnum.SYNTHETIC_FIXTURE,
    external_send=ExternalSendEnum.FROZEN,
    observed_at='observed_at0',
    provider_submission=ProviderSubmissionEnum.NOT_PERFORMED,
    readback=ReadbackEnum.ADD_TRACKING_PREVIEW,
    send_guard=SendGuard(
        account_status=AccountStatusEnum.MATCH,
        case_ref='case_ref6',
        dispute_masked='dispute_masked0',
        bound_dispute_masked='String3',
        case_reason='String7',
        dispute_amount=ProviderMoney(
            currency_code='currency_code0',
            value='value6'
        ),
        dispute_reason='String9',
        dispute_seller_masked='String1'
    ),
    source=SourceEnum.PAYPAL_SANDBOX,
    submit_flag_enabled=False,
    confirm_token='String5',
    payload_sha_256='String5',
    paypal_debug_id='String5'
)
```



