# Dispute Scenario

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkRpc3B1dGVTY2VuYXJpbw

DisputeScenario.


# Class Name

`DisputeScenario`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `citations` | [`List[ScenarioCitation]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/scenario-citation.md) | Required | Citations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `evidence_class` | `str` | Required, Constant | Evidence class.<br><br>**Value**: `"SYNTHETIC_DEMO_SCENARIO"` |
| `expected_route` | `str` | Required, Constant | Expected route.<br><br>**Value**: `"PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW"` |
| `final_authority` | `str` | Required, Constant | Final authority.<br><br>**Value**: `"PAYPAL_OR_EXTERNAL_ISSUER"` |
| `jurisdiction` | `str` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `limitations` | `List[str]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `8` |
| `scenario_id` | `str` | Required, Constant | Scenario id.<br><br>**Value**: `"US-DEMO-DISPUTE-EVIDENCE"` |
| `theme` | `str` | Required, Constant | Theme.<br><br>**Value**: `"dispute_mediation"` |
| `title` | `str` | Required, Constant | Title.<br><br>**Value**: `"INR or counterfeit evidence organization"` |


# Example

```python
from tradeglotlocalconsole.models.dispute_scenario import DisputeScenario
from tradeglotlocalconsole.models.material_type_enum import MaterialTypeEnum
from tradeglotlocalconsole.models.scenario_citation import ScenarioCitation

dispute_scenario = DisputeScenario(
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
```



