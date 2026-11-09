# Invoice Draft Response

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkludm9pY2VEcmFmdFJlc3BvbnNl

InvoiceDraftResponse.


# Class Name

`InvoiceDraftResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `environment` | `str` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `evidence_receipt` | [`SandboxEvidenceReceipt`](http://localhost:3000/llms-pages/python/models/structures/sandbox-evidence-receipt.md) | Required | SandboxEvidenceReceipt. |
| `external_send` | `str` | Required, Constant | External send.<br><br>**Value**: `"FROZEN"` |
| `invoice_id` | `str` | Required | Invoice id.<br><br>**Constraints**: *Minimum Length*: `13`, *Maximum Length*: `69`, *Pattern*: `^INV2-[A-Z0-9-]{8,64}$` |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"paypal_sandbox"` |
| `status` | `str` | Required, Constant | Status.<br><br>**Value**: `"DRAFT"` |


# Example

```python
from tradeglotlocalconsole.models.action_enum import ActionEnum
from tradeglotlocalconsole.models.evidence_class_3_enum import EvidenceClass3Enum
from tradeglotlocalconsole.models.invoice_draft_response import InvoiceDraftResponse
from tradeglotlocalconsole.models.sandbox_evidence_receipt import SandboxEvidenceReceipt
from tradeglotlocalconsole.models.status_10_enum import Status10Enum

invoice_draft_response = InvoiceDraftResponse(
    evidence_receipt=SandboxEvidenceReceipt(
        action=ActionEnum.OAUTH_CONNECT,
        evidence_class=EvidenceClass3Enum.AUTHENTIC_SANDBOX_RESPONSE,
        invoice_id='String3',
        observed_at='observed_at6',
        paypal_debug_id='String3',
        status=Status10Enum.CONNECTED
    ),
    invoice_id='invoice_id8'
)
```



