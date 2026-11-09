# Guide Field Result

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkd1aWRlRmllbGRSZXN1bHQ

GuideFieldResult.


# Class Name

`GuideFieldResult`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Deferred` | `boolean` | Required | Deferred. | boolean getDeferred() | setDeferred(boolean deferred) |
| `Item` | `String` | Required | Item. | String getItem() | setItem(String item) |
| `Valid` | `boolean` | Required | Valid. | boolean getValid() | setValid(boolean valid) |


# Example

```java
import m18000.m0.m0.m127.models.GuideFieldResult;

GuideFieldResult guideFieldResult = new GuideFieldResult.Builder(
    false,
    "item8",
    false
)
.build();
```



