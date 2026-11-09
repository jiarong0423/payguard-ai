# Guide State Response Reply

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZVJlcGx5


# Class Name

`GuideStateResponseReply`


# Cases

| Type |
|  --- |
| [`GuideReply`](http://localhost:3000/llms-pages/typescript/models/structures/guide-reply.md) |


# GuideReply

## Initialization Code

### Example

```ts
const value: GuideStateResponseReply = {
  chooser: ChooserEnum.Form,
  dropped: [
    {
      item: 'item2',
      reason: Reason6Enum.OtherParty,
    }
  ],
  fallbackReason: FallbackReasonEnum.Late,
  stateChanged: false,
  template: TemplateEnum.REVIEW,
  text: 'text0',
};
```



