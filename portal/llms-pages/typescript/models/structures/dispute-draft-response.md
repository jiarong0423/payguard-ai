# Dispute Draft Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNl

DisputeDraftResponse.


# Interface Name

`DisputeDraftResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `caseRef` | `string` | Required | Case ref. |
| `documentRedaction` | [`DocumentRedaction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/document-redaction.md) | Required | DocumentRedaction. |
| `draftDigest` | `string` | Required | Draft digest. |
| `evidence` | [`Evidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/evidence.md) | Required | Evidence. |
| `identityRedaction` | [`IdentityRedaction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/identity-redaction.md) | Required | IdentityRedaction. |
| `limitations` | `string[]` | Required | Limitations. |
| `policyVersion` | `string` | Required | Policy version. |
| `recommendation` | `string` | Required | Recommendation. |
| `restrictedOriginalSummary` | [`RestrictedOriginalSummary`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/restricted-original-summary.md) | Required | RestrictedOriginalSummary. |
| `reviewReasons` | `string[]` | Required | Review reasons. |
| `routing` | [`DisputeRouting`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/dispute-routing.md) | Required | DisputeRouting. |
| `scenarioMatch` | [`ScenarioMatch`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/scenario-match.md) | Required | ScenarioMatch. |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `status` | [`Status5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/status-5.md) | Required | Status. |
| `timeEvidence` | [`DisputeDraftResponseTimeEvidence \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/dispute-draft-response-time-evidence.md) | Optional | This is a container for any-of cases. |


# Example

```ts
import {
  ChannelEnum,
  DirectionEnum,
  DisputeDraftResponse,
  DisputeLifeCycleStageEnum,
  DueStateEnum,
  FieldEnum,
  FlagEnum,
  IntakeStatusEnum,
  MaterialTypeEnum,
  OverallStateEnum,
  Reason2Enum,
  RequirementStateEnum,
  Status3Enum,
  Status5Enum,
  TopicEnum,
  TypeEnum,
} from 'tradeglot-local-consolelib';

const disputeDraftResponse: DisputeDraftResponse = {
  advisoryOnly: 'True',
  caseRef: 'case_ref8',
  documentRedaction: {
    counts: {
      'key0': 128
    },
    exportProfile: 'INTERNAL_REVIEW_ONLY_V1',
    limitations: [
      'limitations9',
      'limitations8',
      'limitations7'
    ],
    limitedDetection: 'True',
    manualReviewRequired: 'True',
    method: 'HMAC-SHA256 document pseudonymization v1',
    redactedText: 'redacted_text8',
    replacementCount: 128,
    reversibility: 'False',
    source: 'synthetic',
    types: [
      TypeEnum.Manual
    ],
  },
  draftDigest: 'draft_digest4',
  evidence: {
    evidenceSource: 'synthetic',
    carrierStatus: 'String5',
    deliveredAt: 'String1',
    openedAt: 'String1',
    orderCreatedAt: 'String3',
    reason: 'String3',
  },
  identityRedaction: {
    fields: [
      FieldEnum.Address,
      FieldEnum.Email,
      FieldEnum.Name
    ],
    method: 'HMAC-SHA256 pseudonymization',
    synthetic: 'True',
    tokens: {
      addressToken: 'address_token0',
      emailToken: 'email_token2',
      nameToken: 'name_token0',
    },
  },
  limitations: [
    'limitations1'
  ],
  policyVersion: 'policy_version2',
  recommendation: 'recommendation0',
  restrictedOriginalSummary: {
    attachmentCount: 20,
    contentReturned: 'False',
    custody: 'SESSION_MEMORY_ONLY',
    dataClass: 'SYNTHETIC_RESTRICTED_EVIDENCE',
    persistentStorage: 'NOT_IMPLEMENTED',
    productionPiiVault: 'NOT_IMPLEMENTED',
    profile: 'RESTRICTED_ORIGINAL_METADATA_V1',
    proofRecordCount: 96,
    providerSubmission: 'NOT_PERFORMED',
    schemaVersion: 1,
  },
  reviewReasons: [
    'review_reasons3',
    'review_reasons4',
    'review_reasons5'
  ],
  routing: {
    availableActions: [
      'available_actions6'
    ],
    disputeLifeCycleStage: DisputeLifeCycleStageEnum.INQUIRY,
    dueState: DueStateEnum.OPEN,
    humanReviewRequired: 'True',
    overallState: OverallStateEnum.NEEDSINPUT,
    providerSubmission: 'NOT_PERFORMED',
    reason: Reason2Enum.OTHER,
    requirements: [
      {
        acceptedAttachmentCount: 20,
        mandatory: false,
        proofCount: 60,
        providerEvidenceType: 'provider_evidence_type0',
        requestId: 'request_id8',
        requirementState: RequirementStateEnum.CONTEXTONLY,
        source: 'source2',
        action: 'String5',
        evidenceType: 'String3',
      }
    ],
    schemaVersion: 1,
    sellerResponseDueDate: 'seller_response_due_date4',
    snapshotClass: 'SYNTHETIC_PROVIDER_FIXTURE',
    status: Status3Enum.WAITINGFORSELLERRESPONSE,
  },
  scenarioMatch: {
    currentPolicyApplicability: 'NOT_ESTABLISHED',
    engineExecution: 'NOT_RUN',
    evaluationScope: 'AUTHORED_SYNTHETIC_DEMO_ONLY',
    intakeStatus: IntakeStatusEnum.ReadyForLocalRules,
    operationalAuthority: 'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',
    provenance: 'AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES',
    realCaseEvidence: 'NOT_PROVIDED',
    requiredHumanReview: 'True',
    scenario: {
      citations: [
        {
          chunkId: 'chunk_id0',
          jurisdiction: 'US',
          locator: 'locator0',
          materialType: MaterialTypeEnum.OfficialApiReference,
          sourceId: 'source_id2',
          textSha256: 'text_sha2564',
          title: 'title4',
          url: 'url2',
        }
      ],
      evidenceClass: 'SYNTHETIC_DEMO_SCENARIO',
      expectedRoute: 'PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW',
      finalAuthority: 'PAYPAL_OR_EXTERNAL_ISSUER',
      jurisdiction: 'US',
      limitations: [
        'limitations3'
      ],
      scenarioId: 'US-DEMO-DISPUTE-EVIDENCE',
      theme: 'dispute_mediation',
      title: 'INR or counterfeit evidence organization',
    },
    schemaVersion: 1,
    source: 'local_synthetic_scenario_matcher',
    status: 'synthetic_scenarios_found',
  },
  source: 'synthetic',
  status: Status5Enum.ManualReview,
  timeEvidence: {
    advisoryOnly: 'advisory_only8',
    events: [
      {
        at: 'at4',
        channel: ChannelEnum.EMAIL,
        direction: DirectionEnum.INBOUND,
        kind: 'kind6',
        messageDigest: 'message_digest2',
        source: 'source4',
        topic: TopicEnum.ORDERDETAILSPROVIDED,
      }
    ],
    flags: [
      FlagEnum.ORDERRECORDABSENT,
      FlagEnum.DELIVERYNOTRECORDED,
      FlagEnum.DELIVERYAFTERCLAIM
    ],
    gapsSeconds: {
      deliveryToClaim: 210,
      paymentToClaim: 154,
      paymentToDelivery: 192,
      paymentToOrderRecord: 208,
    },
    judgement: 'judgement4',
    schemaVersion: 'schema_version6',
  },
};
```



