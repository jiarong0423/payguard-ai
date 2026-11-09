# Guide Dropped

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkd1aWRlRHJvcHBlZA

GuideDropped.


# Class Name

`GuideDropped`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Item` | `String` | Required | Item. | String getItem() | setItem(String item) |
| `Reason` | [`Reason6Enum`](http://localhost:3000/llms-pages/java/models/enumerations/reason-6.md) | Required | Reason. | Reason6Enum getReason() | setReason(Reason6Enum reason) |


# Example

```java
import m18000.m0.m0.m127.models.GuideDropped;
import m18000.m0.m0.m127.models.Reason6Enum;

GuideDropped guideDropped = new GuideDropped.Builder(
    "item6",
    Reason6Enum.OTHER_PARTY
)
.build();
```



