# Paypal Status Response

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlBheXBhbFN0YXR1c1Jlc3BvbnNl

PaypalStatusResponse.


# Class Name

`PaypalStatusResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `configured` | `bool` | Required | Configured. |
| `environment` | `str` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `evidence_receipt` | [SandboxEvidenceReceipt](http://localhost:3000/llms-pages/python/models/structures/sandbox-evidence-receipt.md) | Required | This is a container for any-of cases. |
| `last_verified_at` | str | Required | This is a container for any-of cases. |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"paypal_sandbox"` |
| `status` | [`Status11Enum`](http://localhost:3000/llms-pages/python/models/enumerations/status-11.md) | Required | Status. |


# Example

```python
from tradeglotlocalconsole.models.action_enum import ActionEnum
from tradeglotlocalconsole.models.evidence_class_3_enum import EvidenceClass3Enum
from tradeglotlocalconsole.models.paypal_status_response import PaypalStatusResponse
from tradeglotlocalconsole.models.sandbox_evidence_receipt import SandboxEvidenceReceipt
from tradeglotlocalconsole.models.status_10_enum import Status10Enum
from tradeglotlocalconsole.models.status_11_enum import Status11Enum

paypal_status_response = PaypalStatusResponse(
    configured=False,
    evidence_receipt=SandboxEvidenceReceipt(
        action=ActionEnum.OAUTH_CONNECT,
        evidence_class=EvidenceClass3Enum.AUTHENTIC_SANDBOX_RESPONSE,
        invoice_id='String5',
        observed_at='observed_at8',
        paypal_debug_id='String5',
        status=Status10Enum.CONNECTED
    ),
    last_verified_at='String3',
    status=Status11Enum.CONNECTED
)
```



