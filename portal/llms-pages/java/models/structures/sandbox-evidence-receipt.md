# Sandbox Evidence Receipt

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlNhbmRib3hFdmlkZW5jZVJlY2VpcHQ

SandboxEvidenceReceipt.


# Class Name

`SandboxEvidenceReceipt`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Action` | [`ActionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/action.md) | Required | Action. | ActionEnum getAction() | setAction(ActionEnum action) |
| `Environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` | String getEnvironment() | setEnvironment(String environment) |
| `EvidenceClass` | [`EvidenceClass3Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/evidence-class-3.md) | Required | Evidence class. | EvidenceClass3Enum getEvidenceClass() | setEvidenceClass(EvidenceClass3Enum evidenceClass) |
| `ExternalSend` | `String` | Required, Constant | External send.<br><br>**Value**: `"FROZEN"` | String getExternalSend() | setExternalSend(String externalSend) |
| `InvoiceId` | [`SandboxEvidenceReceiptInvoiceId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/sandbox-evidence-receipt-invoice-id.md) | Required | This is a container for any-of cases. | SandboxEvidenceReceiptInvoiceId getInvoiceId() | setInvoiceId(SandboxEvidenceReceiptInvoiceId invoiceId) |
| `ObservedAt` | `String` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` | String getObservedAt() | setObservedAt(String observedAt) |
| `PaypalDebugId` | [`SandboxEvidenceReceiptPaypalDebugId`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/sandbox-evidence-receipt-paypal-debug-id.md) | Required | This is a container for any-of cases. | SandboxEvidenceReceiptPaypalDebugId getPaypalDebugId() | setPaypalDebugId(SandboxEvidenceReceiptPaypalDebugId paypalDebugId) |
| `ProofKind` | `String` | Required, Constant | Proof kind.<br><br>**Value**: `"POST_RESPONSE_ONLY"` | String getProofKind() | setProofKind(String proofKind) |
| `SchemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` | int getSchemaVersion() | setSchemaVersion(int schemaVersion) |
| `SeparateGetReadback` | `String` | Required, Constant | Separate get readback.<br><br>**Value**: `"False"` | String getSeparateGetReadback() | setSeparateGetReadback(String separateGetReadback) |
| `Status` | [`Status10Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/enumerations/status-10.md) | Required | Status. | Status10Enum getStatus() | setStatus(Status10Enum status) |


# Example

```java
import m18000.m0.m0.m127.models.ActionEnum;
import m18000.m0.m0.m127.models.EvidenceClass3Enum;
import m18000.m0.m0.m127.models.SandboxEvidenceReceipt;
import m18000.m0.m0.m127.models.Status10Enum;
import m18000.m0.m0.m127.models.containers.SandboxEvidenceReceiptInvoiceId;
import m18000.m0.m0.m127.models.containers.SandboxEvidenceReceiptPaypalDebugId;

SandboxEvidenceReceipt sandboxEvidenceReceipt = new SandboxEvidenceReceipt.Builder(
    ActionEnum.OAUTH_CONNECT,
    "sandbox",
    EvidenceClass3Enum.AUTHENTIC_SANDBOX_RESPONSE,
    "FROZEN",
    SandboxEvidenceReceiptInvoiceId.fromString(
        "String5"
    ),
    "observed_at8",
    SandboxEvidenceReceiptPaypalDebugId.fromString(
        "String5"
    ),
    "POST_RESPONSE_ONLY",
    1,
    "False",
    Status10Enum.CONNECTED
)
.build();
```



