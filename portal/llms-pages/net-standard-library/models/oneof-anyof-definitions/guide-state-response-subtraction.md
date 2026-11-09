# Guide State Response Subtraction

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZVN1YnRyYWN0aW9u


# Class Name

`GuideStateResponseSubtraction`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`GuideSubtraction`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-subtraction.md) | GuideStateResponseSubtraction.FromGuideSubtraction(GuideSubtraction guideSubtraction) |


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



