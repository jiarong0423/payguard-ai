# Provide Evidence Request

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlByb3ZpZGVFdmlkZW5jZVJlcXVlc3Q

ProvideEvidenceRequest.


# Class Name

`ProvideEvidenceRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_ref` | `String` | Required | Case ref.<br><br>**Constraints**: *Pattern*: `^case-ref-[0-9]{3}$` |
| `confirm_token` | String \| nil | Optional | This is a container for any-of cases. |
| `dispute_id` | `String` | Required | Dispute id.<br><br>**Constraints**: *Pattern*: `^PP-[A-Z0-9][A-Z0-9-]{2,62}$` |
| `submit` | `TrueClass \| FalseClass` | Optional | Submit.<br><br>**Default**: `false` |


# Example

```ruby
provide_evidence_request = ProvideEvidenceRequest.new(
  'case_ref8',
  'dispute_id6',
  'String5',
  false
)
```



