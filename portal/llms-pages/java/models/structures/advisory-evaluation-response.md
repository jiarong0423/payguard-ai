# Advisory Evaluation Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkFkdmlzb3J5RXZhbHVhdGlvblJlc3BvbnNl

AdvisoryEvaluationResponse.


# Class Name

`AdvisoryEvaluationResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `PIIQuality` | `String` | Required, Constant | PII quality.<br><br>**Value**: `"NOT_EVALUATED"` | String getPIIQuality() | setPIIQuality(String pIIQuality) |
| `AdvisoryOnly` | `boolean` | Required | Advisory only. | boolean getAdvisoryOnly() | setAdvisoryOnly(boolean advisoryOnly) |
| `ClaimCount` | `int` | Required | Claim count.<br><br>**Constraints**: `>= 1`, `<= 20` | int getClaimCount() | setClaimCount(int claimCount) |
| `ClaimGates` | [`List<AdvisoryClaimGate>`](http://localhost:3000/llms-pages/java/models/structures/advisory-claim-gate.md) | Required | Claim gates.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` | List<AdvisoryClaimGate> getClaimGates() | setClaimGates(List<AdvisoryClaimGate> claimGates) |
| `CorpusDigest` | `String` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | String getCorpusDigest() | setCorpusDigest(String corpusDigest) |
| `CorpusDigests` | [`ReferenceDigests`](http://localhost:3000/llms-pages/java/models/structures/reference-digests.md) | Required | ReferenceDigests. | ReferenceDigests getCorpusDigests() | setCorpusDigests(ReferenceDigests corpusDigests) |
| `CorpusId` | `String` | Required, Constant | Corpus id.<br><br>**Value**: `"payguard-us-official-references-v2"` | String getCorpusId() | setCorpusId(String corpusId) |
| `Coverage` | [`PolicyCoverage`](http://localhost:3000/llms-pages/java/models/structures/policy-coverage.md) | Required | PolicyCoverage. | PolicyCoverage getCoverage() | setCoverage(PolicyCoverage coverage) |
| `CurrentPolicyApplicability` | `String` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` | String getCurrentPolicyApplicability() | setCurrentPolicyApplicability(String currentPolicyApplicability) |
| `Limitations` | `List<String>` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` | List<String> getLimitations() | setLimitations(List<String> limitations) |
| `ModelGeneration` | `String` | Required, Constant | Model generation.<br><br>**Value**: `"NOT_RUN"` | String getModelGeneration() | setModelGeneration(String modelGeneration) |
| `NaturalLanguageActionAssuranceQuality` | `String` | Required, Constant | Natural language action assurance quality.<br><br>**Value**: `"NOT_EVALUATED"` | String getNaturalLanguageActionAssuranceQuality() | setNaturalLanguageActionAssuranceQuality(String naturalLanguageActionAssuranceQuality) |
| `OperationalAuthority` | `String` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` | String getOperationalAuthority() | setOperationalAuthority(String operationalAuthority) |
| `PromptInjectionQuality` | `String` | Required, Constant | Prompt injection quality.<br><br>**Value**: `"NOT_EVALUATED"` | String getPromptInjectionQuality() | setPromptInjectionQuality(String promptInjectionQuality) |
| `RequestedContext` | [`PolicyContext`](http://localhost:3000/llms-pages/java/models/structures/policy-context.md) | Required | PolicyContext. | PolicyContext getRequestedContext() | setRequestedContext(PolicyContext requestedContext) |
| `RequiresHumanReview` | `boolean` | Required | Requires human review. | boolean getRequiresHumanReview() | setRequiresHumanReview(boolean requiresHumanReview) |
| `SchemaVersion` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` | int getSchemaVersion() | setSchemaVersion(int schemaVersion) |
| `SemanticEntailment` | `String` | Required, Constant | Semantic entailment.<br><br>**Value**: `"NOT_EVALUATED"` | String getSemanticEntailment() | setSemanticEntailment(String semanticEntailment) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"offline_structured_gate"` | String getSource() | setSource(String source) |
| `Status` | [`StatusEnum`](http://localhost:3000/llms-pages/java/models/enumerations/status.md) | Required | Status. | StatusEnum getStatus() | setStatus(StatusEnum status) |
| `Version` | `String` | Required, Constant | Version.<br><br>**Value**: `"payguard.advisory_eval.v1"` | String getVersion() | setVersion(String version) |


# Example

```java
import java.util.Arrays;
import m18000.m0.m0.m127.models.AdvisoryClaimGate;
import m18000.m0.m0.m127.models.AdvisoryEvaluationResponse;
import m18000.m0.m0.m127.models.ClaimTypeEnum;
import m18000.m0.m0.m127.models.MissingOfficialPolicyThemeEnum;
import m18000.m0.m0.m127.models.PolicyContext;
import m18000.m0.m0.m127.models.PolicyCoverage;
import m18000.m0.m0.m127.models.PolicyThemeCounts;
import m18000.m0.m0.m127.models.ReasonCodeEnum;
import m18000.m0.m0.m127.models.ReferenceDigests;
import m18000.m0.m0.m127.models.StatusEnum;
import m18000.m0.m0.m127.models.ThemeEnum;

AdvisoryEvaluationResponse advisoryEvaluationResponse = new AdvisoryEvaluationResponse.Builder(
    "NOT_EVALUATED",
    false,
    20,
    Arrays.asList(
        new AdvisoryClaimGate.Builder(
            19,
            ClaimTypeEnum.POLICY_REFERENCE,
            Arrays.asList(
                ReasonCodeEnum.ASSURANCE_CLAIM_FORBIDDEN,
                ReasonCodeEnum.CITATION_UNKNOWN,
                ReasonCodeEnum.CITATION_REGION_MISMATCH
            ),
            StatusEnum.INCOMPLETE_EVIDENCE,
            Arrays.asList(
                "trusted_citation_chunk_ids4",
                "trusted_citation_chunk_ids5"
            )
        )
        .build()
    ),
    "corpus_digest4",
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
    Arrays.asList(
        "limitations3",
        "limitations4",
        "limitations5"
    ),
    "NOT_RUN",
    "NOT_EVALUATED",
    "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
    "NOT_EVALUATED",
    new PolicyContext.Builder(
        "as_of8",
        "US",
        14,
        ThemeEnum.DISPUTE_MEDIATION
    )
    .build(),
    false,
    1,
    "NOT_EVALUATED",
    "offline_structured_gate",
    StatusEnum.INCOMPLETE_EVIDENCE,
    "payguard.advisory_eval.v1"
)
.build();
```



