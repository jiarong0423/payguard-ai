# Tracker Batch

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlRyYWNrZXJCYXRjaA

TrackerBatch.


# Class Name

`TrackerBatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `trackers` | [`List[TrackerItem]`](http://localhost:3000/llms-pages/python/models/structures/tracker-item.md) | Required | Trackers.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `1` |


# Example

```python
from tradeglotlocalconsole.models.carrier_enum import CarrierEnum
from tradeglotlocalconsole.models.tracker_batch import TrackerBatch
from tradeglotlocalconsole.models.tracker_item import TrackerItem

tracker_batch = TrackerBatch(
    trackers=[
        TrackerItem(
            carrier=CarrierEnum.JP_JAPANPOST,
            tracking_number='tracking_number0',
            transaction_id='transaction_id0',
            carrier_name_other='String5'
        )
    ]
)
```



