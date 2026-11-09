# Product Card

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlByb2R1Y3RDYXJk

A Channel3 catalogue product reduced to what identifies the item; no prices, offers or buy links.


# Class Name

`ProductCard`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Brand` | [`ProductCardBrand`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/product-card-brand.md) | Required | This is a container for any-of cases. | ProductCardBrand getBrand() | setBrand(ProductCardBrand brand) |
| `Category` | [`ProductCardCategory`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/product-card-category.md) | Required | This is a container for any-of cases. | ProductCardCategory getCategory() | setCategory(ProductCardCategory category) |
| `ImageUrl` | [`ProductCardImageUrl`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/product-card-image-url.md) | Required | This is a container for any-of cases. | ProductCardImageUrl getImageUrl() | setImageUrl(ProductCardImageUrl imageUrl) |
| `KeyFeatures` | `List<String>` | Required | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | List<String> getKeyFeatures() | setKeyFeatures(List<String> keyFeatures) |
| `Materials` | `List<String>` | Required | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | List<String> getMaterials() | setMaterials(List<String> materials) |
| `ProductId` | `String` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` | String getProductId() | setProductId(String productId) |
| `Title` | `String` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` | String getTitle() | setTitle(String title) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.ProductCard;
import m18000.m0.m0.m127.models.containers.ProductCardBrand;
import m18000.m0.m0.m127.models.containers.ProductCardCategory;
import m18000.m0.m0.m127.models.containers.ProductCardImageUrl;

ProductCard productCard = new ProductCard.Builder(
    ProductCardBrand.fromString(
        "String9"
    ),
    ProductCardCategory.fromString(
        "String3"
    ),
    ProductCardImageUrl.fromString(
        "String1"
    ),
    Arrays.asList(
        "key_features0",
        "key_features1"
    ),
    Arrays.asList(
        "materials5"
    ),
    "product_id0",
    "title0"
)
.build();
```



