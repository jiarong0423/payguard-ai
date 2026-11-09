# Product Confirm Response Card

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVzcG9uc2VDYXJk


# Class Name

`ProductConfirmResponseCard`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`ProductCard`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/product-card.md) | ProductConfirmResponseCard.fromProductCard(ProductCard productCard) |


# ProductCard

## Initialization Code

### Example

```java
ProductConfirmResponseCard.fromProductCard(
        new ProductCard.Builder(
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
                "key_features1",
                "key_features2"
            ),
            Arrays.asList(
                "materials5",
                "materials6"
            ),
            "product_id0",
            "title0"
        )
        .build()
    )
```



