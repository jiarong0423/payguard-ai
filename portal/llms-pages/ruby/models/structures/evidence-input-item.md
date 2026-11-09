# Evidence Input Item

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXRJdGVt

EvidenceInputItem.


# Class Name

`EvidenceInputItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `evidence_info` | [`EvidenceInfo`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/evidence-info.md) | Required | EvidenceInfo. |
| `evidence_type` | `String` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` |
| `notes` | `String` | Required | Notes.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```ruby
evidence_input_item = EvidenceInputItem.new(
  EvidenceInfo.new(
    [
      TrackingInfo.new(
        CarrierNameEnum::DHL,
        'tracking_number6',
        'String1'
      )
    ]
  ),
  'evidence_type2',
  'notes2'
)
```



