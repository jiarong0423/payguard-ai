# Card

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkNhcmQ

Card.


# Class Name

`Card`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Brand` | [`*models.CardBrand`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/card-brand.md) | Optional | This is a container for any-of cases. |
| `Category` | [`*models.CardCategory`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/card-category.md) | Optional | This is a container for any-of cases. |
| `ImageUrl` | [`*models.CardImageUrl`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/card-image-url.md) | Optional | This is a container for any-of cases. |
| `KeyFeatures` | `[]string` | Optional | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `Materials` | `[]string` | Optional | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `ProductId` | `*string` | Optional | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `Title` | `*string` | Optional | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    card := models.Card{
        Brand:                models.ToPointer(models.CardBrandContainer.FromString("String1")),
        Category:             models.ToPointer(models.CardCategoryContainer.FromString("String5")),
        ImageUrl:             models.ToPointer(models.CardImageUrlContainer.FromString("String3")),
        KeyFeatures:          []string{
            "key_features2",
        },
        Materials:            []string{
            "materials7",
            "materials8",
            "materials9",
        },
    }

}
```



