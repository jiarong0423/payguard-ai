# Dispute Draft Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNl

DisputeDraftResponse.


# Class Name

`DisputeDraftResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AdvisoryOnly` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` | String getAdvisoryOnly() | setAdvisoryOnly(String advisoryOnly) |
| `CaseRef` | `String` | Required | Case ref. | String getCaseRef() | setCaseRef(String caseRef) |
| `DocumentRedaction` | [`DocumentRedaction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/document-redaction.md) | Required | DocumentRedaction. | DocumentRedaction getDocumentRedaction() | setDocumentRedaction(DocumentRedaction documentRedaction) |
| `DraftDigest` | `String` | Required | Draft digest. | String getDraftDigest() | setDraftDigest(String draftDigest) |
| `Evidence` | [`Evidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/evidence.md) | Required | Evidence. | Evidence getEvidence() | setEvidence(Evidence evidence) |
| `IdentityRedaction` | [`IdentityRedaction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/identity-redaction.md) | Required | IdentityRedaction. | IdentityRedaction getIdentityRedaction() | setIdentityRedaction(IdentityRedaction identityRedaction) |
| `Limitations` | `List<String>` | Required | Limitations. | List<String> getLimitations() | setLimitations(List<String> limitations) |
| `PolicyVersion` | `String` | Required | Policy version. | String getPolicyVersion() | setPolicyVersion(String policyVersion) |
| `Recommendation` | `String` | Required | Recommendation. | String getRecommendation() | setRecommendation(String recommendation) |
| `RestrictedOriginalSummary` | [`RestrictedOriginalSummary`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/restricted-original-summary.md) | Required | RestrictedOriginalSummary. | RestrictedOriginalSummary getRestrictedOriginalSummary() | setRestrictedOriginalSummary(RestrictedOriginalSummary restrictedOriginalSummary) |
| `ReviewReasons` | `List<String>` | Required | Review reasons. | List<String> getReviewReasons() | setReviewReasons(List<String> reviewReasons) |
| `Routing` | [`DisputeRouting`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/dispute-routing.md) | Required | DisputeRouting. | DisputeRouting getRouting() | setRouting(DisputeRouting routing) |
| `ScenarioMatch` | [`ScenarioMatch`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/scenario-match.md) | Required | ScenarioMatch. | ScenarioMatch getScenarioMatch() | setScenarioMatch(ScenarioMatch scenarioMatch) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` | String getSource() | setSource(String source) |
| `Status` | [`Status5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/status-5.md) | Required | Status. | Status5Enum getStatus() | setStatus(Status5Enum status) |
| `TimeEvidence` | [`DisputeDraftResponseTimeEvidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/dispute-draft-response-time-evidence.md) | Optional | This is a container for any-of cases. | DisputeDraftResponseTimeEvidence getTimeEvidence() | setTimeEvidence(DisputeDraftResponseTimeEvidence timeEvidence) |


# Example

```java
import java.util.Arrays;
import java.util.LinkedHashMap;
import m18000.m0.m0.m127.models.ChannelEnum;
import m18000.m0.m0.m127.models.DirectionEnum;
import m18000.m0.m0.m127.models.DisputeDraftResponse;
import m18000.m0.m0.m127.models.DisputeLifeCycleStageEnum;
import m18000.m0.m0.m127.models.DisputeRequirement;
import m18000.m0.m0.m127.models.DisputeRouting;
import m18000.m0.m0.m127.models.DisputeScenario;
import m18000.m0.m0.m127.models.DocumentRedaction;
import m18000.m0.m0.m127.models.DueStateEnum;
import m18000.m0.m0.m127.models.Evidence;
import m18000.m0.m0.m127.models.FieldEnum;
import m18000.m0.m0.m127.models.FlagEnum;
import m18000.m0.m0.m127.models.IdentityRedaction;
import m18000.m0.m0.m127.models.IdentityTokens;
import m18000.m0.m0.m127.models.IntakeStatusEnum;
import m18000.m0.m0.m127.models.MaterialTypeEnum;
import m18000.m0.m0.m127.models.MessageTimeEvent;
import m18000.m0.m0.m127.models.OverallStateEnum;
import m18000.m0.m0.m127.models.Reason2Enum;
import m18000.m0.m0.m127.models.RequirementStateEnum;
import m18000.m0.m0.m127.models.RestrictedOriginalSummary;
import m18000.m0.m0.m127.models.ScenarioCitation;
import m18000.m0.m0.m127.models.ScenarioMatch;
import m18000.m0.m0.m127.models.Status3Enum;
import m18000.m0.m0.m127.models.Status5Enum;
import m18000.m0.m0.m127.models.TimeEvidence;
import m18000.m0.m0.m127.models.TimeGaps;
import m18000.m0.m0.m127.models.TopicEnum;
import m18000.m0.m0.m127.models.TypeEnum;
import m18000.m0.m0.m127.models.containers.DisputeDraftResponseTimeEvidence;
import m18000.m0.m0.m127.models.containers.DisputeRequirementAction;
import m18000.m0.m0.m127.models.containers.DisputeRequirementEvidenceType;
import m18000.m0.m0.m127.models.containers.EvidenceCarrierStatus;
import m18000.m0.m0.m127.models.containers.EvidenceDeliveredAt;
import m18000.m0.m0.m127.models.containers.EvidenceOpenedAt;
import m18000.m0.m0.m127.models.containers.EvidenceOrderCreatedAt;
import m18000.m0.m0.m127.models.containers.EvidenceReason;
import m18000.m0.m0.m127.models.containers.TimeEvidenceEvents;
import m18000.m0.m0.m127.models.containers.TimeGapsDeliveryToClaim;
import m18000.m0.m0.m127.models.containers.TimeGapsPaymentToClaim;
import m18000.m0.m0.m127.models.containers.TimeGapsPaymentToDelivery;
import m18000.m0.m0.m127.models.containers.TimeGapsPaymentToOrderRecord;

DisputeDraftResponse disputeDraftResponse = new DisputeDraftResponse.Builder(
    "True",
    "case_ref8",
    new DocumentRedaction.Builder(
        new LinkedHashMap<String, Integer>() {{
            put("key0", 128);
        }},
        "INTERNAL_REVIEW_ONLY_V1",
        Arrays.asList(
            "limitations9",
            "limitations8",
            "limitations7"
        ),
        "True",
        "True",
        "HMAC-SHA256 document pseudonymization v1",
        "redacted_text8",
        128,
        "False",
        "synthetic",
        Arrays.asList(
            TypeEnum.MANUAL
        )
    )
    .build(),
    "draft_digest4",
    new Evidence.Builder(
        "synthetic"
    )
    .carrierStatus(EvidenceCarrierStatus.fromString(
            "String5"
        ))
    .deliveredAt(EvidenceDeliveredAt.fromString(
            "String1"
        ))
    .openedAt(EvidenceOpenedAt.fromString(
            "String1"
        ))
    .orderCreatedAt(EvidenceOrderCreatedAt.fromString(
            "String3"
        ))
    .reason(EvidenceReason.fromString(
            "String3"
        ))
    .build(),
    new IdentityRedaction.Builder(
        Arrays.asList(
            FieldEnum.ADDRESS,
            FieldEnum.EMAIL,
            FieldEnum.NAME
        ),
        "HMAC-SHA256 pseudonymization",
        "True",
        new IdentityTokens.Builder(
            "address_token0",
            "email_token2",
            "name_token0"
        )
        .build()
    )
    .build(),
    Arrays.asList(
        "limitations1"
    ),
    "policy_version2",
    "recommendation0",
    new RestrictedOriginalSummary.Builder(
        20,
        "False",
        "SESSION_MEMORY_ONLY",
        "SYNTHETIC_RESTRICTED_EVIDENCE",
        "NOT_IMPLEMENTED",
        "NOT_IMPLEMENTED",
        "RESTRICTED_ORIGINAL_METADATA_V1",
        96,
        "NOT_PERFORMED",
        1
    )
    .build(),
    Arrays.asList(
        "review_reasons3",
        "review_reasons4",
        "review_reasons5"
    ),
    new DisputeRouting.Builder(
        Arrays.asList(
            "available_actions6"
        ),
        DisputeLifeCycleStageEnum.INQUIRY,
        DueStateEnum.OPEN,
        "True",
        OverallStateEnum.NEEDS_INPUT,
        "NOT_PERFORMED",
        Reason2Enum.OTHER,
        Arrays.asList(
            new DisputeRequirement.Builder(
                20,
                false,
                60,
                "provider_evidence_type0",
                "request_id8",
                RequirementStateEnum.CONTEXT_ONLY,
                "source2"
            )
            .action(DisputeRequirementAction.fromString(
                    "String5"
                ))
            .evidenceType(DisputeRequirementEvidenceType.fromString(
                    "String3"
                ))
            .build()
        ),
        1,
        "seller_response_due_date4",
        "SYNTHETIC_PROVIDER_FIXTURE",
        Status3Enum.WAITING_FOR_SELLER_RESPONSE
    )
    .build(),
    new ScenarioMatch.Builder(
        "NOT_ESTABLISHED",
        "NOT_RUN",
        "AUTHORED_SYNTHETIC_DEMO_ONLY",
        IntakeStatusEnum.READY_FOR_LOCAL_RULES,
        "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
        "AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES",
        "NOT_PROVIDED",
        "True",
        new DisputeScenario.Builder(
            Arrays.asList(
                new ScenarioCitation.Builder(
                    "chunk_id0",
                    "US",
                    "locator0",
                    MaterialTypeEnum.OFFICIAL_API_REFERENCE,
                    "source_id2",
                    "text_sha2564",
                    "title4",
                    "url2"
                )
                .build()
            ),
            "SYNTHETIC_DEMO_SCENARIO",
            "PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW",
            "PAYPAL_OR_EXTERNAL_ISSUER",
            "US",
            Arrays.asList(
                "limitations3"
            ),
            "US-DEMO-DISPUTE-EVIDENCE",
            "dispute_mediation",
            "INR or counterfeit evidence organization"
        )
        .build(),
        1,
        "local_synthetic_scenario_matcher",
        "synthetic_scenarios_found"
    )
    .build(),
    "synthetic",
    Status5Enum.MANUAL_REVIEW
)
.timeEvidence(DisputeDraftResponseTimeEvidence.fromTimeEvidence(
        new TimeEvidence.Builder(
            "advisory_only8",
            Arrays.asList(
                TimeEvidenceEvents.fromMessageTimeEvent(
                    new MessageTimeEvent.Builder(
                        "at4",
                        ChannelEnum.EMAIL,
                        DirectionEnum.INBOUND,
                        "kind6",
                        "message_digest2",
                        "source4",
                        TopicEnum.ORDER_DETAILS_PROVIDED
                    )
                    .build()
                )
            ),
            Arrays.asList(
                FlagEnum.ORDER_RECORD_ABSENT,
                FlagEnum.DELIVERY_NOT_RECORDED,
                FlagEnum.DELIVERY_AFTER_CLAIM
            ),
            new TimeGaps.Builder(
                TimeGapsDeliveryToClaim.fromNumber(
                    210
                ),
                TimeGapsPaymentToClaim.fromNumber(
                    154
                ),
                TimeGapsPaymentToDelivery.fromNumber(
                    192
                ),
                TimeGapsPaymentToOrderRecord.fromNumber(
                    208
                )
            )
            .build(),
            "judgement4",
            "schema_version6"
        )
        .build()
    ))
.build();
```



