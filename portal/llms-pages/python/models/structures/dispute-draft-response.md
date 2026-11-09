# Dispute Draft Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNl

DisputeDraftResponse.


# Class Name

`DisputeDraftResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `str` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `case_ref` | `str` | Required | Case ref. |
| `document_redaction` | [`DocumentRedaction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/document-redaction.md) | Required | DocumentRedaction. |
| `draft_digest` | `str` | Required | Draft digest. |
| `evidence` | [`Evidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/evidence.md) | Required | Evidence. |
| `identity_redaction` | [`IdentityRedaction`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/identity-redaction.md) | Required | IdentityRedaction. |
| `limitations` | `List[str]` | Required | Limitations. |
| `policy_version` | `str` | Required | Policy version. |
| `recommendation` | `str` | Required | Recommendation. |
| `restricted_original_summary` | [`RestrictedOriginalSummary`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/restricted-original-summary.md) | Required | RestrictedOriginalSummary. |
| `review_reasons` | `List[str]` | Required | Review reasons. |
| `routing` | [`DisputeRouting`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/dispute-routing.md) | Required | DisputeRouting. |
| `scenario_match` | [`ScenarioMatch`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/scenario-match.md) | Required | ScenarioMatch. |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `status` | [`Status5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/status-5.md) | Required | Status. |
| `time_evidence` | [TimeEvidence](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/time-evidence.md) \| None | Optional | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.channel_enum import ChannelEnum
from tradeglotlocalconsole.models.direction_enum import DirectionEnum
from tradeglotlocalconsole.models.dispute_draft_response import DisputeDraftResponse
from tradeglotlocalconsole.models.dispute_life_cycle_stage_enum import DisputeLifeCycleStageEnum
from tradeglotlocalconsole.models.dispute_requirement import DisputeRequirement
from tradeglotlocalconsole.models.dispute_routing import DisputeRouting
from tradeglotlocalconsole.models.dispute_scenario import DisputeScenario
from tradeglotlocalconsole.models.document_redaction import DocumentRedaction
from tradeglotlocalconsole.models.due_state_enum import DueStateEnum
from tradeglotlocalconsole.models.evidence import Evidence
from tradeglotlocalconsole.models.field_enum import FieldEnum
from tradeglotlocalconsole.models.flag_enum import FlagEnum
from tradeglotlocalconsole.models.identity_redaction import IdentityRedaction
from tradeglotlocalconsole.models.identity_tokens import IdentityTokens
from tradeglotlocalconsole.models.intake_status_enum import IntakeStatusEnum
from tradeglotlocalconsole.models.material_type_enum import MaterialTypeEnum
from tradeglotlocalconsole.models.message_time_event import MessageTimeEvent
from tradeglotlocalconsole.models.overall_state_enum import OverallStateEnum
from tradeglotlocalconsole.models.reason_2_enum import Reason2Enum
from tradeglotlocalconsole.models.requirement_state_enum import RequirementStateEnum
from tradeglotlocalconsole.models.restricted_original_summary import RestrictedOriginalSummary
from tradeglotlocalconsole.models.scenario_citation import ScenarioCitation
from tradeglotlocalconsole.models.scenario_match import ScenarioMatch
from tradeglotlocalconsole.models.status_3_enum import Status3Enum
from tradeglotlocalconsole.models.status_5_enum import Status5Enum
from tradeglotlocalconsole.models.time_evidence import TimeEvidence
from tradeglotlocalconsole.models.time_gaps import TimeGaps
from tradeglotlocalconsole.models.topic_enum import TopicEnum
from tradeglotlocalconsole.models.type_enum import TypeEnum

dispute_draft_response = DisputeDraftResponse(
    case_ref='case_ref2',
    document_redaction=DocumentRedaction(
        counts={
            'key0': 128
        },
        limitations=[
            'limitations9',
            'limitations8',
            'limitations7'
        ],
        redacted_text='redacted_text8',
        replacement_count=128,
        types=[
            TypeEnum.MANUAL
        ]
    ),
    draft_digest='draft_digest8',
    evidence=Evidence(
        carrier_status='String5',
        delivered_at='String1',
        opened_at='String1',
        order_created_at='String3',
        reason='String3'
    ),
    identity_redaction=IdentityRedaction(
        fields=[
            FieldEnum.ADDRESS,
            FieldEnum.EMAIL,
            FieldEnum.NAME
        ],
        tokens=IdentityTokens(
            address_token='address_token0',
            email_token='email_token2',
            name_token='name_token0'
        )
    ),
    limitations=[
        'limitations5',
        'limitations4',
        'limitations3'
    ],
    policy_version='policy_version6',
    recommendation='recommendation4',
    restricted_original_summary=RestrictedOriginalSummary(
        attachment_count=20,
        proof_record_count=96
    ),
    review_reasons=[
        'review_reasons7'
    ],
    routing=DisputeRouting(
        available_actions=[
            'available_actions6'
        ],
        dispute_life_cycle_stage=DisputeLifeCycleStageEnum.INQUIRY,
        due_state=DueStateEnum.OPEN,
        overall_state=OverallStateEnum.NEEDS_INPUT,
        reason=Reason2Enum.OTHER,
        requirements=[
            DisputeRequirement(
                accepted_attachment_count=20,
                mandatory=False,
                proof_count=60,
                provider_evidence_type='provider_evidence_type0',
                request_id='request_id8',
                requirement_state=RequirementStateEnum.CONTEXT_ONLY,
                source='source2',
                action='String5',
                evidence_type='String3'
            )
        ],
        seller_response_due_date='seller_response_due_date4',
        status=Status3Enum.WAITING_FOR_SELLER_RESPONSE
    ),
    scenario_match=ScenarioMatch(
        intake_status=IntakeStatusEnum.READY_FOR_LOCAL_RULES,
        scenario=DisputeScenario(
            citations=[
                ScenarioCitation(
                    chunk_id='chunk_id0',
                    locator='locator0',
                    material_type=MaterialTypeEnum.OFFICIAL_API_REFERENCE,
                    source_id='source_id2',
                    text_sha_256='text_sha2564',
                    title='title4',
                    url='url2'
                )
            ],
            limitations=[
                'limitations3'
            ]
        )
    ),
    status=Status5Enum.MANUAL_REVIEW,
    time_evidence=TimeEvidence(
        events=[
            MessageTimeEvent(
                at='at4',
                channel=ChannelEnum.EMAIL,
                direction=DirectionEnum.INBOUND,
                message_digest='message_digest2',
                topic=TopicEnum.ORDER_DETAILS_PROVIDED
            )
        ],
        flags=[
            FlagEnum.ORDER_RECORD_ABSENT,
            FlagEnum.DELIVERY_NOT_RECORDED,
            FlagEnum.DELIVERY_AFTER_CLAIM
        ],
        gaps_seconds=TimeGaps(
            delivery_to_claim=210,
            payment_to_claim=154,
            payment_to_delivery=192,
            payment_to_order_record=208
        )
    )
)
```



