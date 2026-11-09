# Evidence Input

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXQ

EvidenceInput.


# Class Name

`EvidenceInput`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `evidences` | [`List[EvidenceInputItem]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/evidence-input-item.md) | Required | Evidences.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |


# Example

```python
from tradeglotlocalconsole.models.carrier_name_enum import CarrierNameEnum
from tradeglotlocalconsole.models.evidence_info import EvidenceInfo
from tradeglotlocalconsole.models.evidence_input import EvidenceInput
from tradeglotlocalconsole.models.evidence_input_item import EvidenceInputItem
from tradeglotlocalconsole.models.tracking_info import TrackingInfo

evidence_input = EvidenceInput(
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
)
```



