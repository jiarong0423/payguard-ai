# Aup Acknowledge Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVxdWVzdA

AupAcknowledgeRequest.


# Class Name

`AupAcknowledgeRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Choice` | [`ChoiceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/choice.md) | Required | Choice. | ChoiceEnum getChoice() | setChoice(ChoiceEnum choice) |
| `DescriptionDigest` | `String` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getDescriptionDigest() | setDescriptionDigest(String descriptionDigest) |
| `EvaluationId` | `String` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` | String getEvaluationId() | setEvaluationId(String evaluationId) |


# Example

```java
import m18000.m0.m0.m127.models.AupAcknowledgeRequest;
import m18000.m0.m0.m127.models.ChoiceEnum;

AupAcknowledgeRequest aupAcknowledgeRequest = new AupAcknowledgeRequest.Builder(
    ChoiceEnum.ACKNOWLEDGE_AND_CONTINUE,
    "description_digest0",
    "evaluation_id6"
)
.build();
```



