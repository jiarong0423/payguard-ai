# Guide Turn Request Fields

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlVHVyblJlcXVlc3RGaWVsZHM


# Class Name

`GuideTurnRequestFields`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`List<GuideField>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-field.md) | GuideTurnRequestFields.FromListOfGuideField(List<GuideField> listOfGuideField) |


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



