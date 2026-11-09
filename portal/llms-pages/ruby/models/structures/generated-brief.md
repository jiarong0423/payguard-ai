# Generated Brief

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkdlbmVyYXRlZEJyaWVm

GeneratedBrief.


# Class Name

`GeneratedBrief`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `citation_ids` | `Array[String]` | Required | Citation ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `3`, *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z0-9-]+$` |
| `evidence_points` | `Array[String]` | Required | Evidence points.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` |
| `missing_evidence` | `Array[String]` | Required | Missing evidence.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `5`, *Minimum Length*: `1`, *Maximum Length*: `300` |
| `summary` | `String` | Required | Summary.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1200` |


# Example

```ruby
generated_brief = GeneratedBrief.new(
  [
    'citation_ids5',
    'citation_ids6'
  ],
  [
    'evidence_points6'
  ],
  [
    'missing_evidence9',
    'missing_evidence0',
    'missing_evidence1'
  ],
  'summary6'
)
```



