# Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkV2aWRlbmNl

Evidence.


# Class Name

`Evidence`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `carrier_status` | String \| nil | Optional | This is a container for any-of cases. |
| `delivered_at` | String \| nil | Optional | This is a container for any-of cases. |
| `evidence_source` | `String` | Required, Constant | Evidence source.<br><br>**Value**: `'synthetic'` |
| `opened_at` | String \| nil | Optional | This is a container for any-of cases. |
| `order_created_at` | String \| nil | Optional | This is a container for any-of cases. |
| `reason` | String \| nil | Optional | This is a container for any-of cases. |


# Example

```ruby
evidence = Evidence.new(
  'synthetic',
  'String5',
  'String1',
  'String1',
  'String3',
  'String3'
)
```



