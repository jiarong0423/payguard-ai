# Tracker Batch

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlRyYWNrZXJCYXRjaA

TrackerBatch.


# Class Name

`TrackerBatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `trackers` | [`Array[TrackerItem]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/tracker-item.md) | Required | Trackers.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `1` |


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



