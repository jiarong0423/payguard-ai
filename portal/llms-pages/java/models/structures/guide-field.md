# Guide Field

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkd1aWRlRmllbGQ

GuideField.


# Class Name

`GuideField`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Item` | `String` | Required | Item.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z_]+$` | String getItem() | setItem(String item) |
| `Value` | `String` | Required | Value.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `120` | String getValue() | setValue(String value) |


# Example

```java
import m18000.m0.m0.m127.models.GuideField;

GuideField guideField = new GuideField.Builder(
    "item8",
    "value8"
)
.build();
```



