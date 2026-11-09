# Dispute Draft Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNl

DisputeDraftResponse.


# Class Name

`DisputeDraftResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `CaseRef` | `string` | Required | Case ref. |
| `DocumentRedaction` | [`models.DocumentRedaction`](http://localhost:3000/llms-pages/go/models/structures/document-redaction.md) | Required | DocumentRedaction. |
| `DraftDigest` | `string` | Required | Draft digest. |
| `Evidence` | [`models.Evidence`](http://localhost:3000/llms-pages/go/models/structures/evidence.md) | Required | Evidence. |
| `IdentityRedaction` | [`models.IdentityRedaction`](http://localhost:3000/llms-pages/go/models/structures/identity-redaction.md) | Required | IdentityRedaction. |
| `Limitations` | `[]string` | Required | Limitations. |
| `PolicyVersion` | `string` | Required | Policy version. |
| `Recommendation` | `string` | Required | Recommendation. |
| `RestrictedOriginalSummary` | [`models.RestrictedOriginalSummary`](http://localhost:3000/llms-pages/go/models/structures/restricted-original-summary.md) | Required | RestrictedOriginalSummary. |
| `ReviewReasons` | `[]string` | Required | Review reasons. |
| `Routing` | [`models.DisputeRouting`](http://localhost:3000/llms-pages/go/models/structures/dispute-routing.md) | Required | DisputeRouting. |
| `ScenarioMatch` | [`models.ScenarioMatch`](http://localhost:3000/llms-pages/go/models/structures/scenario-match.md) | Required | ScenarioMatch. |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `Status` | [`models.Status5Enum`](http://localhost:3000/llms-pages/go/models/enumerations/status-5.md) | Required | Status. |
| `TimeEvidence` | [`*models.DisputeDraftResponseTimeEvidence`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/dispute-draft-response-time-evidence.md) | Optional | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    disputeDraftResponse := models.DisputeDraftResponse{
        AdvisoryOnly:              "True",
        CaseRef:                   "case_ref8",
        DocumentRedaction:         models.DocumentRedaction{
            Counts:               map[string]int{
                "key0": 128,
            },
            ExportProfile:        "INTERNAL_REVIEW_ONLY_V1",
            Limitations:          []string{
                "limitations9",
                "limitations8",
                "limitations7",
            },
            LimitedDetection:     "True",
            ManualReviewRequired: "True",
            Method:               "HMAC-SHA256 document pseudonymization v1",
            RedactedText:         "redacted_text8",
            ReplacementCount:     128,
            Reversibility:        "False",
            Source:               "synthetic",
            Types:                []models.TypeEnum{
                models.TypeEnum_MANUAL,
            },
        },
        DraftDigest:               "draft_digest4",
        Evidence:                  models.Evidence{
            CarrierStatus:  models.ToPointer(models.EvidenceCarrierStatusContainer.FromString("String5")),
            DeliveredAt:    models.ToPointer(models.EvidenceDeliveredAtContainer.FromString("String1")),
            EvidenceSource: "synthetic",
            OpenedAt:       models.ToPointer(models.EvidenceOpenedAtContainer.FromString("String1")),
            OrderCreatedAt: models.ToPointer(models.EvidenceOrderCreatedAtContainer.FromString("String3")),
            Reason:         models.ToPointer(models.EvidenceReasonContainer.FromString("String3")),
        },
        IdentityRedaction:         models.IdentityRedaction{
            Fields:    []models.FieldEnum{
                models.FieldEnum_ADDRESS,
                models.FieldEnum_EMAIL,
                models.FieldEnum_NAME,
            },
            Method:    "HMAC-SHA256 pseudonymization",
            Synthetic: "True",
            Tokens:    models.IdentityTokens{
                AddressToken: "address_token0",
                EmailToken:   "email_token2",
                NameToken:    "name_token0",
            },
        },
        Limitations:               []string{
            "limitations1",
        },
        PolicyVersion:             "policy_version2",
        Recommendation:            "recommendation0",
        RestrictedOriginalSummary: models.RestrictedOriginalSummary{
            AttachmentCount:    20,
            ContentReturned:    "False",
            Custody:            "SESSION_MEMORY_ONLY",
            DataClass:          "SYNTHETIC_RESTRICTED_EVIDENCE",
            PersistentStorage:  "NOT_IMPLEMENTED",
            ProductionPiiVault: "NOT_IMPLEMENTED",
            Profile:            "RESTRICTED_ORIGINAL_METADATA_V1",
            ProofRecordCount:   96,
            ProviderSubmission: "NOT_PERFORMED",
            SchemaVersion:      1,
        },
        ReviewReasons:             []string{
            "review_reasons3",
            "review_reasons4",
            "review_reasons5",
        },
        Routing:                   models.DisputeRouting{
            AvailableActions:      []string{
                "available_actions6",
            },
            DisputeLifeCycleStage: models.DisputeLifeCycleStageEnum_INQUIRY,
            DueState:              models.DueStateEnum_OPEN,
            HumanReviewRequired:   "True",
            OverallState:          models.OverallStateEnum_NEEDSINPUT,
            ProviderSubmission:    "NOT_PERFORMED",
            Reason:                models.Reason2Enum_OTHER,
            Requirements:          []models.DisputeRequirement{
                models.DisputeRequirement{
                    AcceptedAttachmentCount: 20,
                    Action:                  models.ToPointer(models.DisputeRequirementActionContainer.FromString("String5")),
                    EvidenceType:            models.ToPointer(models.DisputeRequirementEvidenceTypeContainer.FromString("String3")),
                    Mandatory:               false,
                    ProofCount:              60,
                    ProviderEvidenceType:    "provider_evidence_type0",
                    RequestId:               "request_id8",
                    RequirementState:        models.RequirementStateEnum_CONTEXTONLY,
                    Source:                  "source2",
                },
            },
            SchemaVersion:         1,
            SellerResponseDueDate: "seller_response_due_date4",
            SnapshotClass:         "SYNTHETIC_PROVIDER_FIXTURE",
            Status:                models.Status3Enum_WAITINGFORSELLERRESPONSE,
        },
        ScenarioMatch:             models.ScenarioMatch{
            CurrentPolicyApplicability: "NOT_ESTABLISHED",
            EngineExecution:            "NOT_RUN",
            EvaluationScope:            "AUTHORED_SYNTHETIC_DEMO_ONLY",
            IntakeStatus:               models.IntakeStatusEnum_READYFORLOCALRULES,
            OperationalAuthority:       "REFERENCE_ONLY_NO_ACTION_AUTHORIZATION",
            Provenance:                 "AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES",
            RealCaseEvidence:           "NOT_PROVIDED",
            RequiredHumanReview:        "True",
            Scenario:                   models.DisputeScenario{
                Citations:      []models.ScenarioCitation{
                    models.ScenarioCitation{
                        ChunkId:      "chunk_id0",
                        Jurisdiction: "US",
                        Locator:      "locator0",
                        MaterialType: models.MaterialTypeEnum_OFFICIALAPIREFERENCE,
                        SourceId:     "source_id2",
                        TextSha256:   "text_sha2564",
                        Title:        "title4",
                        Url:          "url2",
                    },
                },
                EvidenceClass:  "SYNTHETIC_DEMO_SCENARIO",
                ExpectedRoute:  "PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW",
                FinalAuthority: "PAYPAL_OR_EXTERNAL_ISSUER",
                Jurisdiction:   "US",
                Limitations:    []string{
                    "limitations3",
                },
                ScenarioId:     "US-DEMO-DISPUTE-EVIDENCE",
                Theme:          "dispute_mediation",
                Title:          "INR or counterfeit evidence organization",
            },
            SchemaVersion:              1,
            Source:                     "local_synthetic_scenario_matcher",
            Status:                     "synthetic_scenarios_found",
        },
        Source:                    "synthetic",
        Status:                    models.Status5Enum_MANUALREVIEW,
        TimeEvidence:              models.ToPointer(models.DisputeDraftResponseTimeEvidenceContainer.FromTimeEvidence(models.TimeEvidence{
            AdvisoryOnly:         "advisory_only8",
            Events:               []models.TimeEvidenceEvents{
                models.TimeEvidenceEventsContainer.FromMessageTimeEvent(models.MessageTimeEvent{
                    At:                   "at4",
                    Channel:              models.ChannelEnum_EMAIL,
                    Direction:            models.DirectionEnum_INBOUND,
                    Kind:                 "kind6",
                    MessageDigest:        "message_digest2",
                    Source:               "source4",
                    Topic:                models.TopicEnum_ORDERDETAILSPROVIDED,
                }),
            },
            Flags:                []models.FlagEnum{
                models.FlagEnum_ORDERRECORDABSENT,
                models.FlagEnum_DELIVERYNOTRECORDED,
                models.FlagEnum_DELIVERYAFTERCLAIM,
            },
            GapsSeconds:          models.TimeGaps{
                DeliveryToClaim:      models.TimeGapsDeliveryToClaimContainer.FromNumber(210),
                PaymentToClaim:       models.TimeGapsPaymentToClaimContainer.FromNumber(154),
                PaymentToDelivery:    models.TimeGapsPaymentToDeliveryContainer.FromNumber(192),
                PaymentToOrderRecord: models.TimeGapsPaymentToOrderRecordContainer.FromNumber(208),
            },
            Judgement:            "judgement4",
            SchemaVersion:        "schema_version6",
        })),
    }

}
```



