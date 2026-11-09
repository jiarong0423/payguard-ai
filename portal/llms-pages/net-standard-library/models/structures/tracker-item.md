# Tracker Item

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlRyYWNrZXJJdGVt

TrackerItem.


# Class Name

`TrackerItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Carrier` | [`CarrierEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/carrier.md) | Required | Carrier. |
| `CarrierNameOther` | [`TrackerItemCarrierNameOther`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/tracker-item-carrier-name-other.md) | Optional | This is a container for any-of cases. |
| `Status` | `string` | Required, Constant | Status.<br><br>**Value**: `"SHIPPED"` |
| `TrackingNumber` | `string` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` |
| `TransactionId` | `string` | Required | Transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9*._-]{1,64}$` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

TrackerItem trackerItem = new TrackerItem
{
    Carrier = CarrierEnum.TWCHUNGHWAPOST,
    Status = "SHIPPED",
    TrackingNumber = "tracking_number6",
    TransactionId = "transaction_id6",
    CarrierNameOther = TrackerItemCarrierNameOther.FromString("String1"),
};
```



