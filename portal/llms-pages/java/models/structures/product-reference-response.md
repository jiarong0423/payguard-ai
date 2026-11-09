# Product Reference Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlByb2R1Y3RSZWZlcmVuY2VSZXNwb25zZQ

Up to three Channel3 products for the seller to pick from; advisory, never changes the AUP decision.


# Class Name

`ProductReferenceResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AffectsDecision` | `String` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` | String getAffectsDecision() | setAffectsDecision(String affectsDecision) |
| `Cards` | [`List<ProductCard>`](http://localhost:3000/llms-pages/java/models/structures/product-card.md) | Required | Cards.<br><br>**Constraints**: *Maximum Items*: `3` | List<ProductCard> getCards() | setCards(List<ProductCard> cards) |
| `Reason` | [`ProductReferenceResponseReason`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/product-reference-response-reason.md) | Required | This is a container for any-of cases. | ProductReferenceResponseReason getReason() | setReason(ProductReferenceResponseReason reason) |
| `RecordedAt` | [`ProductReferenceResponseRecordedAt`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/product-reference-response-recorded-at.md) | Required | This is a container for any-of cases. | ProductReferenceResponseRecordedAt getRecordedAt() | setRecordedAt(ProductReferenceResponseRecordedAt recordedAt) |
| `Source` | [`ProductReferenceResponseSource`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/product-reference-response-source.md) | Required | This is a container for any-of cases. | ProductReferenceResponseSource getSource() | setSource(ProductReferenceResponseSource source) |
| `Status` | [`Status12Enum`](http://localhost:3000/llms-pages/java/models/enumerations/status-12.md) | Required | Status. | Status12Enum getStatus() | setStatus(Status12Enum status) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.ProductCard;
import m18000.m0.m0.m127.models.ProductReferenceResponse;
import m18000.m0.m0.m127.models.Reason7Enum;
import m18000.m0.m0.m127.models.Source11Enum;
import m18000.m0.m0.m127.models.Status12Enum;
import m18000.m0.m0.m127.models.containers.ProductCardBrand;
import m18000.m0.m0.m127.models.containers.ProductCardCategory;
import m18000.m0.m0.m127.models.containers.ProductCardImageUrl;
import m18000.m0.m0.m127.models.containers.ProductReferenceResponseReason;
import m18000.m0.m0.m127.models.containers.ProductReferenceResponseRecordedAt;
import m18000.m0.m0.m127.models.containers.ProductReferenceResponseSource;

ProductReferenceResponse productReferenceResponse = new ProductReferenceResponse.Builder(
    "False",
    Arrays.asList(
        new ProductCard.Builder(
            ProductCardBrand.fromString(
                "String3"
            ),
            ProductCardCategory.fromString(
                "String7"
            ),
            ProductCardImageUrl.fromString(
                "String5"
            ),
            Arrays.asList(
                "key_features4",
                "key_features5",
                "key_features6"
            ),
            Arrays.asList(
                "materials9",
                "materials0"
            ),
            "product_id4",
            "title4"
        )
        .build()
    ),
    ProductReferenceResponseReason.fromReason7(
        Reason7Enum.NOTHING_TO_SEND
    ),
    ProductReferenceResponseRecordedAt.fromString(
        "String9"
    ),
    ProductReferenceResponseSource.fromSource11(
        Source11Enum.CHANNEL3_LIVE
    ),
    Status12Enum.NOT_FOUND
)
.build();
```



