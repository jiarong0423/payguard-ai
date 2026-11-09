# Guide Turn Request Fields

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlVHVyblJlcXVlc3RGaWVsZHM


# Class Name

`GuideTurnRequestFields`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`List<GuideField>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/guide-field.md) | GuideTurnRequestFields.FromListOfGuideField(List<GuideField> listOfGuideField) |


# List<GuideField>

## Initialization Code

### Example

```csharp
GuideTurnRequestFields value = GuideTurnRequestFields.FromListOfGuideField(
    new List<GuideField>
    {
        new GuideField
        {
            Item = "item8",
            MValue = "value8",
        },
    }
);
```



