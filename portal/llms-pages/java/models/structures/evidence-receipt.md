# Evidence Receipt

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkV2aWRlbmNlUmVjZWlwdA

Evidence receipt.


# Class Name

`EvidenceReceipt`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Action` | [`ActionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/action.md) | Optional | Action. | ActionEnum getAction() | setAction(ActionEnum action) |
| `Environment` | [`EnvironmentEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/environment.md) | Optional | Environment. | EnvironmentEnum getEnvironment() | setEnvironment(EnvironmentEnum environment) |
| `EvidenceClass` | [`EvidenceClass3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/evidence-class-3.md) | Optional | Evidence class. | EvidenceClass3Enum getEvidenceClass() | setEvidenceClass(EvidenceClass3Enum evidenceClass) |
| `ExternalSend` | [`ExternalSend1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/external-send-1.md) | Optional | External send. | ExternalSend1Enum getExternalSend() | setExternalSend(ExternalSend1Enum externalSend) |
| `InvoiceId` | [`EvidenceReceiptInvoiceId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/evidence-receipt-invoice-id.md) | Optional | This is a container for any-of cases. | EvidenceReceiptInvoiceId getInvoiceId() | setInvoiceId(EvidenceReceiptInvoiceId invoiceId) |
| `ObservedAt` | `String` | Optional | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` | String getObservedAt() | setObservedAt(String observedAt) |
| `PaypalDebugId` | [`EvidenceReceiptPaypalDebugId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/evidence-receipt-paypal-debug-id.md) | Optional | This is a container for any-of cases. | EvidenceReceiptPaypalDebugId getPaypalDebugId() | setPaypalDebugId(EvidenceReceiptPaypalDebugId paypalDebugId) |
| `ProofKind` | [`ProofKindEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/proof-kind.md) | Optional | Proof kind. | ProofKindEnum getProofKind() | setProofKind(ProofKindEnum proofKind) |
| `SchemaVersion` | [`SchemaVersion1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/schema-version-1.md) | Optional | Schema version. | SchemaVersion1Enum getSchemaVersion() | setSchemaVersion(SchemaVersion1Enum schemaVersion) |
| `SeparateGetReadback` | `Boolean` | Optional | Separate get readback. | Boolean getSeparateGetReadback() | setSeparateGetReadback(Boolean separateGetReadback) |
| `Status` | [`Status10Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/status-10.md) | Optional | Status. | Status10Enum getStatus() | setStatus(Status10Enum status) |


# Example

```java
import m18000.m0.m0.m127.models.ActionEnum;
import m18000.m0.m0.m127.models.EnvironmentEnum;
import m18000.m0.m0.m127.models.EvidenceClass3Enum;
import m18000.m0.m0.m127.models.EvidenceReceipt;
import m18000.m0.m0.m127.models.ExternalSend1Enum;
import m18000.m0.m0.m127.models.containers.EvidenceReceiptInvoiceId;

EvidenceReceipt evidenceReceipt = new EvidenceReceipt.Builder()
    .action(ActionEnum.OAUTH_CONNECT)
    .environment(EnvironmentEnum.SANDBOX)
    .evidenceClass(EvidenceClass3Enum.AUTHENTIC_SANDBOX_RESPONSE)
    .externalSend(ExternalSend1Enum.FROZEN)
    .invoiceId(EvidenceReceiptInvoiceId.fromString(
        "String1"
    ))
    .build();
```



