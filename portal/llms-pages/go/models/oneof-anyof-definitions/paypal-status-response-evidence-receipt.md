# Paypal Status Response Evidence Receipt

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlBheXBhbFN0YXR1c1Jlc3BvbnNlRXZpZGVuY2VSZWNlaXB0


# Class Name

`PaypalStatusResponseEvidenceReceipt`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.SandboxEvidenceReceipt`](http://localhost:3000/llms-pages/go/models/structures/sandbox-evidence-receipt.md) | models.PaypalStatusResponseEvidenceReceiptContainer.FromSandboxEvidenceReceipt(models.SandboxEvidenceReceipt sandboxEvidenceReceipt) |


# models.SandboxEvidenceReceipt

## Initialization Code

### Example

```go
value := models.PaypalStatusResponseEvidenceReceiptContainer.FromSandboxEvidenceReceipt(models.SandboxEvidenceReceipt{
    Action:              models.ActionEnum_OAUTHCONNECT,
    Environment:         "sandbox",
    EvidenceClass:       models.EvidenceClass3Enum_AUTHENTICSANDBOXRESPONSE,
    ExternalSend:        "FROZEN",
    InvoiceId:           models.SandboxEvidenceReceiptInvoiceIdContainer.FromString("String5"),
    ObservedAt:          "observed_at8",
    PaypalDebugId:       models.SandboxEvidenceReceiptPaypalDebugIdContainer.FromString("String5"),
    ProofKind:           "POST_RESPONSE_ONLY",
    SchemaVersion:       1,
    SeparateGetReadback: "False",
    Status:              models.Status10Enum_CONNECTED,
})
```



