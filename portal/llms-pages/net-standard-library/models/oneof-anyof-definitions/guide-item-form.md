# Guide Item Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlSXRlbUZvcm0


# Class Name

`GuideItemForm`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`GuideForm`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/guide-form.md) | GuideItemForm.FromGuideForm(GuideForm guideForm) |


# GuideForm

## Initialization Code

### Example

```csharp
GuideItemForm value = GuideItemForm.FromGuideForm(
    new GuideForm
    {
        Kind = Kind2Enum.Choice,
        Options = new List<GuideOption>
        {
            new GuideOption
            {
                Label = "label2",
                MValue = "value4",
            },
        },
        Placeholder = GuideFormPlaceholder.FromString("String9"),
    }
);
```



