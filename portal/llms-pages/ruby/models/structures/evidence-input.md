# Evidence Input

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXQ

EvidenceInput.


# Class Name

`EvidenceInput`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `evidences` | [`Array[EvidenceInputItem]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/evidence-input-item.md) | Required | Evidences.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |


# Example

```ruby
evidence_input = EvidenceInput.new(
  [
    EvidenceInputItem.new(
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
  ]
)
```



