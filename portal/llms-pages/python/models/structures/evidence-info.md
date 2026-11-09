# Evidence Info

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5mbw

EvidenceInfo.


# Class Name

`EvidenceInfo`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `tracking_info` | [`List[TrackingInfo]`](http://localhost:3000/llms-pages/python/models/structures/tracking-info.md) | Required | Tracking info.<br><br>**Constraints**: *Maximum Items*: `10` |


# Example

```python
from tradeglotlocalconsole.models.carrier_name_enum import CarrierNameEnum
from tradeglotlocalconsole.models.evidence_info import EvidenceInfo
from tradeglotlocalconsole.models.tracking_info import TrackingInfo

evidence_info = EvidenceInfo(
    tracking_info=[
        TrackingInfo(
            carrier_name=CarrierNameEnum.DHL,
            tracking_number='tracking_number6',
            carrier_name_other='String1'
        )
    ]
)
```



