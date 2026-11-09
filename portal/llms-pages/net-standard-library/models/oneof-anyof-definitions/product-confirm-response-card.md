# Product Confirm Response Card

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVzcG9uc2VDYXJk


# Class Name

`ProductConfirmResponseCard`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`ProductCard`](http://localhost:3000/llms-pages/net-standard-library/models/structures/product-card.md) | ProductConfirmResponseCard.FromProductCard(ProductCard productCard) |


# ProductCard

## Initialization Code

### Example

```csharp
ProductConfirmResponseCard value = ProductConfirmResponseCard.FromProductCard(
    new ProductCard
    {
        Brand = ProductCardBrand.FromString("String9"),
        Category = ProductCardCategory.FromString("String3"),
        ImageUrl = ProductCardImageUrl.FromString("String1"),
        KeyFeatures = new List<string>
        {
            "key_features0",
            "key_features1",
            "key_features2",
        },
        Materials = new List<string>
        {
            "materials5",
            "materials6",
        },
        ProductId = "product_id0",
        Title = "title0",
    }
);
```



