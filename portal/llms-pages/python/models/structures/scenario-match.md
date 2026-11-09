# Scenario Match

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlNjZW5hcmlvTWF0Y2g

ScenarioMatch.


# Class Name

`ScenarioMatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `current_policy_applicability` | `str` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `engine_execution` | `str` | Required, Constant | Engine execution.<br><br>**Value**: `"NOT_RUN"` |
| `evaluation_scope` | `str` | Required, Constant | Evaluation scope.<br><br>**Value**: `"AUTHORED_SYNTHETIC_DEMO_ONLY"` |
| `intake_status` | [`IntakeStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/intake-status.md) | Required | Intake status. |
| `operational_authority` | `str` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` |
| `provenance` | `str` | Required, Constant | Provenance.<br><br>**Value**: `"AUTHORED_SYNTHETIC_SCENARIOS_NOT_REAL_CASES"` |
| `real_case_evidence` | `str` | Required, Constant | Real case evidence.<br><br>**Value**: `"NOT_PROVIDED"` |
| `required_human_review` | `str` | Required, Constant | Required human review.<br><br>**Value**: `"True"` |
| `scenario` | [`DisputeScenario`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/dispute-scenario.md) | Required | DisputeScenario. |
| `schema_version` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"local_synthetic_scenario_matcher"` |
| `status` | `str` | Required, Constant | Status.<br><br>**Value**: `"synthetic_scenarios_found"` |


# Example

```python
from tradeglotlocalconsole.models.dispute_scenario import DisputeScenario
from tradeglotlocalconsole.models.intake_status_enum import IntakeStatusEnum
from tradeglotlocalconsole.models.material_type_enum import MaterialTypeEnum
from tradeglotlocalconsole.models.scenario_citation import ScenarioCitation
from tradeglotlocalconsole.models.scenario_match import ScenarioMatch

scenario_match = ScenarioMatch(
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
)
```



