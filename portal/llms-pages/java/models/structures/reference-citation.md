# Reference Citation

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlJlZmVyZW5jZUNpdGF0aW9u

ReferenceCitation.


# Class Name

`ReferenceCitation`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CaseOutcome` | [`ReferenceCitationCaseOutcome`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/reference-citation-case-outcome.md) | Required | This is a container for any-of cases. | ReferenceCitationCaseOutcome getCaseOutcome() | setCaseOutcome(ReferenceCitationCaseOutcome caseOutcome) |
| `CaseStage` | [`CaseStageEnum`](http://localhost:3000/llms-pages/java/models/enumerations/case-stage.md) | Required | Case stage. | CaseStageEnum getCaseStage() | setCaseStage(CaseStageEnum caseStage) |
| `ChunkId` | `String` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` | String getChunkId() | setChunkId(String chunkId) |
| `DecisionAcceptanceDeadline` | [`ReferenceCitationDecisionAcceptanceDeadline`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/reference-citation-decision-acceptance-deadline.md) | Required | This is a container for any-of cases. | ReferenceCitationDecisionAcceptanceDeadline getDecisionAcceptanceDeadline() | setDecisionAcceptanceDeadline(ReferenceCitationDecisionAcceptanceDeadline decisionAcceptanceDeadline) |
| `DecisionDate` | [`ReferenceCitationDecisionDate`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/reference-citation-decision-date.md) | Required | This is a container for any-of cases. | ReferenceCitationDecisionDate getDecisionDate() | setDecisionDate(ReferenceCitationDecisionDate decisionDate) |
| `DecisionDateStatus` | [`DecisionDateStatusEnum`](http://localhost:3000/llms-pages/java/models/enumerations/decision-date-status.md) | Required | Decision date status. | DecisionDateStatusEnum getDecisionDateStatus() | setDecisionDateStatus(DecisionDateStatusEnum decisionDateStatus) |
| `EffectiveDate` | [`ReferenceCitationEffectiveDate`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/reference-citation-effective-date.md) | Required | This is a container for any-of cases. | ReferenceCitationEffectiveDate getEffectiveDate() | setEffectiveDate(ReferenceCitationEffectiveDate effectiveDate) |
| `EffectiveDateStatus` | [`EffectiveDateStatusEnum`](http://localhost:3000/llms-pages/java/models/enumerations/effective-date-status.md) | Required | Effective date status. | EffectiveDateStatusEnum getEffectiveDateStatus() | setEffectiveDateStatus(EffectiveDateStatusEnum effectiveDateStatus) |
| `Jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` | String getJurisdiction() | setJurisdiction(String jurisdiction) |
| `JurisdictionLabel` | `String` | Required | Jurisdiction label.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` | String getJurisdictionLabel() | setJurisdictionLabel(String jurisdictionLabel) |
| `Locator` | `String` | Required | Locator.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` | String getLocator() | setLocator(String locator) |
| `MaterialType` | [`MaterialType1Enum`](http://localhost:3000/llms-pages/java/models/enumerations/material-type-1.md) | Required | Material type. | MaterialType1Enum getMaterialType() | setMaterialType(MaterialType1Enum materialType) |
| `RelevanceScore` | `int` | Required | Relevance score.<br><br>**Constraints**: `>= 1`, `<= 128` | int getRelevanceScore() | setRelevanceScore(int relevanceScore) |
| `RetrievedAt` | `String` | Required | Retrieved at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` | String getRetrievedAt() | setRetrievedAt(String retrievedAt) |
| `SourceId` | `String` | Required | Source id.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128` | String getSourceId() | setSourceId(String sourceId) |
| `SourceTitle` | `String` | Required | Source title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` | String getSourceTitle() | setSourceTitle(String sourceTitle) |
| `SourceUpdatedDate` | [`ReferenceCitationSourceUpdatedDate`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/reference-citation-source-updated-date.md) | Required | This is a container for any-of cases. | ReferenceCitationSourceUpdatedDate getSourceUpdatedDate() | setSourceUpdatedDate(ReferenceCitationSourceUpdatedDate sourceUpdatedDate) |
| `SourceUpdatedDateStatus` | [`SourceUpdatedDateStatusEnum`](http://localhost:3000/llms-pages/java/models/enumerations/source-updated-date-status.md) | Required | Source updated date status. | SourceUpdatedDateStatusEnum getSourceUpdatedDateStatus() | setSourceUpdatedDateStatus(SourceUpdatedDateStatusEnum sourceUpdatedDateStatus) |
| `Text` | `String` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` | String getText() | setText(String text) |
| `TextSha256` | `String` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getTextSha256() | setTextSha256(String textSha256) |
| `Title` | `String` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` | String getTitle() | setTitle(String title) |
| `Url` | `String` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` | String getUrl() | setUrl(String url) |


# Example

```java
import m18000.m0.m0.m127.models.CaseOutcomeEnum;
import m18000.m0.m0.m127.models.CaseStageEnum;
import m18000.m0.m0.m127.models.DecisionDateStatusEnum;
import m18000.m0.m0.m127.models.EffectiveDateStatusEnum;
import m18000.m0.m0.m127.models.MaterialType1Enum;
import m18000.m0.m0.m127.models.ReferenceCitation;
import m18000.m0.m0.m127.models.SourceUpdatedDateStatusEnum;
import m18000.m0.m0.m127.models.containers.ReferenceCitationCaseOutcome;
import m18000.m0.m0.m127.models.containers.ReferenceCitationDecisionAcceptanceDeadline;
import m18000.m0.m0.m127.models.containers.ReferenceCitationDecisionDate;
import m18000.m0.m0.m127.models.containers.ReferenceCitationEffectiveDate;
import m18000.m0.m0.m127.models.containers.ReferenceCitationSourceUpdatedDate;

ReferenceCitation referenceCitation = new ReferenceCitation.Builder(
    ReferenceCitationCaseOutcome.fromCaseOutcome(
        CaseOutcomeEnum.SETTLEMENT_APPROVAL_NOT_FINAL_MERITS
    ),
    CaseStageEnum.PROCEDURAL_ORDER,
    "chunk_id0",
    ReferenceCitationDecisionAcceptanceDeadline.fromString(
        "String7"
    ),
    ReferenceCitationDecisionDate.fromString(
        "String1"
    ),
    DecisionDateStatusEnum.NOT_APPLICABLE,
    ReferenceCitationEffectiveDate.fromString(
        "String9"
    ),
    EffectiveDateStatusEnum.DOCUMENT_STATED,
    "US",
    "jurisdiction_label6",
    "locator0",
    MaterialType1Enum.OFFICIAL_API_REFERENCE,
    128,
    "retrieved_at2",
    "source_id2",
    "source_title4",
    ReferenceCitationSourceUpdatedDate.fromString(
        "String1"
    ),
    SourceUpdatedDateStatusEnum.DOCUMENT_STATED,
    "text8",
    "text_sha2566",
    "title4",
    "url2"
)
.build();
```



