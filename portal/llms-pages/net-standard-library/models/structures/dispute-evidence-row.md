# Dispute Evidence Row

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkRpc3B1dGVFdmlkZW5jZVJvdw

DisputeEvidenceRow.


# Class Name

`DisputeEvidenceRow`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Action` | [`DisputeEvidenceRowAction`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-evidence-row-action.md) | Optional | This is a container for any-of cases. |
| `Date` | [`DisputeEvidenceRowDate`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/dispute-evidence-row-date.md) | Optional | This is a container for any-of cases. |
| `EvidenceType` | `string` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` |
| `Source` | [`Source3Enum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/source-3.md) | Required | Source. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

DisputeEvidenceRow disputeEvidenceRow = new DisputeEvidenceRow
{
    EvidenceType = "evidence_type8",
    Source = Source3Enum.REQUESTEDFROMSELLER,
    Action = DisputeEvidenceRowAction.FromString("String7"),
    Date = DisputeEvidenceRowDate.FromString("String3"),
};
```



