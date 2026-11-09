# Paypal Status Response

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlBheXBhbFN0YXR1c1Jlc3BvbnNl

PaypalStatusResponse.


# Class Name

`PaypalStatusResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Configured` | `boolean` | Required | Configured. | boolean getConfigured() | setConfigured(boolean configured) |
| `Environment` | `String` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` | String getEnvironment() | setEnvironment(String environment) |
| `EvidenceReceipt` | [`PaypalStatusResponseEvidenceReceipt`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/paypal-status-response-evidence-receipt.md) | Required | This is a container for any-of cases. | PaypalStatusResponseEvidenceReceipt getEvidenceReceipt() | setEvidenceReceipt(PaypalStatusResponseEvidenceReceipt evidenceReceipt) |
| `LastVerifiedAt` | [`PaypalStatusResponseLastVerifiedAt`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/paypal-status-response-last-verified-at.md) | Required | This is a container for any-of cases. | PaypalStatusResponseLastVerifiedAt getLastVerifiedAt() | setLastVerifiedAt(PaypalStatusResponseLastVerifiedAt lastVerifiedAt) |
| `Source` | `String` | Required, Constant | Source.<br><br>**Value**: `"paypal_sandbox"` | String getSource() | setSource(String source) |
| `Status` | [`Status11Enum`](http://localhost:3000/llms-pages/java/models/enumerations/status-11.md) | Required | Status. | Status11Enum getStatus() | setStatus(Status11Enum status) |


# Example

```java
import m18000.m0.m0.m127.models.ActionEnum;
import m18000.m0.m0.m127.models.EvidenceClass3Enum;
import m18000.m0.m0.m127.models.PaypalStatusResponse;
import m18000.m0.m0.m127.models.SandboxEvidenceReceipt;
import m18000.m0.m0.m127.models.Status10Enum;
import m18000.m0.m0.m127.models.Status11Enum;
import m18000.m0.m0.m127.models.containers.PaypalStatusResponseEvidenceReceipt;
import m18000.m0.m0.m127.models.containers.PaypalStatusResponseLastVerifiedAt;
import m18000.m0.m0.m127.models.containers.SandboxEvidenceReceiptInvoiceId;
import m18000.m0.m0.m127.models.containers.SandboxEvidenceReceiptPaypalDebugId;

PaypalStatusResponse paypalStatusResponse = new PaypalStatusResponse.Builder(
    false,
    "sandbox",
    PaypalStatusResponseEvidenceReceipt.fromSandboxEvidenceReceipt(
        new SandboxEvidenceReceipt.Builder(
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
        .build()
    ),
    PaypalStatusResponseLastVerifiedAt.fromString(
        "String3"
    ),
    "paypal_sandbox",
    Status11Enum.CONNECTED
)
.build();
```



