# Product Confirm Response Card

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVzcG9uc2VDYXJk


# Class Name

`ProductConfirmResponseCard`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.ProductCard`](http://localhost:3000/llms-pages/go/models/structures/product-card.md) | models.ProductConfirmResponseCardContainer.FromProductCard(models.ProductCard productCard) |


# models.ProductCard

## Initialization Code

### Example

```go
value := models.ProductConfirmResponseCardContainer.FromProductCard(models.ProductCard{
    Brand:       models.ProductCardBrandContainer.FromString("String9"),
    Category:    models.ProductCardCategoryContainer.FromString("String3"),
    ImageUrl:    models.ProductCardImageUrlContainer.FromString("String1"),
    KeyFeatures: []string{
        "key_features0",
        "key_features1",
        "key_features2",
    },
    Materials:   []string{
        "materials5",
        "materials6",
    },
    ProductId:   "product_id0",
    Title:       "title0",
})
```



