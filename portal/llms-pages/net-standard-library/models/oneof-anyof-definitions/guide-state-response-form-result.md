# Guide State Response Form Result

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZUZvcm1SZXN1bHQ


# Class Name

`GuideStateResponseFormResult`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`GuideFormResult`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/guide-form-result.md) | GuideStateResponseFormResult.FromGuideFormResult(GuideFormResult guideFormResult) |


# GuideFormResult

## Initialization Code

### Example

```csharp
GuideStateResponseFormResult value = GuideStateResponseFormResult.FromGuideFormResult(
    new GuideFormResult
    {
        Item = "item2",
        Valid = false,
    }
);
```



