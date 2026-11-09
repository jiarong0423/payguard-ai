# Dispute Draft Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNl

DisputeDraftResponse.


# Class Name

`DisputeDraftResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `CaseRef` | `string` | Required | Case ref. |
| `DocumentRedaction` | [`DocumentRedaction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/document-redaction.md) | Required | DocumentRedaction. |
| `DraftDigest` | `string` | Required | Draft digest. |
| `Evidence` | [`Evidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/evidence.md) | Required | Evidence. |
| `IdentityRedaction` | [`IdentityRedaction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/identity-redaction.md) | Required | IdentityRedaction. |
| `Limitations` | `List<string>` | Required | Limitations. |
| `PolicyVersion` | `string` | Required | Policy version. |
| `Recommendation` | `string` | Required | Recommendation. |
| `RestrictedOriginalSummary` | [`RestrictedOriginalSummary`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/restricted-original-summary.md) | Required | RestrictedOriginalSummary. |
| `ReviewReasons` | `List<string>` | Required | Review reasons. |
| `Routing` | [`DisputeRouting`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/dispute-routing.md) | Required | DisputeRouting. |
| `ScenarioMatch` | [`ScenarioMatch`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/scenario-match.md) | Required | ScenarioMatch. |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `Status` | [`Status5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/status-5.md) | Required | Status. |
| `TimeEvidence` | [`DisputeDraftResponseTimeEvidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-draft-response-time-evidence.md) | Optional | This is a container for any-of cases. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

DisputeDraftResponse disputeDraftResponse = new DisputeDraftResponse
{
    AdvisoryOnly = "True",
    CaseRef = "case_ref8",
    DocumentRedaction = new DocumentRedaction
    {
        Counts = new Dictionary<string, int>
        {
            ["key0"] = 128,
        },
        ExportProfile = "INTERNAL_REVIEW_ONLY_V1",
        Limitations = new List<string>
        {
            "limitations9",
            "limitations8",
            "limitations7",
        },
        LimitedDetection = "True",
        ManualReviewRequired = "True",
        Method = "HMAC-SHA256 document pseudonymization v1",
        RedactedText = "redacted_text8",
        ReplacementCount = 128,
        Reversibility = "False",
        Source = "synthetic",
        Types = new List<TypeEnum>
        {
            TypeEnum.Manual,
        },
    },
    DraftDigest = "draft_digest4",
    Evidence = new Evidence
    {
        EvidenceSource = "synthetic",
        CarrierStatus = EvidenceCarrierStatus.FromString("String5"),
        DeliveredAt = EvidenceDeliveredAt.FromString("String1"),
        OpenedAt = EvidenceOpenedAt.FromString("String1"),
        OrderCreatedAt = EvidenceOrderCreatedAt.FromString("String3"),
        Reason = EvidenceReason.FromString("String3"),
    },
    IdentityRedaction = new IdentityRedaction
    {
        Fields = new List<FieldEnum>
        {
            FieldEnum.Address,
            FieldEnum.Email,
            FieldEnum.Name,
        },
        Method = "HMAC-SHA256 pseudonymization",
        Synthetic = "True",
        Tokens = new IdentityTokens
        {
            AddressToken = "address_token0",
            EmailToken = "email_token2",
            NameToken = "name_token0",
        },
    },
    Limitations = new List<string>
    {
        "limitations1",
    },
    PolicyVersion = "policy_version2",
    Recommendation = "recommendation0",
    RestrictedOriginalSummary = new RestrictedOriginalSummary
    {
        AttachmentCount = 20,
        ContentReturned = "False",
        Custody = "SESSION_MEMORY_ONLY",
        DataClass = "SYNTHETIC_RESTRICTED_EVIDENCE",
        PersistentStorage = "NOT_IMPLEMENTED",
        ProductionPiiVault = "NOT_IMPLEMENTED",
        Profile = "RESTRICTED_ORIGINAL_METADATA_V1",
        ProofRecordCount = 96,
        ProviderSubmission = "NOT_PERFORMED",
        SchemaVersion = 1,
    },
    ReviewReasons = new List<string>
    {
        "review_reasons3",
        "review_reasons4",
        "review_reasons5",
    },
    Routing = new DisputeRouting
    {
        AvailableActions = new List<string>
        {
            "available_actions6",
        },
        DisputeLifeCycleStage = DisputeLifeCycleStageEnum.INQUIRY,
        DueState = DueStateEnum.OPEN,
        HumanReviewRequired = "True",
        OverallState = OverallStateEnum.NEEDSINPUT,
        ProviderSubmission = "NOT_PERFORMED",
        Reason = Reason2Enum.OTHER,
        Requirements = new List<DisputeRequirement>
        {
            new DisputeRequirement
            {
                AcceptedAttachmentCount = 20,
                Mandatory = false,
                ProofCount = 60,
                ProviderEvidenceType = "provider_evidence_type0",
                RequestId = "request_id8",
                RequirementState = RequirementStateEnum.CONTEXTONLY,
                Source = "source2",
                Action = DisputeRequirementAction.FromString("String5"),
                EvidenceType = DisputeRequirementEvidenceType.FromString("String3"),
            },
        },
        SchemaVersion = 1,
        SellerResponseDueDate = "seller_response_due_date4",
        SnapshotClass = "SYNTHETIC_PROVIDER_FIXTURE",
        Status = Status3Enum.WAITINGFORSELLERRESPONSE,
    },
    ScenarioMatch = new ScenarioMatch
    {
        CurrentPolicyApplicability = "NOT_ESTABLISHED",
        EngineExecution = "NOT_RUN",
        EvaluationScope = "AUTHORED_SYNTHETIC_DEMO_ONLY",
        IntakeStatus = IntakeStatusEnum.ReadyForLocalRules,
        OperationalAuthority = "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
        Provenance = "AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES",
        RealCaseEvidence = "NOT_PROVIDED",
        RequiredHumanReview = "True",
        Scenario = new DisputeScenario
        {
            Citations = new List<ScenarioCitation>
            {
                new ScenarioCitation
                {
                    ChunkId = "chunk_id0",
                    Jurisdiction = "US",
                    Locator = "locator0",
                    MaterialType = MaterialTypeEnum.OfficialApiReference,
                    SourceId = "source_id2",
                    TextSha256 = "text_sha2564",
                    Title = "title4",
                    Url = "url2",
                },
            },
            EvidenceClass = "SYNTHETIC_DEMO_SCENARIO",
            ExpectedRoute = "PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW",
            FinalAuthority = "PAYPAL_OR_EXTERNAL_ISSUER",
            Jurisdiction = "US",
            Limitations = new List<string>
            {
                "limitations3",
            },
            ScenarioId = "US-DEMO-DISPUTE-EVIDENCE",
            Theme = "dispute_mediation",
            Title = "INR or counterfeit evidence organization",
        },
        SchemaVersion = 1,
        Source = "local_synthetic_scenario_matcher",
        Status = "synthetic_scenarios_found",
    },
    Source = "synthetic",
    Status = Status5Enum.ManualReview,
    TimeEvidence = DisputeDraftResponseTimeEvidence.FromTimeEvidence(
        new TimeEvidence
        {
            AdvisoryOnly = "advisory_only8",
            Events = new List<TimeEvidenceEvents>
            {
                TimeEvidenceEvents.FromMessageTimeEvent(
                    new MessageTimeEvent
                    {
                        At = "at4",
                        Channel = ChannelEnum.EMAIL,
                        Direction = DirectionEnum.INBOUND,
                        Kind = "kind6",
                        MessageDigest = "message_digest2",
                        Source = "source4",
                        Topic = TopicEnum.ORDERDETAILSPROVIDED,
                    }
                ),
            },
            Flags = new List<FlagEnum>
            {
                FlagEnum.ORDERRECORDABSENT,
                FlagEnum.DELIVERYNOTRECORDED,
                FlagEnum.DELIVERYAFTERCLAIM,
            },
            GapsSeconds = new TimeGaps
            {
                DeliveryToClaim = TimeGapsDeliveryToClaim.FromNumber(210),
                PaymentToClaim = TimeGapsPaymentToClaim.FromNumber(154),
                PaymentToDelivery = TimeGapsPaymentToDelivery.FromNumber(192),
                PaymentToOrderRecord = TimeGapsPaymentToOrderRecord.FromNumber(208),
            },
            Judgement = "judgement4",
            SchemaVersion = "schema_version6",
        }
    ),
};
```



