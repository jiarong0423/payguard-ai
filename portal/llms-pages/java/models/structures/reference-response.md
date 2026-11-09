# Reference Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlc3BvbnNl

ReferenceResponse.


# Class Name

`ReferenceResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AdvisoryOnly` | `boolean` | Required | Advisory only. | boolean getAdvisoryOnly() | setAdvisoryOnly(boolean advisoryOnly) |
| `CorpusDigest` | `String` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getCorpusDigest() | setCorpusDigest(String corpusDigest) |
| `CorpusDigests` | [`ReferenceDigests`](http://localhost:3000/llms-pages/java/models/structures/reference-digests.md) | Required | ReferenceDigests. | ReferenceDigests getCorpusDigests() | setCorpusDigests(ReferenceDigests corpusDigests) |
| `CorpusId` | `String` | Required, Constant | Corpus id.<br><br>**Value**: `"payguard-us-official-references-v2"` | String getCorpusId() | setCorpusId(String corpusId) |
| `FiltersApplied` | [`ReferenceFilters`](http://localhost:3000/llms-pages/java/models/structures/reference-filters.md) | Required | ReferenceFilters. | ReferenceFilters getFiltersApplied() | setFiltersApplied(ReferenceFilters filtersApplied) |
| `Limitations` | `List<String>` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` | List<String> getLimitations() | setLimitations(List<String> limitations) |
| `OperationalAuthority` | `String` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` | String getOperationalAuthority() | setOperationalAuthority(String operationalAuthority) |
| `Results` | [`List<ReferenceCitation>`](http://localhost:3000/llms-pages/java/models/structures/reference-citation.md) | Required | Results.<br><br>**Constraints**: *Maximum Items*: `10` | List<ReferenceCitation> getResults() | setResults(List<ReferenceCitation> results) |
| `SchemaVersion` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` | int getSchemaVersion() | setSchemaVersion(int schemaVersion) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"public_reference"` | String getSource() | setSource(String source) |
| `Status` | [`Status13Enum`](http://localhost:3000/llms-pages/java/models/enumerations/status-13.md) | Required | Status. | Status13Enum getStatus() | setStatus(Status13Enum status) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.CaseOutcomeEnum;
import m18000.m0.m0.m127.models.CaseStage2Enum;
import m18000.m0.m0.m127.models.CaseStageEnum;
import m18000.m0.m0.m127.models.DecisionDateStatusEnum;
import m18000.m0.m0.m127.models.EffectiveDateStatusEnum;
import m18000.m0.m0.m127.models.MaterialType1Enum;
import m18000.m0.m0.m127.models.MaterialType4Enum;
import m18000.m0.m0.m127.models.ReferenceCitation;
import m18000.m0.m0.m127.models.ReferenceDigests;
import m18000.m0.m0.m127.models.ReferenceFilters;
import m18000.m0.m0.m127.models.ReferenceResponse;
import m18000.m0.m0.m127.models.SourceUpdatedDateStatusEnum;
import m18000.m0.m0.m127.models.Status13Enum;
import m18000.m0.m0.m127.models.ThemeEnum;
import m18000.m0.m0.m127.models.containers.ReferenceCitationCaseOutcome;
import m18000.m0.m0.m127.models.containers.ReferenceCitationDecisionAcceptanceDeadline;
import m18000.m0.m0.m127.models.containers.ReferenceCitationDecisionDate;
import m18000.m0.m0.m127.models.containers.ReferenceCitationEffectiveDate;
import m18000.m0.m0.m127.models.containers.ReferenceCitationSourceUpdatedDate;
import m18000.m0.m0.m127.models.containers.ReferenceFiltersAsOf;
import m18000.m0.m0.m127.models.containers.ReferenceFiltersMaxSourceAgeDays;

ReferenceResponse referenceResponse = new ReferenceResponse.Builder(
    false,
    "corpus_digest2",
    new ReferenceDigests.Builder(
        "chunks_sha2564",
        "sources_sha2562"
    )
    .build(),
    "payguard-us-official-references-v2",
    new ReferenceFilters.Builder(
        "source_updated_date_utc_calendar",
        ReferenceFiltersAsOf.fromString(
            "String1"
        ),
        CaseStage2Enum.PROCEDURAL_ORDER,
        "US",
        10,
        Arrays.asList(
            MaterialType4Enum.OFFICIAL_POLICY,
            MaterialType4Enum.PUBLIC_COURT_ORDER_COPY
        ),
        ReferenceFiltersMaxSourceAgeDays.fromNumber(
            28
        ),
        false,
        ThemeEnum.DISPUTE_MEDIATION
    )
    .build(),
    Arrays.asList(
        "limitations5",
        "limitations6"
    ),
    "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
    Arrays.asList(
        new ReferenceCitation.Builder(
            ReferenceCitationCaseOutcome.fromCaseOutcome(
                CaseOutcomeEnum.SETTLEMENT_APPROVAL_NOT_FINAL_MERITS
            ),
            CaseStageEnum.PROCEDURAL_ORDER,
            "chunk_id2",
            ReferenceCitationDecisionAcceptanceDeadline.fromString(
                "String5"
            ),
            ReferenceCitationDecisionDate.fromString(
                "String9"
            ),
            DecisionDateStatusEnum.NOT_APPLICABLE,
            ReferenceCitationEffectiveDate.fromString(
                "String5"
            ),
            EffectiveDateStatusEnum.DOCUMENT_STATED,
            "US",
            "jurisdiction_label4",
            "locator8",
            MaterialType1Enum.OFFICIAL_API_REFERENCE,
            128,
            "retrieved_at0",
            "source_id0",
            "source_title8",
            ReferenceCitationSourceUpdatedDate.fromString(
                "String9"
            ),
            SourceUpdatedDateStatusEnum.DOCUMENT_STATED,
            "text4",
            "text_sha2566",
            "title8",
            "url0"
        )
        .build()
    ),
    1,
    "public_reference",
    Status13Enum.REFERENCES_FOUND
)
.build();
```



