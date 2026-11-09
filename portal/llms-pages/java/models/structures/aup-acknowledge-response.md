# Aup Acknowledge Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVzcG9uc2U

AupAcknowledgeResponse.


# Class Name

`AupAcknowledgeResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AcknowledgementToken` | [`AupAcknowledgeResponseAcknowledgementToken`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/aup-acknowledge-response-acknowledgement-token.md) | Required | This is a container for any-of cases. | AupAcknowledgeResponseAcknowledgementToken getAcknowledgementToken() | setAcknowledgementToken(AupAcknowledgeResponseAcknowledgementToken acknowledgementToken) |
| `Choice` | [`ChoiceEnum`](http://localhost:3000/llms-pages/java/models/enumerations/choice.md) | Required | Choice. | ChoiceEnum getChoice() | setChoice(ChoiceEnum choice) |
| `ComplianceDecision` | `String` | Required, Constant | Compliance decision.<br><br>**Value**: `"NOT_MADE"` | String getComplianceDecision() | setComplianceDecision(String complianceDecision) |
| `DescriptionDigest` | `String` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getDescriptionDigest() | setDescriptionDigest(String descriptionDigest) |
| `EvaluationId` | `String` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` | String getEvaluationId() | setEvaluationId(String evaluationId) |
| `ExpiresAt` | [`AupAcknowledgeResponseExpiresAt`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/aup-acknowledge-response-expires-at.md) | Required | This is a container for any-of cases. | AupAcknowledgeResponseExpiresAt getExpiresAt() | setExpiresAt(AupAcknowledgeResponseExpiresAt expiresAt) |
| `ExternalActionAuthorized` | `String` | Required, Constant | External action authorized.<br><br>**Value**: `"False"` | String getExternalActionAuthorized() | setExternalActionAuthorized(String externalActionAuthorized) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` | String getSource() | setSource(String source) |
| `WarningCopyVersion` | `String` | Required, Constant | Warning copy version.<br><br>**Value**: `"aup-warning-v1"` | String getWarningCopyVersion() | setWarningCopyVersion(String warningCopyVersion) |


# Example

```java
import m18000.m0.m0.m127.models.AupAcknowledgeResponse;
import m18000.m0.m0.m127.models.ChoiceEnum;
import m18000.m0.m0.m127.models.containers.AupAcknowledgeResponseAcknowledgementToken;
import m18000.m0.m0.m127.models.containers.AupAcknowledgeResponseExpiresAt;

AupAcknowledgeResponse aupAcknowledgeResponse = new AupAcknowledgeResponse.Builder(
    AupAcknowledgeResponseAcknowledgementToken.fromString(
        "String9"
    ),
    ChoiceEnum.ACKNOWLEDGE_AND_CONTINUE,
    "NOT_MADE",
    "description_digest6",
    "evaluation_id2",
    AupAcknowledgeResponseExpiresAt.fromString(
        "String9"
    ),
    "False",
    "synthetic",
    "aup-warning-v1"
)
.build();
```



