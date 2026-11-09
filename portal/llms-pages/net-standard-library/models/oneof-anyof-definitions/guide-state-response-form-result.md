# Guide State Response Form Result

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZUZvcm1SZXN1bHQ


# Class Name

`GuideStateResponseFormResult`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`GuideFormResult`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-form-result.md) | GuideStateResponseFormResult.FromGuideFormResult(GuideFormResult guideFormResult) |


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



