# Tracking Info

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlRyYWNraW5nSW5mbw

TrackingInfo.


# Class Name

`TrackingInfo`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `carrier_name` | [`CarrierNameEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/carrier-name.md) | Required | Carrier name. |
| `carrier_name_other` | str \| None | Optional | This is a container for any-of cases. |
| `tracking_number` | `str` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` |


# Example

```python
from tradeglotlocalconsole.models.carrier_name_enum import CarrierNameEnum
from tradeglotlocalconsole.models.tracking_info import TrackingInfo

tracking_info = TrackingInfo(
    carrier_name=CarrierNameEnum.DHL,
    tracking_number='tracking_number6',
    carrier_name_other='String1'
)
```



