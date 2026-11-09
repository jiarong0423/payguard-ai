# Tracking Info

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlRyYWNraW5nSW5mbw

TrackingInfo.


# Class Name

`TrackingInfo`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CarrierName` | [`CarrierNameEnum`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/carrier-name.md) | Required | Carrier name. |
| `CarrierNameOther` | [`TrackingInfoCarrierNameOther`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/tracking-info-carrier-name-other.md) | Optional | This is a container for any-of cases. |
| `TrackingNumber` | `string` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

TrackingInfo trackingInfo = new TrackingInfo
{
    CarrierName = CarrierNameEnum.TWCHUNGHWAPOST,
    TrackingNumber = "tracking_number4",
    CarrierNameOther = TrackingInfoCarrierNameOther.FromString("String9"),
};
```



