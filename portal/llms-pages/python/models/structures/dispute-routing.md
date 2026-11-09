# Dispute Routing

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkRpc3B1dGVSb3V0aW5n

DisputeRouting.


# Class Name

`DisputeRouting`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `available_actions` | `List[str]` | Required | Available actions.<br><br>**Constraints**: *Maximum Items*: `20` |
| `dispute_life_cycle_stage` | [`DisputeLifeCycleStageEnum`](http://localhost:3000/llms-pages/python/models/enumerations/dispute-life-cycle-stage.md) | Required | Dispute life cycle stage. |
| `due_state` | [`DueStateEnum`](http://localhost:3000/llms-pages/python/models/enumerations/due-state.md) | Required | Due state. |
| `human_review_required` | `str` | Required, Constant | Human review required.<br><br>**Value**: `"True"` |
| `overall_state` | [`OverallStateEnum`](http://localhost:3000/llms-pages/python/models/enumerations/overall-state.md) | Required | Overall state. |
| `provider_submission` | `str` | Required, Constant | Provider submission.<br><br>**Value**: `"NOT_PERFORMED"` |
| `reason` | [`Reason2Enum`](http://localhost:3000/llms-pages/python/models/enumerations/reason-2.md) | Required | Reason. |
| `requirements` | [`List[DisputeRequirement]`](http://localhost:3000/llms-pages/python/models/structures/dispute-requirement.md) | Required | Requirements.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `schema_version` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `seller_response_due_date` | `str` | Required | Seller response due date.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `snapshot_class` | `str` | Required, Constant | Snapshot class.<br><br>**Value**: `"SYNTHETIC_PROVIDER_FIXTURE"` |
| `status` | [`Status3Enum`](http://localhost:3000/llms-pages/python/models/enumerations/status-3.md) | Required | Status. |


# Example

```python
from tradeglotlocalconsole.models.dispute_life_cycle_stage_enum import DisputeLifeCycleStageEnum
from tradeglotlocalconsole.models.dispute_requirement import DisputeRequirement
from tradeglotlocalconsole.models.dispute_routing import DisputeRouting
from tradeglotlocalconsole.models.due_state_enum import DueStateEnum
from tradeglotlocalconsole.models.overall_state_enum import OverallStateEnum
from tradeglotlocalconsole.models.reason_2_enum import Reason2Enum
from tradeglotlocalconsole.models.requirement_state_enum import RequirementStateEnum
from tradeglotlocalconsole.models.status_3_enum import Status3Enum

dispute_routing = DisputeRouting(
    available_actions=[
        'available_actions2',
        'available_actions3'
    ],
    dispute_life_cycle_stage=DisputeLifeCycleStageEnum.CHARGEBACK,
    due_state=DueStateEnum.OPEN,
    overall_state=OverallStateEnum.DUE_DATE_EXPIRED,
    reason=Reason2Enum.DUPLICATE_TRANSACTION,
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
    seller_response_due_date='seller_response_due_date0',
    status=Status3Enum.OPEN
)
```



