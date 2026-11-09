# Dispute Evidence Row

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkRpc3B1dGVFdmlkZW5jZVJvdw

DisputeEvidenceRow.


# Class Name

`DisputeEvidenceRow`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | String \| nil | Optional | This is a container for any-of cases. |
| `date` | String \| nil | Optional | This is a container for any-of cases. |
| `evidence_type` | `String` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` |
| `source` | [`Source3Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/source-3.md) | Required | Source. |


# Example

```ruby
dispute_evidence_row = DisputeEvidenceRow.new(
  'evidence_type8',
  Source3Enum::REQUESTED_FROM_SELLER,
  'String7',
  'String3'
)
```



