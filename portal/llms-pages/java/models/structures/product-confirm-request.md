# Product Confirm Request

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVxdWVzdA

ProductConfirmRequest.


# Class Name

`ProductConfirmRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Description` | `String` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` | String getDescription() | setDescription(String description) |
| `EvaluationId` | `String` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` | String getEvaluationId() | setEvaluationId(String evaluationId) |
| `ProductId` | [`ProductConfirmRequestProductId`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/product-confirm-request-product-id.md) | Required | This is a container for any-of cases. | ProductConfirmRequestProductId getProductId() | setProductId(ProductConfirmRequestProductId productId) |


# Example

```java
import m18000.m0.m0.m127.models.ProductConfirmRequest;
import m18000.m0.m0.m127.models.containers.ProductConfirmRequestProductId;

ProductConfirmRequest productConfirmRequest = new ProductConfirmRequest.Builder(
    "description6",
    "evaluation_id8",
    ProductConfirmRequestProductId.fromString(
        "String1"
    )
)
.build();
```



