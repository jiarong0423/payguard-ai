# Product Reference Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlByb2R1Y3RSZWZlcmVuY2VSZXF1ZXN0

ProductReferenceRequest.


# Class Name

`ProductReferenceRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Description` | `String` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` | String getDescription() | setDescription(String description) |
| `EvaluationId` | `String` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` | String getEvaluationId() | setEvaluationId(String evaluationId) |


# Example

```java
import m18000.m0.m0.m127.models.ProductReferenceRequest;

ProductReferenceRequest productReferenceRequest = new ProductReferenceRequest.Builder(
    "description8",
    "evaluation_id2"
)
.build();
```



