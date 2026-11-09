# Tracking Info

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlRyYWNraW5nSW5mbw

TrackingInfo.


# Class Name

`TrackingInfo`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `carrier_name` | [`CarrierNameEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/carrier-name.md) | Required | Carrier name. |
| `carrier_name_other` | String \| nil | Optional | This is a container for any-of cases. |
| `tracking_number` | `String` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` |


# Example

```ruby
tracking_info = TrackingInfo.new(
  CarrierNameEnum::DHL,
  'tracking_number6',
  'String1'
)
```



