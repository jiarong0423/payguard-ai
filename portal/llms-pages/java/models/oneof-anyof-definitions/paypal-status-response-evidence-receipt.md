# Paypal Status Response Evidence Receipt

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlBheXBhbFN0YXR1c1Jlc3BvbnNlRXZpZGVuY2VSZWNlaXB0


# Class Name

`PaypalStatusResponseEvidenceReceipt`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`SandboxEvidenceReceipt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/sandbox-evidence-receipt.md) | PaypalStatusResponseEvidenceReceipt.fromSandboxEvidenceReceipt(SandboxEvidenceReceipt sandboxEvidenceReceipt) |


# SandboxEvidenceReceipt

## Initialization Code

### Example

```java
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
    )
```



