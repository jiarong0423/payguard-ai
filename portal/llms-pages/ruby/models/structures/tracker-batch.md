# Tracker Batch

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlRyYWNrZXJCYXRjaA

TrackerBatch.


# Class Name

`TrackerBatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `trackers` | [`Array[TrackerItem]`](http://localhost:3000/llms-pages/ruby/models/structures/tracker-item.md) | Required | Trackers.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `1` |


# Example

```ruby
tracker_batch = TrackerBatch.new(
  [
    TrackerItem.new(
      CarrierEnum::JP_JAPANPOST,
      'SHIPPED',
      'tracking_number0',
      'transaction_id0',
      'String5'
    )
  ]
)
```



