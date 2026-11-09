# Aup Response

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkF1cFJlc3BvbnNl

AupResponse.


# Class Name

`AupResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `str` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `compliance_decision` | `str` | Required, Constant | Compliance decision.<br><br>**Value**: `"NOT_MADE"` |
| `current_policy_applicability` | `str` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `description_digest` | `str` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `evaluated_at` | `str` | Required | Evaluated at. |
| `evaluation_id` | `str` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `expires_at` | `str` | Required | Expires at. |
| `findings` | [`List[Finding]`](http://localhost:3000/llms-pages/python/models/structures/finding.md) | Required | Findings. |
| `match_status` | [`MatchStatusEnum`](http://localhost:3000/llms-pages/python/models/enumerations/match-status.md) | Required | Match status. |
| `policy_url` | `str` | Required, Constant | Policy url.<br><br>**Value**: `"https://www.paypal.com/us/legalhub/paypal/acceptableuse-full"` |
| `policy_version` | `str` | Required | Policy version.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128` |
| `recommendation` | `str` | Required | Recommendation.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1000` |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `warning_copy_version` | `str` | Required, Constant | Warning copy version.<br><br>**Value**: `"aup-warning-v1"` |


# Example

```python
from tradeglotlocalconsole.models.aup_response import AupResponse
from tradeglotlocalconsole.models.category_enum import CategoryEnum
from tradeglotlocalconsole.models.finding import Finding
from tradeglotlocalconsole.models.match_status_enum import MatchStatusEnum

aup_response = AupResponse(
    description_digest='description_digest0',
    evaluated_at='evaluated_at6',
    evaluation_id='evaluation_id6',
    expires_at='expires_at4',
    findings=[
        Finding(
            category=CategoryEnum.WEAPONS
        )
    ],
    match_status=MatchStatusEnum.NO_MATCH,
    policy_version='policy_version0',
    recommendation='recommendation2'
)
```



