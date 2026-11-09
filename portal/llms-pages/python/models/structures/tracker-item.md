# Tracker Item

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlRyYWNrZXJJdGVt

TrackerItem.


# Class Name

`TrackerItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `carrier` | [`CarrierEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/carrier.md) | Required | Carrier. |
| `carrier_name_other` | str \| None | Optional | This is a container for any-of cases. |
| `status` | `str` | Required, Constant | Status.<br><br>**Value**: `"SHIPPED"` |
| `tracking_number` | `str` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` |
| `transaction_id` | `str` | Required | Transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9*._-]{1,64}$` |


# Example

```python
from tradeglotlocalconsole.models.carrier_enum import CarrierEnum
from tradeglotlocalconsole.models.tracker_item import TrackerItem

tracker_item = TrackerItem(
    carrier=CarrierEnum.FEDEX,
    tracking_number='tracking_number6',
    transaction_id='transaction_id6',
    carrier_name_other='String1'
)
```



