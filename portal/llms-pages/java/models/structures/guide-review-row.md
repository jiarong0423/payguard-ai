# Guide Review Row

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3Um93

GuideReviewRow.


# Class Name

`GuideReviewRow`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Item` | `String` | Required | Item. | String getItem() | setItem(String item) |
| `Source` | [`Source9Enum`](http://localhost:3000/llms-pages/java/models/enumerations/source-9.md) | Required | Source. | Source9Enum getSource() | setSource(Source9Enum source) |
| `Value` | `String` | Required | Value.<br><br>**Constraints**: *Maximum Length*: `120` | String getValue() | setValue(String value) |


# Example

```java
import m18000.m0.m0.m127.models.GuideReviewRow;
import m18000.m0.m0.m127.models.Source9Enum;

GuideReviewRow guideReviewRow = new GuideReviewRow.Builder(
    "item6",
    Source9Enum.WORDS,
    "value6"
)
.build();
```



