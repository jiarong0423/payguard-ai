# Policy Assessment Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlBvbGljeUFzc2Vzc21lbnRSZXNwb25zZQ

PolicyAssessmentResponse.


# Class Name

`PolicyAssessmentResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AdvisoryOnly` | `boolean` | Required | Advisory only. | boolean getAdvisoryOnly() | setAdvisoryOnly(boolean advisoryOnly) |
| `Chunks` | [`List<PolicyChunk>`](http://localhost:3000/llms-pages/java/models/structures/policy-chunk.md) | Required | Chunks.<br><br>**Constraints**: *Maximum Items*: `29` | List<PolicyChunk> getChunks() | setChunks(List<PolicyChunk> chunks) |
| `CorpusDigest` | `String` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getCorpusDigest() | setCorpusDigest(String corpusDigest) |
| `CorpusDigests` | [`ReferenceDigests`](http://localhost:3000/llms-pages/java/models/structures/reference-digests.md) | Required | ReferenceDigests. | ReferenceDigests getCorpusDigests() | setCorpusDigests(ReferenceDigests corpusDigests) |
| `CorpusId` | `String` | Required, Constant | Corpus id.<br><br>**Value**: `"payguard-us-official-references-v2"` | String getCorpusId() | setCorpusId(String corpusId) |
| `Coverage` | [`PolicyCoverage`](http://localhost:3000/llms-pages/java/models/structures/policy-coverage.md) | Required | PolicyCoverage. | PolicyCoverage getCoverage() | setCoverage(PolicyCoverage coverage) |
| `CurrentPolicyApplicability` | `String` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` | String getCurrentPolicyApplicability() | setCurrentPolicyApplicability(String currentPolicyApplicability) |
| `FiltersApplied` | [`PolicyContext`](http://localhost:3000/llms-pages/java/models/structures/policy-context.md) | Required | PolicyContext. | PolicyContext getFiltersApplied() | setFiltersApplied(PolicyContext filtersApplied) |
| `Limitations` | `List<String>` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` | List<String> getLimitations() | setLimitations(List<String> limitations) |
| `OperationalAuthority` | `String` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` | String getOperationalAuthority() | setOperationalAuthority(String operationalAuthority) |
| `ReasonCodes` | [`List<ReasonCode1Enum>`](http://localhost:3000/llms-pages/java/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` | List<ReasonCode1Enum> getReasonCodes() | setReasonCodes(List<ReasonCode1Enum> reasonCodes) |
| `RequiresHumanReview` | `boolean` | Required | Requires human review. | boolean getRequiresHumanReview() | setRequiresHumanReview(boolean requiresHumanReview) |
| `SchemaVersion` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` | int getSchemaVersion() | setSchemaVersion(int schemaVersion) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"public_reference"` | String getSource() | setSource(String source) |
| `Sources` | [`List<PolicySource>`](http://localhost:3000/llms-pages/java/models/structures/policy-source.md) | Required | Sources.<br><br>**Constraints**: *Maximum Items*: `16` | List<PolicySource> getSources() | setSources(List<PolicySource> sources) |
| `Status` | `String` | Required, Constant | Status.<br><br>**Value**: `"INCOMPLETE_POLICY_EVIDENCE"` | String getStatus() | setStatus(String status) |
| `Version` | `String` | Required, Constant | Version.<br><br>**Value**: `"payguard.applicability.v1"` | String getVersion() | setVersion(String version) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.CaseOutcomeEnum;
import m18000.m0.m0.m127.models.CaseStageEnum;
import m18000.m0.m0.m127.models.DecisionDateStatusEnum;
import m18000.m0.m0.m127.models.EffectiveDateStatusEnum;
import m18000.m0.m0.m127.models.MaterialType1Enum;
import m18000.m0.m0.m127.models.MissingOfficialPolicyThemeEnum;
import m18000.m0.m0.m127.models.ObservationStatusEnum;
import m18000.m0.m0.m127.models.PolicyAssessmentResponse;
import m18000.m0.m0.m127.models.PolicyChunk;
import m18000.m0.m0.m127.models.PolicyContext;
import m18000.m0.m0.m127.models.PolicyCoverage;
import m18000.m0.m0.m127.models.PolicySource;
import m18000.m0.m0.m127.models.PolicyThemeCounts;
import m18000.m0.m0.m127.models.ReasonCode1Enum;
import m18000.m0.m0.m127.models.ReferenceDigests;
import m18000.m0.m0.m127.models.SourceUpdatedDateStatusEnum;
import m18000.m0.m0.m127.models.ThemeEnum;
import m18000.m0.m0.m127.models.containers.PolicyChunkCaseOutcome;
import m18000.m0.m0.m127.models.containers.PolicySourceDecisionAcceptanceDeadline;
import m18000.m0.m0.m127.models.containers.PolicySourceDecisionDate;
import m18000.m0.m0.m127.models.containers.PolicySourceEffectiveDate;
import m18000.m0.m0.m127.models.containers.PolicySourceSourceUpdatedDate;

PolicyAssessmentResponse policyAssessmentResponse = new PolicyAssessmentResponse.Builder(
    false,
    Arrays.asList(
        new PolicyChunk.Builder(
            PolicyChunkCaseOutcome.fromCaseOutcome(
                CaseOutcomeEnum.SETTLEMENT_APPROVAL_NOT_FINAL_MERITS
            ),
            CaseStageEnum.PROCEDURAL_ORDER,
            "chunk_id6",
            "US",
            MaterialType1Enum.OFFICIAL_POLICY,
            "source_id6",
            "text_sha2560",
            ThemeEnum.VELOCITY_GUARD
        )
        .build()
    ),
    "corpus_digest2",
    new ReferenceDigests.Builder(
        "chunks_sha2564",
        "sources_sha2562"
    )
    .build(),
    "payguard-us-official-references-v2",
    new PolicyCoverage.Builder(
        "pinned_authored_summaries_only",
        false,
        Arrays.asList(
            MissingOfficialPolicyThemeEnum.SOURCE_COMPLIANCE
        ),
        new PolicyThemeCounts.Builder(
            12,
            29,
            29
        )
        .build(),
        Arrays.asList(
            "official_policy_source_ids0"
        ),
        16,
        29,
        16
    )
    .build(),
    "NOT_ESTABLISHED",
    new PolicyContext.Builder(
        "as_of0",
        "US",
        28,
        ThemeEnum.DISPUTE_MEDIATION
    )
    .build(),
    Arrays.asList(
        "limitations5",
        "limitations4",
        "limitations3"
    ),
    "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
    Arrays.asList(
        ReasonCode1Enum.CURRENT_POLICY_APPLICABILITY_NOT_ESTABLISHED,
        ReasonCode1Enum.FUTURE_OBSERVATION
    ),
    false,
    1,
    "public_reference",
    Arrays.asList(
        new PolicySource.Builder(
            Arrays.asList(
                "citation_chunk_ids2",
                "citation_chunk_ids3"
            ),
            "public_reference_summary",
            "NOT_ESTABLISHED",
            PolicySourceDecisionAcceptanceDeadline.fromString(
                "String5"
            ),
            PolicySourceDecisionDate.fromString(
                "String9"
            ),
            DecisionDateStatusEnum.DOCUMENT_STATED,
            PolicySourceEffectiveDate.fromString(
                "String7"
            ),
            EffectiveDateStatusEnum.DOCUMENT_STATED,
            "jurisdiction0",
            "US",
            MaterialType1Enum.PUBLIC_COURT_ORDER_COPY,
            "saved_retrieved_at_exact_elapsed_time",
            ObservationStatusEnum.FUTURE_OBSERVATION,
            Arrays.asList(
                ReasonCode1Enum.CURRENT_POLICY_APPLICABILITY_NOT_ESTABLISHED,
                ReasonCode1Enum.FUTURE_OBSERVATION
            ),
            "authored_paraphrase_not_full_source",
            "retrieved_at0",
            "source_id0",
            PolicySourceSourceUpdatedDate.fromString(
                "String9"
            ),
            SourceUpdatedDateStatusEnum.DOCUMENT_STATED,
            "title2",
            "url0"
        )
        .build()
    ),
    "INCOMPLETE_POLICY_EVIDENCE",
    "payguard.applicability.v1"
)
.build();
```



