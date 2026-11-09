# Paypal Status Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlBheXBhbFN0YXR1c1Jlc3BvbnNl

PaypalStatusResponse.


# Class Name

`PaypalStatusResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Configured` | `bool` | Required | Configured. |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceReceipt` | [`PaypalStatusResponseEvidenceReceipt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/paypal-status-response-evidence-receipt.md) | Required | This is a container for any-of cases. |
| `LastVerifiedAt` | [`PaypalStatusResponseLastVerifiedAt`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/paypal-status-response-last-verified-at.md) | Required | This is a container for any-of cases. |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"paypal_sandbox"` |
| `Status` | [`Status11Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/status-11.md) | Required | Status. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

PaypalStatusResponse paypalStatusResponse = new PaypalStatusResponse
{
    Configured = false,
    Environment = "sandbox",
    EvidenceReceipt = PaypalStatusResponseEvidenceReceipt.FromSandboxEvidenceReceipt(
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
    ),
    LastVerifiedAt = PaypalStatusResponseLastVerifiedAt.FromString("String3"),
    Source = "paypal_sandbox",
    Status = Status11Enum.Connected,
};
```



