# Category Signal

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkNhdGVnb3J5U2lnbmFs

CategorySignal.


# Class Name

`CategorySignal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | String | Required | This is a container for any-of cases. |
| `confidence` | [Confidence](http://localhost:3000/llms-pages/ruby/models/enumerations/confidence.md) | Required | This is a container for any-of cases. |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'channel3'` |


# Example

```ruby
category_signal = CategorySignal.new(
  'String9',
  ConfidenceEnum::HIGH,
  'channel3'
)
```



