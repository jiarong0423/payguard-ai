# Signal

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlNpZ25hbA

Signal.


# Class Name

`Signal`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | String \| nil | Optional | This is a container for any-of cases. |
| `confidence` | [Confidence](http://localhost:3000/llms-pages/ruby/models/enumerations/confidence.md) \| nil | Optional | This is a container for any-of cases. |
| `source` | [`Source2Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/source-2.md) | Optional | Source. |


# Example

```ruby
signal = Signal.new(
  'String1',
  ConfidenceEnum::HIGH,
  Source2Enum::CHANNEL3
)
```



