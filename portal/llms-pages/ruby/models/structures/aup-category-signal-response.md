# Aup Category Signal Response

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVzcG9uc2U

Optional Channel3 signal shown next to the AUP result; it never changes the rule decision.


# Class Name

`AupCategorySignalResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `affects_decision` | `String` | Required, Constant | Affects decision.<br><br>**Value**: `'False'` |
| `reason` | [Reason](http://localhost:3000/llms-pages/ruby/models/enumerations/reason.md) | Required | This is a container for any-of cases. |
| `signal` | [CategorySignal](http://localhost:3000/llms-pages/ruby/models/structures/category-signal.md) | Required | This is a container for any-of cases. |
| `status` | [`Status2Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/status-2.md) | Required | Status. |


# Example

```ruby
aup_category_signal_response = AupCategorySignalResponse.new(
  'False',
  ReasonEnum::TIMEOUT,
  CategorySignal.new(
    'String9',
    ConfidenceEnum::HIGH,
    'channel3'
  ),
  Status2Enum::OFF
)
```



