# Restricted Original Summary

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlJlc3RyaWN0ZWRPcmlnaW5hbFN1bW1hcnk

RestrictedOriginalSummary.


# Class Name

`RestrictedOriginalSummary`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `attachment_count` | `int` | Required | Attachment count.<br><br>**Constraints**: `>= 0`, `<= 20` |
| `content_returned` | `str` | Required, Constant | Content returned.<br><br>**Value**: `"False"` |
| `custody` | `str` | Required, Constant | Custody.<br><br>**Value**: `"SESSION_MEMORY_ONLY"` |
| `data_class` | `str` | Required, Constant | Data class.<br><br>**Value**: `"SYNTHETIC_RESTRICTED_EVIDENCE"` |
| `persistent_storage` | `str` | Required, Constant | Persistent storage.<br><br>**Value**: `"NOT_IMPLEMENTED"` |
| `production_pii_vault` | `str` | Required, Constant | Production pii vault.<br><br>**Value**: `"NOT_IMPLEMENTED"` |
| `profile` | `str` | Required, Constant | Profile.<br><br>**Value**: `"RESTRICTED_ORIGINAL_METADATA_V1"` |
| `proof_record_count` | `int` | Required | Proof record count.<br><br>**Constraints**: `>= 0`, `<= 128` |
| `provider_submission` | `str` | Required, Constant | Provider submission.<br><br>**Value**: `"NOT_PERFORMED"` |
| `schema_version` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` |


# Example

```python
from tradeglotlocalconsole.models.restricted_original_summary import RestrictedOriginalSummary

restricted_original_summary = RestrictedOriginalSummary(
    attachment_count=20,
    proof_record_count=96
)
```



