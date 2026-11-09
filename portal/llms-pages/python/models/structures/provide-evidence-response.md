# Provide Evidence Response

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlc3BvbnNl

ProvideEvidenceResponse.


# Class Name

`ProvideEvidenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_ref` | `str` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `confirm_token` | str \| None | Optional | This is a container for any-of cases. |
| `content_type` | `str` | Required, Constant | Content type.<br><br>**Value**: `"multipart/form-data"` |
| `data_source_label` | [`DataSourceLabelEnum`](http://localhost:3000/llms-pages/python/models/enumerations/data-source-label.md) | Required | Data source label. |
| `dispute_id` | `str` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `environment` | `str` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `evidence_class` | [`EvidenceClassEnum`](http://localhost:3000/llms-pages/python/models/enumerations/evidence-class.md) | Required | Evidence class. |
| `external_send` | [`ExternalSendEnum`](http://localhost:3000/llms-pages/python/models/enumerations/external-send.md) | Required | External send. |
| `files` | [`List[MultipartFilePart]`](http://localhost:3000/llms-pages/python/models/structures/multipart-file-part.md) | Required | Files.<br><br>**Constraints**: *Maximum Items*: `20` |
| `human_review_required` | `str` | Required, Constant | Human review required.<br><br>**Value**: `"True"` |
| `input` | [`EvidenceInput`](http://localhost:3000/llms-pages/python/models/structures/evidence-input.md) | Required | EvidenceInput. |
| `method` | `str` | Required, Constant | Method.<br><br>**Value**: `"POST"` |
| `observed_at` | `str` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `path` | `str` | Required | Path.<br><br>**Constraints**: *Pattern*: `^/v1/customer/disputes/PP-[A-Z0-9][A-Z0-9-]{2,62}/provide-evidence$` |
| `payload_sha_256` | str \| None | Optional | This is a container for any-of cases. |
| `paypal_debug_id` | str \| None | Optional | This is a container for any-of cases. |
| `provider_submission` | [`ProviderSubmissionEnum`](http://localhost:3000/llms-pages/python/models/enumerations/provider-submission.md) | Required | Provider submission. |
| `readback` | [`Readback1Enum`](http://localhost:3000/llms-pages/python/models/enumerations/readback-1.md) | Required | Readback. |
| `send_guard` | [`SendGuard`](http://localhost:3000/llms-pages/python/models/structures/send-guard.md) | Required | (r25 send guard) What a send carries and to whom, side by side; every account id is masked (first 2, last 4). |
| `source` | [`SourceEnum`](http://localhost:3000/llms-pages/python/models/enumerations/source.md) | Required | Source. |
| `submit_flag_enabled` | `bool` | Required | Submit flag enabled. |


# Example

```python
from tradeglotlocalconsole.models.account_status_enum import AccountStatusEnum
from tradeglotlocalconsole.models.carrier_name_enum import CarrierNameEnum
from tradeglotlocalconsole.models.content_type_enum import ContentTypeEnum
from tradeglotlocalconsole.models.data_source_label_enum import DataSourceLabelEnum
from tradeglotlocalconsole.models.evidence_class_enum import EvidenceClassEnum
from tradeglotlocalconsole.models.evidence_info import EvidenceInfo
from tradeglotlocalconsole.models.evidence_input import EvidenceInput
from tradeglotlocalconsole.models.evidence_input_item import EvidenceInputItem
from tradeglotlocalconsole.models.external_send_enum import ExternalSendEnum
from tradeglotlocalconsole.models.multipart_file_part import MultipartFilePart
from tradeglotlocalconsole.models.provide_evidence_response import ProvideEvidenceResponse
from tradeglotlocalconsole.models.provider_money import ProviderMoney
from tradeglotlocalconsole.models.provider_submission_enum import ProviderSubmissionEnum
from tradeglotlocalconsole.models.readback_1_enum import Readback1Enum
from tradeglotlocalconsole.models.send_guard import SendGuard
from tradeglotlocalconsole.models.source_enum import SourceEnum
from tradeglotlocalconsole.models.tracking_info import TrackingInfo

provide_evidence_response = ProvideEvidenceResponse(
    case_ref='case_ref4',
    data_source_label=DataSourceLabelEnum.SANDBOX,
    dispute_id='dispute_id2',
    evidence_class=EvidenceClassEnum.SYNTHETIC_TEST_RESPONSE,
    external_send=ExternalSendEnum.FROZEN,
    files=[
        MultipartFilePart(
            byte_length=68,
            content_type=ContentTypeEnum.ENUM_IMAGEPNG,
            filename='filename6',
            name='name4'
        )
    ],
    input=EvidenceInput(
        evidences=[
            EvidenceInputItem(
                evidence_info=EvidenceInfo(
                    tracking_info=[
                        TrackingInfo(
                            carrier_name=CarrierNameEnum.DHL,
                            tracking_number='tracking_number6',
                            carrier_name_other='String1'
                        )
                    ]
                ),
                evidence_type='evidence_type2',
                notes='notes2'
            )
        ]
    ),
    observed_at='observed_at4',
    path='path4',
    provider_submission=ProviderSubmissionEnum.NOT_PERFORMED,
    readback=Readback1Enum.PROVIDE_EVIDENCE_PREVIEW,
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
    confirm_token='String1',
    payload_sha_256='String1',
    paypal_debug_id='String1'
)
```



