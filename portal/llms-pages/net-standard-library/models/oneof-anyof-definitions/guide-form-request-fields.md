# Guide Form Request Fields

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlcXVlc3RGaWVsZHM


# Class Name

`GuideFormRequestFields`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`List<GuideField>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-field.md) | GuideFormRequestFields.FromListOfGuideField(List<GuideField> listOfGuideField) |


# List<GuideField>

## Initialization Code

### Example

```csharp
GuideFormRequestFields value = GuideFormRequestFields.FromListOfGuideField(
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



