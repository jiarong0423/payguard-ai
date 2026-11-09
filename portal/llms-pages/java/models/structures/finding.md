# Finding

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkZpbmRpbmc

Finding.


# Class Name

`Finding`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Category` | [`CategoryEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/category.md) | Required | Category. | CategoryEnum getCategory() | setCategory(CategoryEnum category) |
| `Code` | `String` | Required, Constant | Code.<br><br>**Value**: `"keyword_requires_policy_review"` | String getCode() | setCode(String code) |


# Example

```java
import m18000.m0.m0.m127.models.CategoryEnum;
import m18000.m0.m0.m127.models.Finding;

Finding finding = new Finding.Builder(
    CategoryEnum.UNSUPPORTED_FINANCIAL_PROMISE,
    "keyword_requires_policy_review"
)
.build();
```



