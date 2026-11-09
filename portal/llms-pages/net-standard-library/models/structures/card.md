# Card

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkNhcmQ

Card.


# Class Name

`Card`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Brand` | [`CardBrand`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/card-brand.md) | Optional | This is a container for any-of cases. |
| `Category` | [`CardCategory`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/card-category.md) | Optional | This is a container for any-of cases. |
| `ImageUrl` | [`CardImageUrl`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/card-image-url.md) | Optional | This is a container for any-of cases. |
| `KeyFeatures` | `List<string>` | Optional | Key features.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `100`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `Materials` | `List<string>` | Optional | Materials.<br><br>**Constraints**: *Maximum Items*: `4`, *Minimum Length*: `2`, *Maximum Length*: `40`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |
| `ProductId` | `string` | Optional | Product id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9_.:-]{1,64}$` |
| `Title` | `string` | Optional | Title.<br><br>**Constraints**: *Minimum Length*: `2`, *Maximum Length*: `120`, *Pattern*: `^[A-Za-z0-9 &'\-,./+()%\"]+$` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

Card card = new Card
{
    Brand = CardBrand.FromString("String1"),
    Category = CardCategory.FromString("String5"),
    ImageUrl = CardImageUrl.FromString("String3"),
    KeyFeatures = new List<string>
    {
        "key_features2",
    },
    Materials = new List<string>
    {
        "materials7",
        "materials8",
        "materials9",
    },
};
```



