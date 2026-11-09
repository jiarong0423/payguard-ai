# Dispute Approval Response

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkRpc3B1dGVBcHByb3ZhbFJlc3BvbnNl

DisputeApprovalResponse.


# Class Name

`DisputeApprovalResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | `String` | Required, Constant | Action.<br><br>**Value**: `'review_draft'` |
| `authenticated_actor` | `String` | Required, Constant | Authenticated actor.<br><br>**Value**: `'False'` |
| `case_ref` | `String` | Required | Case ref. |
| `durable_approval` | `String` | Required, Constant | Durable approval.<br><br>**Value**: `'False'` |
| `external_submission` | `String` | Required, Constant | External submission.<br><br>**Value**: `'FROZEN'` |
| `retention` | `String` | Required, Constant | Retention.<br><br>**Value**: `'SESSION_MEMORY_ONLY'` |
| `reviewed_at` | `DateTime` | Required | Reviewed at. |
| `reviewer` | `String` | Required, Constant | Reviewer.<br><br>**Value**: `'DEMO_OPERATOR_UNAUTHENTICATED'` |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `status` | `String` | Required, Constant | Status.<br><br>**Value**: `'local_draft_reviewed'` |


# Example

```ruby
dispute_approval_response = DisputeApprovalResponse.new(
  'review_draft',
  'False',
  'case_ref6',
  'False',
  'FROZEN',
  'SESSION_MEMORY_ONLY',
  DateTimeHelper.from_rfc3339('2016-03-13T12:52:32.123Z'),
  'DEMO_OPERATOR_UNAUTHENTICATED',
  'synthetic',
  'local_draft_reviewed'
)
```



