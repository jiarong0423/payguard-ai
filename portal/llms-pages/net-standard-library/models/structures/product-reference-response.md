# Product Reference Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlByb2R1Y3RSZWZlcmVuY2VSZXNwb25zZQ

Up to three Channel3 products for the seller to pick from; advisory, never changes the AUP decision.


# Class Name

`ProductReferenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AffectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` |
| `Cards` | [`List<ProductCard>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/product-card.md) | Required | Cards.<br><br>**Constraints**: *Maximum Items*: `3` |
| `Reason` | [`ProductReferenceResponseReason`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/product-reference-response-reason.md) | Required | This is a container for any-of cases. |
| `RecordedAt` | [`ProductReferenceResponseRecordedAt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/product-reference-response-recorded-at.md) | Required | This is a container for any-of cases. |
| `Source` | [`ProductReferenceResponseSource`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/product-reference-response-source.md) | Required | This is a container for any-of cases. |
| `Status` | [`Status12Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/status-12.md) | Required | Status. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

ProductReferenceResponse productReferenceResponse = new ProductReferenceResponse
{
    AffectsDecision = "False",
    Cards = new List<ProductCard>
    {
        new ProductCard
        {
            Brand = ProductCardBrand.FromString("String3"),
            Category = ProductCardCategory.FromString("String7"),
            ImageUrl = ProductCardImageUrl.FromString("String5"),
            KeyFeatures = new List<string>
            {
                "key_features4",
                "key_features5",
                "key_features6",
            },
            Materials = new List<string>
            {
                "materials9",
                "materials0",
            },
            ProductId = "product_id4",
            Title = "title4",
        },
    },
    Reason = ProductReferenceResponseReason.FromReason7(Reason7Enum.NothingToSend),
    RecordedAt = ProductReferenceResponseRecordedAt.FromString("String9"),
    Source = ProductReferenceResponseSource.FromSource11(Source11Enum.Channel3Live),
    Status = Status12Enum.NOTFOUND,
};
```



