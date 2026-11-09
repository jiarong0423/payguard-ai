# Product Reference Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlByb2R1Y3RSZWZlcmVuY2VSZXNwb25zZQ

Up to three Channel3 products for the seller to pick from; advisory, never changes the AUP decision.


# Class Name

`ProductReferenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AffectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` |
| `Cards` | [`[]models.ProductCard`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/product-card.md) | Required | Cards.<br><br>**Constraints**: *Maximum Items*: `3` |
| `Reason` | [`models.ProductReferenceResponseReason`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/product-reference-response-reason.md) | Required | This is a container for any-of cases. |
| `RecordedAt` | [`models.ProductReferenceResponseRecordedAt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/product-reference-response-recorded-at.md) | Required | This is a container for any-of cases. |
| `Source` | [`models.ProductReferenceResponseSource`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/product-reference-response-source.md) | Required | This is a container for any-of cases. |
| `Status` | [`models.Status12Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/status-12.md) | Required | Status. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    productReferenceResponse := models.ProductReferenceResponse{
        AffectsDecision: "False",
        Cards:           []models.ProductCard{
            models.ProductCard{
                Brand:       models.ProductCardBrandContainer.FromString("String3"),
                Category:    models.ProductCardCategoryContainer.FromString("String7"),
                ImageUrl:    models.ProductCardImageUrlContainer.FromString("String5"),
                KeyFeatures: []string{
                    "key_features4",
                    "key_features5",
                    "key_features6",
                },
                Materials:   []string{
                    "materials9",
                    "materials0",
                },
                ProductId:   "product_id4",
                Title:       "title4",
            },
        },
        Reason:          models.ProductReferenceResponseReasonContainer.FromReason7(models.Reason7Enum_NOTHINGTOSEND),
        RecordedAt:      models.ProductReferenceResponseRecordedAtContainer.FromString("String9"),
        Source:          models.ProductReferenceResponseSourceContainer.FromSource11(models.Source11Enum_CHANNEL3LIVE),
        Status:          models.Status12Enum_NOTFOUND,
    }

}
```



