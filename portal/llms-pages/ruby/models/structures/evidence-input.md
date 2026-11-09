# Evidence Input

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXQ

EvidenceInput.


# Class Name

`EvidenceInput`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `evidences` | [`Array[EvidenceInputItem]`](http://localhost:3000/llms-pages/ruby/models/structures/evidence-input-item.md) | Required | Evidences.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |


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



