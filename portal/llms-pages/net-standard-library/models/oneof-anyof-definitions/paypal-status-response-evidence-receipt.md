# Paypal Status Response Evidence Receipt

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlBheXBhbFN0YXR1c1Jlc3BvbnNlRXZpZGVuY2VSZWNlaXB0


# Class Name

`PaypalStatusResponseEvidenceReceipt`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`SandboxEvidenceReceipt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/sandbox-evidence-receipt.md) | PaypalStatusResponseEvidenceReceipt.FromSandboxEvidenceReceipt(SandboxEvidenceReceipt sandboxEvidenceReceipt) |


# SandboxEvidenceReceipt

## Initialization Code

### Example

```csharp
PaypalStatusResponseEvidenceReceipt value = PaypalStatusResponseEvidenceReceipt.FromSandboxEvidenceReceipt(
    new SandboxEvidenceReceipt
    {
        Action = ActionEnum.OAUTHCONNECT,
        Environment = "sandbox",
        EvidenceClass = EvidenceClass3Enum.AUTHENTICSANDBOXRESPONSE,
        ExternalSend = "FROZEN",
        InvoiceId = SandboxEvidenceReceiptInvoiceId.FromString("String5"),
        ObservedAt = "observed_at8",
        PaypalDebugId = SandboxEvidenceReceiptPaypalDebugId.FromString("String5"),
        ProofKind = "POST_RESPONSE_ONLY",
        SchemaVersion = 1,
        SeparateGetReadback = "False",
        Status = Status10Enum.CONNECTED,
    }
);
```



