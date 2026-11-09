# Invoice Draft Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkludm9pY2VEcmFmdFJlc3BvbnNl

InvoiceDraftResponse.


# Class Name

`InvoiceDraftResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceReceipt` | [`SandboxEvidenceReceipt`](http://localhost:3000/llms-pages/net-standard-library/models/structures/sandbox-evidence-receipt.md) | Required | SandboxEvidenceReceipt. |
| `ExternalSend` | `string` | Required, Constant | External send.<br><br>**Value**: `"FROZEN"` |
| `InvoiceId` | `string` | Required | Invoice id.<br><br>**Constraints**: *Minimum Length*: `13`, *Maximum Length*: `69`, *Pattern*: `^INV2-[A-Z0-9-]{8,64}$` |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"paypal_sandbox"` |
| `Status` | `string` | Required, Constant | Status.<br><br>**Value**: `"DRAFT"` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

InvoiceDraftResponse invoiceDraftResponse = new InvoiceDraftResponse
{
    Environment = "sandbox",
    EvidenceReceipt = new SandboxEvidenceReceipt
    {
        Action = ActionEnum.OAUTHCONNECT,
        Environment = "sandbox",
        EvidenceClass = EvidenceClass3Enum.AUTHENTICSANDBOXRESPONSE,
        ExternalSend = "FROZEN",
        InvoiceId = SandboxEvidenceReceiptInvoiceId.FromString("String3"),
        ObservedAt = "observed_at6",
        PaypalDebugId = SandboxEvidenceReceiptPaypalDebugId.FromString("String3"),
        ProofKind = "POST_RESPONSE_ONLY",
        SchemaVersion = 1,
        SeparateGetReadback = "False",
        Status = Status10Enum.CONNECTED,
    },
    ExternalSend = "FROZEN",
    InvoiceId = "invoice_id6",
    Source = "paypal_sandbox",
    Status = "DRAFT",
};
```



