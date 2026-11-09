# Sandbox Evidence Receipt

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlNhbmRib3hFdmlkZW5jZVJlY2VpcHQ

SandboxEvidenceReceipt.


# Class Name

`SandboxEvidenceReceipt`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | [`ActionEnum`](http://localhost:3000/llms-pages/python/models/enumerations/action.md) | Required | Action. |
| `environment` | `str` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `evidence_class` | [`EvidenceClass3Enum`](http://localhost:3000/llms-pages/python/models/enumerations/evidence-class-3.md) | Required | Evidence class. |
| `external_send` | `str` | Required, Constant | External send.<br><br>**Value**: `"FROZEN"` |
| `invoice_id` | str | Required | This is a container for any-of cases. |
| `observed_at` | `str` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypal_debug_id` | str | Required | This is a container for any-of cases. |
| `proof_kind` | `str` | Required, Constant | Proof kind.<br><br>**Value**: `"POST_RESPONSE_ONLY"` |
| `schema_version` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `separate_get_readback` | `str` | Required, Constant | Separate get readback.<br><br>**Value**: `"False"` |
| `status` | [`Status10Enum`](http://localhost:3000/llms-pages/python/models/enumerations/status-10.md) | Required | Status. |


# Example

```python
from tradeglotlocalconsole.models.action_enum import ActionEnum
from tradeglotlocalconsole.models.evidence_class_3_enum import EvidenceClass3Enum
from tradeglotlocalconsole.models.sandbox_evidence_receipt import SandboxEvidenceReceipt
from tradeglotlocalconsole.models.status_10_enum import Status10Enum

sandbox_evidence_receipt = SandboxEvidenceReceipt(
    action=ActionEnum.OAUTH_CONNECT,
    evidence_class=EvidenceClass3Enum.AUTHENTIC_SANDBOX_RESPONSE,
    invoice_id='String9',
    observed_at='observed_at2',
    paypal_debug_id='String9',
    status=Status10Enum.CONNECTED
)
```



