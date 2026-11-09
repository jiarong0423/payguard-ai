# Guide Gap

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkd1aWRlR2Fw

GuideGap.


# Class Name

`GuideGap`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `conflicting` | `Array[String]` | Required | Conflicting. |
| `missing` | `Array[String]` | Required | Missing. |
| `partial` | `Array[String]` | Required | Partial. |
| `present` | `Array[String]` | Required | Present. |


# Example

```ruby
guide_gap = GuideGap.new(
  [
    'conflicting9',
    'conflicting8',
    'conflicting7'
  ],
  [
    'missing2',
    'missing3'
  ],
  [
    'partial4'
  ],
  [
    'present7'
  ]
)
```



