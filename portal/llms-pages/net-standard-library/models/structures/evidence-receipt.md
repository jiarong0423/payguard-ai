# Evidence Receipt

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkV2aWRlbmNlUmVjZWlwdA

Evidence receipt.


# Class Name

`EvidenceReceipt`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Action` | [`ActionEnum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/action.md) | Optional | Action. |
| `Environment` | [`EnvironmentEnum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/environment.md) | Optional | Environment. |
| `EvidenceClass` | [`EvidenceClass3Enum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/evidence-class-3.md) | Optional | Evidence class. |
| `ExternalSend` | [`ExternalSend1Enum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/external-send-1.md) | Optional | External send. |
| `InvoiceId` | [`EvidenceReceiptInvoiceId`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/evidence-receipt-invoice-id.md) | Optional | This is a container for any-of cases. |
| `ObservedAt` | `string` | Optional | Observed at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `27` |
| `PaypalDebugId` | [`EvidenceReceiptPaypalDebugId`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/evidence-receipt-paypal-debug-id.md) | Optional | This is a container for any-of cases. |
| `ProofKind` | [`ProofKindEnum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/proof-kind.md) | Optional | Proof kind. |
| `SchemaVersion` | [`SchemaVersion1Enum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/schema-version-1.md) | Optional | Schema version. |
| `SeparateGetReadback` | `bool?` | Optional | Separate get readback. |
| `Status` | [`Status10Enum?`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/status-10.md) | Optional | Status. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

EvidenceReceipt evidenceReceipt = new EvidenceReceipt
{
    Action = ActionEnum.OAUTHCONNECT,
    Environment = EnvironmentEnum.Sandbox,
    EvidenceClass = EvidenceClass3Enum.AUTHENTICSANDBOXRESPONSE,
    ExternalSend = ExternalSend1Enum.FROZEN,
    InvoiceId = EvidenceReceiptInvoiceId.FromString("String1"),
};
```



