# Dispute Approval Response

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkRpc3B1dGVBcHByb3ZhbFJlc3BvbnNl

DisputeApprovalResponse.


# Class Name

`DisputeApprovalResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | `str` | Required, Constant | Action.<br><br>**Value**: `"review_draft"` |
| `authenticated_actor` | `str` | Required, Constant | Authenticated actor.<br><br>**Value**: `"False"` |
| `case_ref` | `str` | Required | Case ref. |
| `durable_approval` | `str` | Required, Constant | Durable approval.<br><br>**Value**: `"False"` |
| `external_submission` | `str` | Required, Constant | External submission.<br><br>**Value**: `"FROZEN"` |
| `retention` | `str` | Required, Constant | Retention.<br><br>**Value**: `"SESSION_MEMORY_ONLY"` |
| `reviewed_at` | `datetime` | Required | Reviewed at. |
| `reviewer` | `str` | Required, Constant | Reviewer.<br><br>**Value**: `"DEMO_OPERATOR_UNAUTHENTICATED"` |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `status` | `str` | Required, Constant | Status.<br><br>**Value**: `"local_draft_reviewed"` |


# Example

```python
import dateutil.parser

from tradeglotlocalconsole.models.dispute_approval_response import DisputeApprovalResponse

dispute_approval_response = DisputeApprovalResponse(
    case_ref='case_ref6',
    reviewed_at=dateutil.parser.parse('2016-03-13T12:52:32.123Z')
)
```



