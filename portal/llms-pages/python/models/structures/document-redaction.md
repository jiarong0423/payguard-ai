# Document Redaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkRvY3VtZW50UmVkYWN0aW9u

DocumentRedaction.


# Class Name

`DocumentRedaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `counts` | `Dict[str, int]` | Required | Counts.<br><br>**Constraints**: `>= 1`, `<= 128` |
| `export_profile` | `str` | Required, Constant | Export profile.<br><br>**Value**: `"INTERNAL_REVIEW_ONLY_V1"` |
| `limitations` | `List[str]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `8`, *Minimum Length*: `1`, *Maximum Length*: `1000` |
| `limited_detection` | `str` | Required, Constant | Limited detection.<br><br>**Value**: `"True"` |
| `manual_review_required` | `str` | Required, Constant | Manual review required.<br><br>**Value**: `"True"` |
| `method` | `str` | Required, Constant | Method.<br><br>**Value**: `"HMAC-SHA256 document pseudonymization v1"` |
| `redacted_text` | `str` | Required | Redacted text.<br><br>**Constraints**: *Maximum Length*: `32768` |
| `replacement_count` | `int` | Required | Replacement count.<br><br>**Constraints**: `>= 0`, `<= 128` |
| `reversibility` | `str` | Required, Constant | Reversibility.<br><br>**Value**: `"False"` |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `types` | [`List[TypeEnum]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/type.md) | Required | Types.<br><br>**Constraints**: *Maximum Items*: `7` |


# Example

```python
from tradeglotlocalconsole.models.document_redaction import DocumentRedaction
from tradeglotlocalconsole.models.type_enum import TypeEnum

document_redaction = DocumentRedaction(
    counts={
        'key0': 128
    },
    limitations=[
        'limitations9',
        'limitations8',
        'limitations7'
    ],
    redacted_text='redacted_text8',
    replacement_count=128,
    types=[
        TypeEnum.MANUAL
    ]
)
```



