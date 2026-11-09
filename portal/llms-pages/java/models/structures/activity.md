# Activity

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkFjdGl2aXR5

Activity.


# Class Name

`Activity`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `At` | `String` | Required | At. | String getAt() | setAt(String at) |
| `Id` | `String` | Required | Id. | String getId() | setId(String id) |
| `Kind` | `String` | Required | Kind. | String getKind() | setKind(String kind) |
| `Label` | `String` | Required | Label. | String getLabel() | setLabel(String label) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` | String getSource() | setSource(String source) |


# Example

```java
import m18000.m0.m0.m127.models.Activity;

Activity activity = new Activity.Builder(
    "at4",
    "id8",
    "kind6",
    "label8",
    "synthetic"
)
.build();
```



