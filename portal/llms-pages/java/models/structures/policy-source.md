# Policy Source

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlBvbGljeVNvdXJjZQ

PolicySource.


# Class Name

`PolicySource`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CitationChunkIds` | `List<String>` | Required | Citation chunk ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `29`, *Pattern*: `^[A-Z0-9-]{1,128}$` | List<String> getCitationChunkIds() | setCitationChunkIds(List<String> citationChunkIds) |
| `ContentClass` | `String` | Required, Constant | Content class.<br><br>**Value**: `"public_reference_summary"` | String getContentClass() | setContentClass(String contentClass) |
| `CurrentPolicyApplicability` | `String` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` | String getCurrentPolicyApplicability() | setCurrentPolicyApplicability(String currentPolicyApplicability) |
| `DecisionAcceptanceDeadline` | [`PolicySourceDecisionAcceptanceDeadline`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/policy-source-decision-acceptance-deadline.md) | Required | This is a container for any-of cases. | PolicySourceDecisionAcceptanceDeadline getDecisionAcceptanceDeadline() | setDecisionAcceptanceDeadline(PolicySourceDecisionAcceptanceDeadline decisionAcceptanceDeadline) |
| `DecisionDate` | [`PolicySourceDecisionDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/policy-source-decision-date.md) | Required | This is a container for any-of cases. | PolicySourceDecisionDate getDecisionDate() | setDecisionDate(PolicySourceDecisionDate decisionDate) |
| `DecisionDateStatus` | [`DecisionDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/decision-date-status.md) | Required | Decision date status. | DecisionDateStatusEnum getDecisionDateStatus() | setDecisionDateStatus(DecisionDateStatusEnum decisionDateStatus) |
| `EffectiveDate` | [`PolicySourceEffectiveDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/policy-source-effective-date.md) | Required | This is a container for any-of cases. | PolicySourceEffectiveDate getEffectiveDate() | setEffectiveDate(PolicySourceEffectiveDate effectiveDate) |
| `EffectiveDateStatus` | [`EffectiveDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/effective-date-status.md) | Required | Effective date status. | EffectiveDateStatusEnum getEffectiveDateStatus() | setEffectiveDateStatus(EffectiveDateStatusEnum effectiveDateStatus) |
| `Jurisdiction` | `String` | Required | Jurisdiction.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` | String getJurisdiction() | setJurisdiction(String jurisdiction) |
| `JurisdictionNormalized` | `String` | Required, Constant | Jurisdiction normalized.<br><br>**Value**: `"US"` | String getJurisdictionNormalized() | setJurisdictionNormalized(String jurisdictionNormalized) |
| `MaterialType` | [`MaterialType1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/material-type-1.md) | Required | Material type. | MaterialType1Enum getMaterialType() | setMaterialType(MaterialType1Enum materialType) |
| `ObservationAgeBasis` | `String` | Required, Constant | Observation age basis.<br><br>**Value**: `"saved_retrieved_at_exact_elapsed_time"` | String getObservationAgeBasis() | setObservationAgeBasis(String observationAgeBasis) |
| `ObservationStatus` | [`ObservationStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/observation-status.md) | Required | Observation status. | ObservationStatusEnum getObservationStatus() | setObservationStatus(ObservationStatusEnum observationStatus) |
| `ReasonCodes` | [`List<ReasonCode1Enum>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` | List<ReasonCode1Enum> getReasonCodes() | setReasonCodes(List<ReasonCode1Enum> reasonCodes) |
| `Representation` | `String` | Required, Constant | Representation.<br><br>**Value**: `"authored_paraphrase_not_full_source"` | String getRepresentation() | setRepresentation(String representation) |
| `RetrievedAt` | `String` | Required | Retrieved at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` | String getRetrievedAt() | setRetrievedAt(String retrievedAt) |
| `SourceId` | `String` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` | String getSourceId() | setSourceId(String sourceId) |
| `SourceUpdatedDate` | [`PolicySourceSourceUpdatedDate`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/policy-source-source-updated-date.md) | Required | This is a container for any-of cases. | PolicySourceSourceUpdatedDate getSourceUpdatedDate() | setSourceUpdatedDate(PolicySourceSourceUpdatedDate sourceUpdatedDate) |
| `SourceUpdatedDateStatus` | [`SourceUpdatedDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/source-updated-date-status.md) | Required | Source updated date status. | SourceUpdatedDateStatusEnum getSourceUpdatedDateStatus() | setSourceUpdatedDateStatus(SourceUpdatedDateStatusEnum sourceUpdatedDateStatus) |
| `Title` | `String` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` | String getTitle() | setTitle(String title) |
| `Url` | `String` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` | String getUrl() | setUrl(String url) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.DecisionDateStatusEnum;
import m18000.m0.m0.m127.models.EffectiveDateStatusEnum;
import m18000.m0.m0.m127.models.MaterialType1Enum;
import m18000.m0.m0.m127.models.ObservationStatusEnum;
import m18000.m0.m0.m127.models.PolicySource;
import m18000.m0.m0.m127.models.ReasonCode1Enum;
import m18000.m0.m0.m127.models.SourceUpdatedDateStatusEnum;
import m18000.m0.m0.m127.models.containers.PolicySourceDecisionAcceptanceDeadline;
import m18000.m0.m0.m127.models.containers.PolicySourceDecisionDate;
import m18000.m0.m0.m127.models.containers.PolicySourceEffectiveDate;
import m18000.m0.m0.m127.models.containers.PolicySourceSourceUpdatedDate;

PolicySource policySource = new PolicySource.Builder(
    Arrays.asList(
        "citation_chunk_ids4"
    ),
    "public_reference_summary",
    "NOT_ESTABLISHED",
    PolicySourceDecisionAcceptanceDeadline.fromString(
        "String7"
    ),
    PolicySourceDecisionDate.fromString(
        "String1"
    ),
    DecisionDateStatusEnum.NOT_APPLICABLE,
    PolicySourceEffectiveDate.fromString(
        "String3"
    ),
    EffectiveDateStatusEnum.DOCUMENT_STATED,
    "jurisdiction2",
    "US",
    MaterialType1Enum.OFFICIAL_API_REFERENCE,
    "saved_retrieved_at_exact_elapsed_time",
    ObservationStatusEnum.STALE_OBSERVATION,
    Arrays.asList(
        ReasonCode1Enum.STALE_OBSERVATION
    ),
    "authored_paraphrase_not_full_source",
    "retrieved_at2",
    "source_id2",
    PolicySourceSourceUpdatedDate.fromString(
        "String1"
    ),
    SourceUpdatedDateStatusEnum.DOCUMENT_STATED,
    "title6",
    "url2"
)
.build();
```



