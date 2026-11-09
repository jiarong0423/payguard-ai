# Tracker Item

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlRyYWNrZXJJdGVt

TrackerItem.


# Class Name

`TrackerItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `carrier` | [`CarrierEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/carrier.md) | Required | Carrier. |
| `carrier_name_other` | String \| nil | Optional | This is a container for any-of cases. |
| `status` | `String` | Required, Constant | Status.<br><br>**Value**: `'SHIPPED'` |
| `tracking_number` | `String` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` |
| `transaction_id` | `String` | Required | Transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9*._-]{1,64}$` |


# Example

```ruby
tracker_item = TrackerItem.new(
  CarrierEnum::FEDEX,
  'SHIPPED',
  'tracking_number6',
  'transaction_id6',
  'String1'
)
```



