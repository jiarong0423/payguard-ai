# Aup Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkF1cFJlc3BvbnNl

AupResponse.


# Class Name

`AupResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AdvisoryOnly` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` | String getAdvisoryOnly() | setAdvisoryOnly(String advisoryOnly) |
| `ComplianceDecision` | `String` | Required, Constant | Compliance decision.<br><br>**Value**: `"NOT_MADE"` | String getComplianceDecision() | setComplianceDecision(String complianceDecision) |
| `CurrentPolicyApplicability` | `String` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` | String getCurrentPolicyApplicability() | setCurrentPolicyApplicability(String currentPolicyApplicability) |
| `DescriptionDigest` | `String` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getDescriptionDigest() | setDescriptionDigest(String descriptionDigest) |
| `EvaluatedAt` | `String` | Required | Evaluated at. | String getEvaluatedAt() | setEvaluatedAt(String evaluatedAt) |
| `EvaluationId` | `String` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` | String getEvaluationId() | setEvaluationId(String evaluationId) |
| `ExpiresAt` | `String` | Required | Expires at. | String getExpiresAt() | setExpiresAt(String expiresAt) |
| `Findings` | [`List<Finding>`](http://localhost:3000/llms-pages/java/models/structures/finding.md) | Required | Findings. | List<Finding> getFindings() | setFindings(List<Finding> findings) |
| `MatchStatus` | [`MatchStatusEnum`](http://localhost:3000/llms-pages/java/models/enumerations/match-status.md) | Required | Match status. | MatchStatusEnum getMatchStatus() | setMatchStatus(MatchStatusEnum matchStatus) |
| `PolicyUrl` | `String` | Required, Constant | Policy url.<br><br>**Value**: `"https://www.paypal.com/us/legalhub/paypal/acceptableuse-full"` | String getPolicyUrl() | setPolicyUrl(String policyUrl) |
| `PolicyVersion` | `String` | Required | Policy version.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128` | String getPolicyVersion() | setPolicyVersion(String policyVersion) |
| `Recommendation` | `String` | Required | Recommendation.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1000` | String getRecommendation() | setRecommendation(String recommendation) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` | String getSource() | setSource(String source) |
| `WarningCopyVersion` | `String` | Required, Constant | Warning copy version.<br><br>**Value**: `"aup-warning-v1"` | String getWarningCopyVersion() | setWarningCopyVersion(String warningCopyVersion) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.AupResponse;
import m18000.m0.m0.m127.models.CategoryEnum;
import m18000.m0.m0.m127.models.Finding;
import m18000.m0.m0.m127.models.MatchStatusEnum;

AupResponse aupResponse = new AupResponse.Builder(
    "True",
    "NOT_MADE",
    "NOT_ESTABLISHED",
    "description_digest8",
    "evaluated_at4",
    "evaluation_id4",
    "expires_at4",
    Arrays.asList(
        new Finding.Builder(
            CategoryEnum.WEAPONS,
            "keyword_requires_policy_review"
        )
        .build()
    ),
    MatchStatusEnum.NO_MATCH,
    "https://www.paypal.com/us/legalhub/paypal/acceptableuse-full",
    "policy_version8",
    "recommendation6",
    "synthetic",
    "aup-warning-v1"
)
.build();
```



