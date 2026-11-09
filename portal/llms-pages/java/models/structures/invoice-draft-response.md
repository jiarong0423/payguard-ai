# Invoice Draft Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkludm9pY2VEcmFmdFJlc3BvbnNl

InvoiceDraftResponse.


# Class Name

`InvoiceDraftResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` | String getEnvironment() | setEnvironment(String environment) |
| `EvidenceReceipt` | [`SandboxEvidenceReceipt`](http://localhost:3000/llms-pages/java/models/structures/sandbox-evidence-receipt.md) | Required | SandboxEvidenceReceipt. | SandboxEvidenceReceipt getEvidenceReceipt() | setEvidenceReceipt(SandboxEvidenceReceipt evidenceReceipt) |
| `ExternalSend` | `String` | Required, Constant | External send.<br><br>**Value**: `"FROZEN"` | String getExternalSend() | setExternalSend(String externalSend) |
| `InvoiceId` | `String` | Required | Invoice id.<br><br>**Constraints**: *Minimum Length*: `13`, *Maximum Length*: `69`, *Pattern*: `^INV2-[A-Z0-9-]{8,64}$` | String getInvoiceId() | setInvoiceId(String invoiceId) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"paypal_sandbox"` | String getSource() | setSource(String source) |
| `Status` | `String` | Required, Constant | Status.<br><br>**Value**: `"DRAFT"` | String getStatus() | setStatus(String status) |


# Example

```java
import m18000.m0.m0.m127.models.ActionEnum;
import m18000.m0.m0.m127.models.EvidenceClass3Enum;
import m18000.m0.m0.m127.models.InvoiceDraftResponse;
import m18000.m0.m0.m127.models.SandboxEvidenceReceipt;
import m18000.m0.m0.m127.models.Status10Enum;
import m18000.m0.m0.m127.models.containers.SandboxEvidenceReceiptInvoiceId;
import m18000.m0.m0.m127.models.containers.SandboxEvidenceReceiptPaypalDebugId;

InvoiceDraftResponse invoiceDraftResponse = new InvoiceDraftResponse.Builder(
    "sandbox",
    new SandboxEvidenceReceipt.Builder(
        ActionEnum.OAUTH_CONNECT,
        "sandbox",
        EvidenceClass3Enum.AUTHENTIC_SANDBOX_RESPONSE,
        "FROZEN",
        SandboxEvidenceReceiptInvoiceId.fromString(
            "String3"
        ),
        "observed_at6",
        SandboxEvidenceReceiptPaypalDebugId.fromString(
            "String3"
        ),
        "POST_RESPONSE_ONLY",
        1,
        "False",
        Status10Enum.CONNECTED
    )
    .build(),
    "FROZEN",
    "invoice_id6",
    "paypal_sandbox",
    "DRAFT"
)
.build();
```



