# Category Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkNhdGVnb3J5U2lnbmFs

CategorySignal.


# Class Name

`CategorySignal`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Category` | [`CategorySignalCategory`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/category-signal-category.md) | Required | This is a container for any-of cases. | CategorySignalCategory getCategory() | setCategory(CategorySignalCategory category) |
| `Confidence` | [`CategorySignalConfidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/category-signal-confidence.md) | Required | This is a container for any-of cases. | CategorySignalConfidence getConfidence() | setConfidence(CategorySignalConfidence confidence) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"channel3"` | String getSource() | setSource(String source) |


# Example

```java
import m18000.m0.m0.m127.models.CategorySignal;
import m18000.m0.m0.m127.models.ConfidenceEnum;
import m18000.m0.m0.m127.models.containers.CategorySignalCategory;
import m18000.m0.m0.m127.models.containers.CategorySignalConfidence;

CategorySignal categorySignal = new CategorySignal.Builder(
    CategorySignalCategory.fromString(
        "String1"
    ),
    CategorySignalConfidence.fromConfidence(
        ConfidenceEnum.HIGH
    ),
    "channel3"
)
.build();
```



