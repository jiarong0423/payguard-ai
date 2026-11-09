# Evidence

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkV2aWRlbmNl

Evidence.


# Class Name

`Evidence`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CarrierStatus` | [`EvidenceCarrierStatus`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/evidence-carrier-status.md) | Optional | This is a container for any-of cases. |
| `DeliveredAt` | [`EvidenceDeliveredAt`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/evidence-delivered-at.md) | Optional | This is a container for any-of cases. |
| `EvidenceSource` | `string` | Required, Constant | Evidence source.<br><br>**Value**: `"synthetic"` |
| `OpenedAt` | [`EvidenceOpenedAt`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/evidence-opened-at.md) | Optional | This is a container for any-of cases. |
| `OrderCreatedAt` | [`EvidenceOrderCreatedAt`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/evidence-order-created-at.md) | Optional | This is a container for any-of cases. |
| `Reason` | [`EvidenceReason`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/evidence-reason.md) | Optional | This is a container for any-of cases. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

Evidence evidence = new Evidence
{
    EvidenceSource = "synthetic",
    CarrierStatus = EvidenceCarrierStatus.FromString("String5"),
    DeliveredAt = EvidenceDeliveredAt.FromString("String1"),
    OpenedAt = EvidenceOpenedAt.FromString("String1"),
    OrderCreatedAt = EvidenceOrderCreatedAt.FromString("String3"),
    Reason = EvidenceReason.FromString("String3"),
};
```



