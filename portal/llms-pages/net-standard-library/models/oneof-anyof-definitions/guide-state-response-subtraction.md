# Guide State Response Subtraction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZVN1YnRyYWN0aW9u


# Class Name

`GuideStateResponseSubtraction`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`GuideSubtraction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/guide-subtraction.md) | GuideStateResponseSubtraction.FromGuideSubtraction(GuideSubtraction guideSubtraction) |


# GuideSubtraction

## Initialization Code

### Example

```csharp
GuideStateResponseSubtraction value = GuideStateResponseSubtraction.FromGuideSubtraction(
    new GuideSubtraction
    {
        Left = 64,
        Needed = 190,
        Taken = 178,
        Text = "text0",
    }
);
```



