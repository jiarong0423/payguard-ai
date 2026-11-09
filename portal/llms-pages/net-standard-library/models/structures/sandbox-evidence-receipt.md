# Sandbox Evidence Receipt

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlNhbmRib3hFdmlkZW5jZVJlY2VpcHQ

SandboxEvidenceReceipt.


# Class Name

`SandboxEvidenceReceipt`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Action` | [`ActionEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/action.md) | Required | Action. |
| `Environment` | `string` | Required, Constant | Environment.<br><br>**Value**: `"sandbox"` |
| `EvidenceClass` | [`EvidenceClass3Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/evidence-class-3.md) | Required | Evidence class. |
| `ExternalSend` | `string` | Required, Constant | External send.<br><br>**Value**: `"FROZEN"` |
| `InvoiceId` | [`SandboxEvidenceReceiptInvoiceId`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/sandbox-evidence-receipt-invoice-id.md) | Required | This is a container for any-of cases. |
| `ObservedAt` | `string` | Required | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `PaypalDebugId` | [`SandboxEvidenceReceiptPaypalDebugId`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/sandbox-evidence-receipt-paypal-debug-id.md) | Required | This is a container for any-of cases. |
| `ProofKind` | `string` | Required, Constant | Proof kind.<br><br>**Value**: `"POST_RESPONSE_ONLY"` |
| `SchemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` |
| `SeparateGetReadback` | `string` | Required, Constant | Separate get readback.<br><br>**Value**: `"False"` |
| `Status` | [`Status10Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/status-10.md) | Required | Status. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

SandboxEvidenceReceipt sandboxEvidenceReceipt = new SandboxEvidenceReceipt
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
};
```



