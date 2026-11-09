# Dispute Draft Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNl

DisputeDraftResponse.


# Class Name

`DisputeDraftResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `case_ref` | `String` | Required | Case ref. |
| `document_redaction` | [`DocumentRedaction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/document-redaction.md) | Required | DocumentRedaction. |
| `draft_digest` | `String` | Required | Draft digest. |
| `evidence` | [`Evidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/evidence.md) | Required | Evidence. |
| `identity_redaction` | [`IdentityRedaction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/identity-redaction.md) | Required | IdentityRedaction. |
| `limitations` | `Array[String]` | Required | Limitations. |
| `policy_version` | `String` | Required | Policy version. |
| `recommendation` | `String` | Required | Recommendation. |
| `restricted_original_summary` | [`RestrictedOriginalSummary`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/restricted-original-summary.md) | Required | RestrictedOriginalSummary. |
| `review_reasons` | `Array[String]` | Required | Review reasons. |
| `routing` | [`DisputeRouting`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/dispute-routing.md) | Required | DisputeRouting. |
| `scenario_match` | [`ScenarioMatch`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/scenario-match.md) | Required | ScenarioMatch. |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `status` | [`Status5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/status-5.md) | Required | Status. |
| `time_evidence` | [TimeEvidence](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/time-evidence.md) \| nil | Optional | This is a container for any-of cases. |


# Example

```ruby
dispute_draft_response = DisputeDraftResponse.new(
  'True',
  'case_ref2',
  DocumentRedaction.new(
    {
      'key0': 128
    },
    'INTERNAL_REVIEW_ONLY_V1',
    [
      'limitations9',
      'limitations8',
      'limitations7'
    ],
    'True',
    'True',
    'HMAC-SHA256 document pseudonymization v1',
    'redacted_text8',
    128,
    'False',
    'synthetic',
    [
      TypeEnum::MANUAL
    ]
  ),
  'draft_digest8',
  Evidence.new(
    'synthetic',
    'String5',
    'String1',
    'String1',
    'String3',
    'String3'
  ),
  IdentityRedaction.new(
    [
      FieldEnum::ADDRESS,
      FieldEnum::EMAIL,
      FieldEnum::NAME
    ],
    'HMAC-SHA256 pseudonymization',
    'True',
    IdentityTokens.new(
      'address_token0',
      'email_token2',
      'name_token0'
    )
  ),
  [
    'limitations5',
    'limitations4',
    'limitations3'
  ],
  'policy_version6',
  'recommendation4',
  RestrictedOriginalSummary.new(
    20,
    'False',
    'SESSION_MEMORY_ONLY',
    'SYNTHETIC_RESTRICTED_EVIDENCE',
    'NOT_IMPLEMENTED',
    'NOT_IMPLEMENTED',
    'RESTRICTED_ORIGINAL_METADATA_V1',
    96,
    'NOT_PERFORMED',
    1
  ),
  [
    'review_reasons7'
  ],
  DisputeRouting.new(
    [
      'available_actions6'
    ],
    DisputeLifeCycleStageEnum::INQUIRY,
    DueStateEnum::OPEN,
    'True',
    OverallStateEnum::NEEDS_INPUT,
    'NOT_PERFORMED',
    Reason2Enum::OTHER,
    [
      DisputeRequirement.new(
        20,
        false,
        60,
        'provider_evidence_type0',
        'request_id8',
        RequirementStateEnum::CONTEXT_ONLY,
        'source2',
        'String5',
        'String3'
      )
    ],
    1,
    'seller_response_due_date4',
    'SYNTHETIC_PROVIDER_FIXTURE',
    Status3Enum::WAITING_FOR_SELLER_RESPONSE
  ),
  ScenarioMatch.new(
    'NOT_ESTABLISHED',
    'NOT_RUN',
    'AUTHORED_SYNTHETIC_DEMO_ONLY',
    IntakeStatusEnum::READY_FOR_LOCAL_RULES,
    'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',
    'AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES',
    'NOT_PROVIDED',
    'True',
    DisputeScenario.new(
      [
        ScenarioCitation.new(
          'chunk_id0',
          'US',
          'locator0',
          MaterialTypeEnum::OFFICIAL_API_REFERENCE,
          'source_id2',
          'text_sha2564',
          'title4',
          'url2'
        )
      ],
      'SYNTHETIC_DEMO_SCENARIO',
      'PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW',
      'PAYPAL_OR_EXTERNAL_ISSUER',
      'US',
      [
        'limitations3'
      ],
      'US-DEMO-DISPUTE-EVIDENCE',
      'dispute_mediation',
      'INR or counterfeit evidence organization'
    ),
    1,
    'local_synthetic_scenario_matcher',
    'synthetic_scenarios_found'
  ),
  'synthetic',
  Status5Enum::MANUAL_REVIEW,
  TimeEvidence.new(
    'advisory_only8',
    [
      MessageTimeEvent.new(
        'at4',
        ChannelEnum::EMAIL,
        DirectionEnum::INBOUND,
        'kind6',
        'message_digest2',
        'source4',
        TopicEnum::ORDER_DETAILS_PROVIDED
      )
    ],
    [
      FlagEnum::ORDER_RECORD_ABSENT,
      FlagEnum::DELIVERY_NOT_RECORDED,
      FlagEnum::DELIVERY_AFTER_CLAIM
    ],
    TimeGaps.new(
      210,
      154,
      192,
      208
    ),
    'judgement4',
    'schema_version6'
  )
)
```



