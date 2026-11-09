# Evidence Info

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5mbw

EvidenceInfo.


# Class Name

`EvidenceInfo`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `tracking_info` | [`Array[TrackingInfo]`](http://localhost:3000/llms-pages/ruby/models/structures/tracking-info.md) | Required | Tracking info.<br><br>**Constraints**: *Maximum Items*: `10` |


# Example

```ruby
evidence_info = EvidenceInfo.new(
  [
    TrackingInfo.new(
      CarrierNameEnum::DHL,
      'tracking_number6',
      'String1'
    )
  ]
)
```



