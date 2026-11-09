# Product Confirm Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVzcG9uc2U

The seller's own choice: one of the cards they were shown, or none of them.


# Class Name

`ProductConfirmResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AffectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` |
| `Card` | [`models.ProductConfirmResponseCard`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/product-confirm-response-card.md) | Required | This is a container for any-of cases. |
| `CardDigest` | [`models.ProductConfirmResponseCardDigest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/product-confirm-response-card-digest.md) | Required | This is a container for any-of cases. |
| `Choice` | [`models.Choice2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/choice-2.md) | Required | Choice. |
| `ConfirmedBy` | `string` | Required, Constant | Confirmed by.<br><br>**Value**: `"seller"` |
| `DescriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `EvaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `RecordedAt` | [`models.ProductConfirmResponseRecordedAt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/product-confirm-response-recorded-at.md) | Required | This is a container for any-of cases. |
| `Source` | [`models.Source10Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/source-10.md) | Required | Source. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    productConfirmResponse := models.ProductConfirmResponse{
        AffectsDecision:   "False",
        Card:              models.ProductConfirmResponseCardContainer.FromProductCard(models.ProductCard{
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
        }),
        CardDigest:        models.ProductConfirmResponseCardDigestContainer.FromString("String1"),
        Choice:            models.Choice2Enum_CONFIRMED,
        ConfirmedBy:       "seller",
        DescriptionDigest: "description_digest2",
        EvaluationId:      "evaluation_id8",
        RecordedAt:        models.ProductConfirmResponseRecordedAtContainer.FromString("String1"),
        Source:            models.Source10Enum_CHANNEL3LIVE,
    }

}
```



