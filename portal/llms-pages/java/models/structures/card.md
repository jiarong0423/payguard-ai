# Card

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkNhcmQ

Card.


# Class Name

`Card`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Brand` | [`CardBrand`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/card-brand.md) | Optional | This is a container for any-of cases. | CardBrand getBrand() | setBrand(CardBrand brand) |
| `Category` | [`CardCategory`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/card-category.md) | Optional | This is a container for any-of cases. | CardCategory getCategory() | setCategory(CardCategory category) |
| `ImageUrl` | [`CardImageUrl`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/card-image-url.md) | Optional | This is a container for any-of cases. | CardImageUrl getImageUrl() | setImageUrl(CardImageUrl imageUrl) |
| `KeyFeatures` | `List<String>` | Optional | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | List<String> getKeyFeatures() | setKeyFeatures(List<String> keyFeatures) |
| `Materials` | `List<String>` | Optional | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | List<String> getMaterials() | setMaterials(List<String> materials) |
| `ProductId` | `String` | Optional | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` | String getProductId() | setProductId(String productId) |
| `Title` | `String` | Optional | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | String getTitle() | setTitle(String title) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.Card;
import m18000.m0.m0.m127.models.containers.CardBrand;
import m18000.m0.m0.m127.models.containers.CardCategory;
import m18000.m0.m0.m127.models.containers.CardImageUrl;

Card card = new Card.Builder()
    .brand(CardBrand.fromString(
        "String1"
    ))
    .category(CardCategory.fromString(
        "String5"
    ))
    .imageUrl(CardImageUrl.fromString(
        "String3"
    ))
    .keyFeatures(Arrays.asList(
        "key_features2"
    ))
    .materials(Arrays.asList(
        "materials7",
        "materials8",
        "materials9"
    ))
    .build();
```



