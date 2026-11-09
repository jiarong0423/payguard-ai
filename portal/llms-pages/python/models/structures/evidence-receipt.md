# Evidence Receipt

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkV2aWRlbmNlUmVjZWlwdA

Evidence receipt.


# Class Name

`EvidenceReceipt`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | [`ActionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/action.md) | Optional | Action. |
| `environment` | [`EnvironmentEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/environment.md) | Optional | Environment. |
| `evidence_class` | [`EvidenceClass3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/evidence-class-3.md) | Optional | Evidence class. |
| `external_send` | [`ExternalSend1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/external-send-1.md) | Optional | External send. |
| `invoice_id` | str \| None | Optional | This is a container for any-of cases. |
| `observed_at` | `str` | Optional | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `paypal_debug_id` | str \| None | Optional | This is a container for any-of cases. |
| `proof_kind` | [`ProofKindEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/proof-kind.md) | Optional | Proof kind. |
| `schema_version` | [`SchemaVersion1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/schema-version-1.md) | Optional | Schema version. |
| `separate_get_readback` | `bool` | Optional | Separate get readback. |
| `status` | [`Status10Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/status-10.md) | Optional | Status. |


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



