# Evidence Receipt

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkV2aWRlbmNlUmVjZWlwdA

Evidence receipt.


# Class Name

`EvidenceReceipt`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | [`ActionEnum`](http://localhost:3000/llms-pages/python/models/enumerations/action.md) | Optional | Action. |
| `environment` | [`EnvironmentEnum`](http://localhost:3000/llms-pages/python/models/enumerations/environment.md) | Optional | Environment. |
| `evidence_class` | [`EvidenceClass3Enum`](http://localhost:3000/llms-pages/python/models/enumerations/evidence-class-3.md) | Optional | Evidence class. |
| `external_send` | [`ExternalSend1Enum`](http://localhost:3000/llms-pages/python/models/enumerations/external-send-1.md) | Optional | External send. |
| `invoice_id` | str \| None | Optional | This is a container for any-of cases. |
| `observed_at` | `str` | Optional | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypal_debug_id` | str \| None | Optional | This is a container for any-of cases. |
| `proof_kind` | [`ProofKindEnum`](http://localhost:3000/llms-pages/python/models/enumerations/proof-kind.md) | Optional | Proof kind. |
| `schema_version` | [`SchemaVersion1Enum`](http://localhost:3000/llms-pages/python/models/enumerations/schema-version-1.md) | Optional | Schema version. |
| `separate_get_readback` | `bool` | Optional | Separate get readback. |
| `status` | [`Status10Enum`](http://localhost:3000/llms-pages/python/models/enumerations/status-10.md) | Optional | Status. |


# Example

```python
from tradeglotlocalconsole.models.action_enum import ActionEnum
from tradeglotlocalconsole.models.environment_enum import EnvironmentEnum
from tradeglotlocalconsole.models.evidence_class_3_enum import EvidenceClass3Enum
from tradeglotlocalconsole.models.evidence_receipt import EvidenceReceipt
from tradeglotlocalconsole.models.external_send_1_enum import ExternalSend1Enum

evidence_receipt = EvidenceReceipt(
    action=ActionEnum.OAUTH_CONNECT,
    environment=EnvironmentEnum.SANDBOX,
    evidence_class=EvidenceClass3Enum.AUTHENTIC_SANDBOX_RESPONSE,
    external_send=ExternalSend1Enum.FROZEN,
    invoice_id='String3'
)
```



