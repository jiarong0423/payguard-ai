# Guide Field

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlRmllbGQ

GuideField.


# Class Name

`GuideField`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Item` | `string` | Required | Item.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z_]+$` |
| `MValue` | `string` | Required | Value.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `120` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

GuideField guideField = new GuideField
{
    Item = "item8",
    MValue = "value8",
};
```



