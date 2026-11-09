# Product Confirm Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVzcG9uc2U

The seller's own choice: one of the cards they were shown, or none of them.


# Class Name

`ProductConfirmResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AffectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` |
| `Card` | [`ProductConfirmResponseCard`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/product-confirm-response-card.md) | Required | This is a container for any-of cases. |
| `CardDigest` | [`ProductConfirmResponseCardDigest`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/product-confirm-response-card-digest.md) | Required | This is a container for any-of cases. |
| `Choice` | [`Choice2Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/choice-2.md) | Required | Choice. |
| `ConfirmedBy` | `string` | Required, Constant | Confirmed by.<br><br>**Value**: `"seller"` |
| `DescriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `EvaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `RecordedAt` | [`ProductConfirmResponseRecordedAt`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/product-confirm-response-recorded-at.md) | Required | This is a container for any-of cases. |
| `Source` | [`Source10Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/source-10.md) | Required | Source. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

ProductConfirmResponse productConfirmResponse = new ProductConfirmResponse
{
    AffectsDecision = "False",
    Card = ProductConfirmResponseCard.FromProductCard(
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
    ),
    CardDigest = ProductConfirmResponseCardDigest.FromString("String1"),
    Choice = Choice2Enum.CONFIRMED,
    ConfirmedBy = "seller",
    DescriptionDigest = "description_digest2",
    EvaluationId = "evaluation_id8",
    RecordedAt = ProductConfirmResponseRecordedAt.FromString("String1"),
    Source = Source10Enum.Channel3Live,
};
```



