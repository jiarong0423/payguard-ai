# Guide State Response Reply

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZVJlcGx5


# Data Type

`GuideReply`


# Cases

| Type |
|  --- |
| [`GuideReply`](http://localhost:3000/llms-pages/ruby/models/structures/guide-reply.md) |


# GuideReply

## Initialization Code

### Example

```ruby
value = GuideReply.new(
  ChooserEnum::FORM,
  [
    GuideDropped.new(
      'item2',
      Reason6Enum::OTHER_PARTY
    )
  ],
  FallbackReasonEnum::LATE,
  false,
  TemplateEnum::REVIEW,
  'text0'
)
```



