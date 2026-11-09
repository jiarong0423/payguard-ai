# Product Confirm Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVzcG9uc2U

The seller's own choice: one of the cards they were shown, or none of them.


# Class Name

`ProductConfirmResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AffectsDecision` | `String` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` | String getAffectsDecision() | setAffectsDecision(String affectsDecision) |
| `Card` | [`ProductConfirmResponseCard`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/product-confirm-response-card.md) | Required | This is a container for any-of cases. | ProductConfirmResponseCard getCard() | setCard(ProductConfirmResponseCard card) |
| `CardDigest` | [`ProductConfirmResponseCardDigest`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/product-confirm-response-card-digest.md) | Required | This is a container for any-of cases. | ProductConfirmResponseCardDigest getCardDigest() | setCardDigest(ProductConfirmResponseCardDigest cardDigest) |
| `Choice` | [`Choice2Enum`](http://localhost:3000/llms-pages/java/models/enumerations/choice-2.md) | Required | Choice. | Choice2Enum getChoice() | setChoice(Choice2Enum choice) |
| `ConfirmedBy` | `String` | Required, Constant | Confirmed by.<br><br>**Value**: `"seller"` | String getConfirmedBy() | setConfirmedBy(String confirmedBy) |
| `DescriptionDigest` | `String` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getDescriptionDigest() | setDescriptionDigest(String descriptionDigest) |
| `EvaluationId` | `String` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` | String getEvaluationId() | setEvaluationId(String evaluationId) |
| `RecordedAt` | [`ProductConfirmResponseRecordedAt`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/product-confirm-response-recorded-at.md) | Required | This is a container for any-of cases. | ProductConfirmResponseRecordedAt getRecordedAt() | setRecordedAt(ProductConfirmResponseRecordedAt recordedAt) |
| `Source` | [`Source10Enum`](http://localhost:3000/llms-pages/java/models/enumerations/source-10.md) | Required | Source. | Source10Enum getSource() | setSource(Source10Enum source) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.Choice2Enum;
import m18000.m0.m0.m127.models.ProductCard;
import m18000.m0.m0.m127.models.ProductConfirmResponse;
import m18000.m0.m0.m127.models.Source10Enum;
import m18000.m0.m0.m127.models.containers.ProductCardBrand;
import m18000.m0.m0.m127.models.containers.ProductCardCategory;
import m18000.m0.m0.m127.models.containers.ProductCardImageUrl;
import m18000.m0.m0.m127.models.containers.ProductConfirmResponseCard;
import m18000.m0.m0.m127.models.containers.ProductConfirmResponseCardDigest;
import m18000.m0.m0.m127.models.containers.ProductConfirmResponseRecordedAt;

ProductConfirmResponse productConfirmResponse = new ProductConfirmResponse.Builder(
    "False",
    ProductConfirmResponseCard.fromProductCard(
        new ProductCard.Builder(
            ProductCardBrand.fromString(
                "String9"
            ),
            ProductCardCategory.fromString(
                "String3"
            ),
            ProductCardImageUrl.fromString(
                "String1"
            ),
            Arrays.asList(
                "key_features0",
                "key_features1",
                "key_features2"
            ),
            Arrays.asList(
                "materials5",
                "materials6"
            ),
            "product_id0",
            "title0"
        )
        .build()
    ),
    ProductConfirmResponseCardDigest.fromString(
        "String1"
    ),
    Choice2Enum.CONFIRMED,
    "seller",
    "description_digest2",
    "evaluation_id8",
    ProductConfirmResponseRecordedAt.fromString(
        "String1"
    ),
    Source10Enum.CHANNEL3_LIVE
)
.build();
```



