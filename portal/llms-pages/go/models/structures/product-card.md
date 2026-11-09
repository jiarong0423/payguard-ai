# Product Card

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlByb2R1Y3RDYXJk

A Channel3 catalogue product reduced to what identifies the item; no prices, offers or buy links.


# Class Name

`ProductCard`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Brand` | [`models.ProductCardBrand`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/product-card-brand.md) | Required | This is a container for any-of cases. |
| `Category` | [`models.ProductCardCategory`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/product-card-category.md) | Required | This is a container for any-of cases. |
| `ImageUrl` | [`models.ProductCardImageUrl`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/product-card-image-url.md) | Required | This is a container for any-of cases. |
| `KeyFeatures` | `[]string` | Required | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `Materials` | `[]string` | Required | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `ProductId` | `string` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `Title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    productCard := models.ProductCard{
        Brand:       models.ProductCardBrandContainer.FromString("String9"),
        Category:    models.ProductCardCategoryContainer.FromString("String3"),
        ImageUrl:    models.ProductCardImageUrlContainer.FromString("String1"),
        KeyFeatures: []string{
            "key_features0",
            "key_features1",
        },
        Materials:   []string{
            "materials5",
        },
        ProductId:   "product_id0",
        Title:       "title0",
    }

}
```



