# Product Card

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlByb2R1Y3RDYXJk

A Channel3 catalogue product reduced to what identifies the item; no prices, offers or buy links.


# Class Name

`ProductCard`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Brand` | [`ProductCardBrand`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/product-card-brand.md) | Required | This is a container for any-of cases. |
| `Category` | [`ProductCardCategory`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/product-card-category.md) | Required | This is a container for any-of cases. |
| `ImageUrl` | [`ProductCardImageUrl`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/product-card-image-url.md) | Required | This is a container for any-of cases. |
| `KeyFeatures` | `List<string>` | Required | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `Materials` | `List<string>` | Required | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `ProductId` | `string` | Required | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `Title` | `string` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

ProductCard productCard = new ProductCard
{
    Brand = ProductCardBrand.FromString("String9"),
    Category = ProductCardCategory.FromString("String3"),
    ImageUrl = ProductCardImageUrl.FromString("String1"),
    KeyFeatures = new List<string>
    {
        "key_features0",
        "key_features1",
    },
    Materials = new List<string>
    {
        "materials5",
    },
    ProductId = "product_id0",
    Title = "title0",
};
```



