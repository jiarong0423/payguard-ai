# Evidence Input Item

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXRJdGVt

EvidenceInputItem.


# Class Name

`EvidenceInputItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `evidence_info` | [`EvidenceInfo`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/evidence-info.md) | Required | EvidenceInfo. |
| `evidence_type` | `str` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` |
| `notes` | `str` | Required | Notes.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```python
from tradeglotlocalconsole.models.carrier_name_enum import CarrierNameEnum
from tradeglotlocalconsole.models.evidence_info import EvidenceInfo
from tradeglotlocalconsole.models.evidence_input_item import EvidenceInputItem
from tradeglotlocalconsole.models.tracking_info import TrackingInfo

evidence_input_item = EvidenceInputItem(
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
```



