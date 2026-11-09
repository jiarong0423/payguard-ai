# Activity

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkFjdGl2aXR5

Activity.


# Class Name

`Activity`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `At` | `string` | Required | At. |
| `Id` | `string` | Required | Id. |
| `Kind` | `string` | Required | Kind. |
| `Label` | `string` | Required | Label. |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

Activity activity = new Activity
{
    At = "at4",
    Id = "id8",
    Kind = "kind6",
    Label = "label8",
    Source = "synthetic",
};
```



